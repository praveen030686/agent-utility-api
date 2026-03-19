"""
Agent Utility API - High-traffic utility endpoints for AI agents
x402 micropayment gated API with USDC on Base mainnet
"""

from fastapi import FastAPI, HTTPException, Header, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict
import re
import unicodedata
from datetime import datetime
import pytz
import math
from functools import lru_cache
import httpx
from difflib import SequenceMatcher
import phonenumbers
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import os

# Environment configuration
PAYMENT_WALLET = os.getenv("PAYMENT_WALLET", "0x41A024c1C89Fd30122c8b184de99cbE751eaC970")
BASE_RPC_URL = os.getenv("BASE_RPC_URL", "https://mainnet.base.org")
PRICE_PER_CALL_USDC = float(os.getenv("PRICE_PER_CALL_USDC", "0.001"))  # $0.001 per call

app = FastAPI(
    title="Agent Utility API",
    description="High-traffic utility endpoints for AI agents - slug intelligence, transliteration, IFSC lookup, timezone detection, phone validation",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# x402 Payment verification middleware
async def verify_x402_payment(request: Request):
    """Verify x402 payment header with on-chain verification"""
    payment_header = request.headers.get("x-payment")
    
    # Development bypass
    if os.getenv("BYPASS_PAYMENT") == "true":
        return True
    
    if not payment_header:
        raise HTTPException(
            status_code=402,
            detail={
                "error": "Payment required",
                "payment_protocol": "x402",
                "amount": f"{PRICE_PER_CALL_USDC} USDC",
                "recipient": PAYMENT_WALLET,
                "chain": "base-mainnet",
                "instructions": "Include x-payment header with transaction hash"
            }
        )
    
    # Verify transaction on Base mainnet
    try:
        from web3 import Web3
        
        # Connect to Base RPC
        w3 = Web3(Web3.HTTPProvider(BASE_RPC_URL))
        
        # Verify connection
        if not w3.is_connected():
            raise HTTPException(
                status_code=500,
                detail="Unable to connect to Base network"
            )
        
        # Get transaction
        try:
            tx = w3.eth.get_transaction(payment_header)
        except Exception as e:
            raise HTTPException(
                status_code=402,
                detail=f"Invalid transaction hash: {str(e)}"
            )
        
        # USDC contract address on Base mainnet
        USDC_CONTRACT = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
        
        # Normalize addresses for comparison (checksummed format)
        tx_to = w3.to_checksum_address(tx['to']) if tx.get('to') else None
        usdc_contract = w3.to_checksum_address(USDC_CONTRACT)
        
        # Verify this is a USDC transfer
        if not tx_to or tx_to != usdc_contract:
            raise HTTPException(
                status_code=402,
                detail=f"Transaction is not a USDC transfer. To: {tx_to}, Expected: {usdc_contract}"
            )
        
        # Decode ERC20 transfer data
        # transfer(address,uint256) signature: 0xa9059cbb
        input_data = tx.get('input', '')
        if not input_data or len(input_data) < 10:
            raise HTTPException(
                status_code=402,
                detail="Transaction has no input data"
            )
            
        if input_data[:10] != '0xa9059cbb':
            raise HTTPException(
                status_code=402,
                detail=f"Transaction is not a token transfer. Method: {input_data[:10]}"
            )
        
        # Extract recipient address from input data
        # Input format: 0xa9059cbb + 32 bytes (address) + 32 bytes (amount)
        if len(input_data) < 138:
            raise HTTPException(
                status_code=402,
                detail="Invalid transaction input data length"
            )
            
        recipient_hex = input_data[10:74]  # 64 hex chars = 32 bytes
        recipient_address = w3.to_checksum_address('0x' + recipient_hex[-40:])  # Last 40 hex chars = 20 bytes
        payment_wallet = w3.to_checksum_address(PAYMENT_WALLET)
        
        # Verify recipient matches our wallet
        if recipient_address != payment_wallet:
            raise HTTPException(
                status_code=402,
                detail=f"Payment sent to wrong address. Expected: {payment_wallet}, Got: {recipient_address}"
            )
        
        # Extract amount from input data
        # USDC has 6 decimals
        amount_hex = input_data[74:138]  # Next 64 hex chars = 32 bytes
        amount_wei = int(amount_hex, 16)
        amount_usdc = amount_wei / 1_000_000  # Convert from smallest unit to USDC
        
        # Verify amount is sufficient
        if amount_usdc < PRICE_PER_CALL_USDC:
            raise HTTPException(
                status_code=402,
                detail=f"Insufficient payment. Required: {PRICE_PER_CALL_USDC} USDC, Received: {amount_usdc} USDC"
            )
        
        # Verify transaction has enough confirmations
        current_block = w3.eth.block_number
        tx_block = tx.get('blockNumber')
        
        if tx_block is None:
            raise HTTPException(
                status_code=402,
                detail="Transaction not yet mined. Please wait for confirmation."
            )
        
        confirmations = current_block - tx_block
        MIN_CONFIRMATIONS = 3
        
        if confirmations < MIN_CONFIRMATIONS:
            raise HTTPException(
                status_code=402,
                detail=f"Insufficient confirmations. Required: {MIN_CONFIRMATIONS}, Current: {confirmations}"
            )
        
        # Log successful payment
        print(f"✅ Payment verified: {payment_header[:10]}... | Amount: {amount_usdc} USDC | Recipient: {recipient_address}")
        
        # All checks passed
        return True
        
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log unexpected errors
        print(f"❌ Payment verification error: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=402,
            detail=f"Payment verification failed: {str(e)}"
        )

@app.middleware("http")
async def payment_middleware(request: Request, call_next):
    """Global payment verification middleware"""
    if request.url.path not in ["/", "/health", "/docs", "/redoc", "/openapi.json"]:
        try:
            await verify_x402_payment(request)
        except HTTPException as e:
            return JSONResponse(
                status_code=e.status_code,
                content=e.detail
            )
    response = await call_next(request)
    return response


# ============================================================================
# 1. SLUG INTELLIGENCE API
# ============================================================================

class SlugRequest(BaseModel):
    text: str = Field(..., description="Text to convert to slug")
    max_length: Optional[int] = Field(50, description="Maximum slug length")
    separator: Optional[str] = Field("-", description="Word separator")
    lowercase: Optional[bool] = Field(True, description="Convert to lowercase")

class SlugValidationRequest(BaseModel):
    slug: str = Field(..., description="Slug to validate")
    strict: Optional[bool] = Field(False, description="Strict validation mode")

class SlugSimilarityRequest(BaseModel):
    slug1: str = Field(..., description="First slug")
    slug2: str = Field(..., description="Second slug")

def generate_slug(text: str, max_length: int = 50, separator: str = "-", lowercase: bool = True) -> str:
    """Generate URL-friendly slug from text"""
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')
    
    # Convert to lowercase if requested
    if lowercase:
        text = text.lower()
    
    # Replace spaces and special characters with separator
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', separator, text)
    
    # Remove leading/trailing separators
    text = text.strip(separator)
    
    # Truncate to max length
    if len(text) > max_length:
        text = text[:max_length].rstrip(separator)
    
    return text

def validate_slug(slug: str, strict: bool = False) -> dict:
    """Validate if string is a proper slug"""
    if not slug:
        return {"valid": False, "reason": "Empty slug"}
    
    # Basic validation: lowercase, hyphens, alphanumeric
    if strict:
        pattern = r'^[a-z0-9]+(?:-[a-z0-9]+)*$'
    else:
        pattern = r'^[a-zA-Z0-9]+(?:[-_][a-zA-Z0-9]+)*$'
    
    if re.match(pattern, slug):
        return {"valid": True}
    else:
        return {"valid": False, "reason": "Contains invalid characters"}

def slug_similarity(slug1: str, slug2: str) -> float:
    """Calculate similarity between two slugs (0-1)"""
    return SequenceMatcher(None, slug1, slug2).ratio()

@app.post("/api/slug/generate")
async def api_generate_slug(request: SlugRequest):
    """Generate URL-friendly slug from text"""
    slug = generate_slug(
        request.text,
        request.max_length,
        request.separator,
        request.lowercase
    )
    return {
        "slug": slug,
        "original": request.text,
        "length": len(slug),
        "valid": validate_slug(slug)["valid"]
    }

@app.post("/api/slug/validate")
async def api_validate_slug(request: SlugValidationRequest):
    """Validate if string is a proper slug"""
    result = validate_slug(request.slug, request.strict)
    return {
        "slug": request.slug,
        **result
    }

@app.post("/api/slug/similarity")
async def api_slug_similarity(request: SlugSimilarityRequest):
    """Calculate similarity between two slugs"""
    similarity = slug_similarity(request.slug1, request.slug2)
    return {
        "slug1": request.slug1,
        "slug2": request.slug2,
        "similarity": round(similarity, 4),
        "percentage": f"{round(similarity * 100, 2)}%"
    }


# ============================================================================
# 2. INDIAN TRANSLITERATION API
# ============================================================================

class TransliterationRequest(BaseModel):
    text: str = Field(..., description="Text to transliterate")
    source_script: str = Field(..., description="Source script (e.g., 'devanagari', 'roman')")
    target_script: str = Field(..., description="Target script (e.g., 'telugu', 'tamil', 'roman')")

# Supported scripts mapping
SUPPORTED_SCRIPTS = {
    "devanagari": sanscript.DEVANAGARI,
    "telugu": sanscript.TELUGU,
    "tamil": sanscript.TAMIL,
    "kannada": sanscript.KANNADA,
    "malayalam": sanscript.MALAYALAM,
    "bengali": sanscript.BENGALI,
    "gujarati": sanscript.GUJARATI,
    "gurmukhi": sanscript.GURMUKHI,
    "oriya": sanscript.ORIYA,
    "roman": sanscript.ITRANS,
    "iast": sanscript.IAST,
    "itrans": sanscript.ITRANS
}

@app.post("/api/transliterate")
async def api_transliterate(request: TransliterationRequest):
    """Transliterate text between Indian scripts"""
    if request.source_script not in SUPPORTED_SCRIPTS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported source script. Supported: {list(SUPPORTED_SCRIPTS.keys())}"
        )
    
    if request.target_script not in SUPPORTED_SCRIPTS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported target script. Supported: {list(SUPPORTED_SCRIPTS.keys())}"
        )
    
    try:
        result = transliterate(
            request.text,
            SUPPORTED_SCRIPTS[request.source_script],
            SUPPORTED_SCRIPTS[request.target_script]
        )
        
        return {
            "original": request.text,
            "transliterated": result,
            "source_script": request.source_script,
            "target_script": request.target_script
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transliteration failed: {str(e)}")


# ============================================================================
# 3. IFSC LOOKUP API
# ============================================================================

class IFSCRequest(BaseModel):
    ifsc: str = Field(..., description="IFSC code (11 characters)")

# Simple IFSC data cache (in production, use database)
@lru_cache(maxsize=10000)
def get_ifsc_data(ifsc: str) -> dict:
    """Fetch IFSC data from RazorPay IFSC API"""
    try:
        response = httpx.get(f"https://ifsc.razorpay.com/{ifsc}", timeout=5.0)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

@app.post("/api/ifsc/lookup")
async def api_ifsc_lookup(request: IFSCRequest):
    """Lookup bank details by IFSC code"""
    ifsc = request.ifsc.upper().strip()
    
    # Validate IFSC format
    if not re.match(r'^[A-Z]{4}0[A-Z0-9]{6}$', ifsc):
        raise HTTPException(
            status_code=400,
            detail="Invalid IFSC format. Expected: 4 letters + 0 + 6 alphanumeric"
        )
    
    data = get_ifsc_data(ifsc)
    
    if not data:
        raise HTTPException(status_code=404, detail="IFSC code not found")
    
    return {
        "ifsc": ifsc,
        "bank": data.get("BANK"),
        "branch": data.get("BRANCH"),
        "address": data.get("ADDRESS"),
        "city": data.get("CITY"),
        "district": data.get("DISTRICT"),
        "state": data.get("STATE"),
        "micr": data.get("MICR"),
        "swift": data.get("SWIFT"),
        "contact": data.get("CONTACT"),
        "rtgs": data.get("RTGS"),
        "neft": data.get("NEFT"),
        "imps": data.get("IMPS"),
        "upi": data.get("UPI")
    }

@app.get("/api/ifsc/validate/{ifsc}")
async def api_ifsc_validate(ifsc: str):
    """Validate IFSC code format and existence"""
    ifsc = ifsc.upper().strip()
    
    # Format validation
    format_valid = bool(re.match(r'^[A-Z]{4}0[A-Z0-9]{6}$', ifsc))
    
    if not format_valid:
        return {
            "ifsc": ifsc,
            "valid": False,
            "reason": "Invalid format"
        }
    
    # Existence check
    data = get_ifsc_data(ifsc)
    
    return {
        "ifsc": ifsc,
        "valid": data is not None,
        "exists": data is not None,
        "bank": data.get("BANK") if data else None
    }


# ============================================================================
# 4. TIMEZONE DETECTION API
# ============================================================================

class TimezoneRequest(BaseModel):
    latitude: float = Field(..., description="Latitude coordinate")
    longitude: float = Field(..., description="Longitude coordinate")

@app.post("/api/timezone/lookup")
async def api_timezone_lookup(request: TimezoneRequest):
    """Detect timezone from coordinates"""
    try:
        from timezonefinder import TimezoneFinder
        
        tf = TimezoneFinder()
        timezone_str = tf.timezone_at(lat=request.latitude, lng=request.longitude)
        
        if not timezone_str:
            raise HTTPException(
                status_code=404,
                detail="Could not determine timezone for coordinates"
            )
        
        # Get current time in that timezone
        tz = pytz.timezone(timezone_str)
        current_time = datetime.now(tz)
        
        return {
            "latitude": request.latitude,
            "longitude": request.longitude,
            "timezone": timezone_str,
            "current_time": current_time.isoformat(),
            "utc_offset": current_time.strftime("%z"),
            "is_dst": bool(current_time.dst())
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Timezone lookup failed: {str(e)}")


# ============================================================================
# 5. PHONE VALIDATION API
# ============================================================================

class PhoneValidationRequest(BaseModel):
    phone: str = Field(..., description="Phone number to validate")
    country_code: Optional[str] = Field("IN", description="Country code (default: IN for India)")

@app.post("/api/phone/validate")
async def api_phone_validate(request: PhoneValidationRequest):
    """Validate and parse phone number"""
    try:
        # Parse phone number
        parsed = phonenumbers.parse(request.phone, request.country_code)
        
        # Validate
        is_valid = phonenumbers.is_valid_number(parsed)
        is_possible = phonenumbers.is_possible_number(parsed)
        
        # Get number type
        number_type = phonenumbers.number_type(parsed)
        type_name = {
            phonenumbers.PhoneNumberType.MOBILE: "mobile",
            phonenumbers.PhoneNumberType.FIXED_LINE: "landline",
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE: "fixed_or_mobile",
            phonenumbers.PhoneNumberType.TOLL_FREE: "toll_free",
            phonenumbers.PhoneNumberType.PREMIUM_RATE: "premium_rate",
            phonenumbers.PhoneNumberType.VOIP: "voip"
        }.get(number_type, "unknown")
        
        # Format number
        e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
        international = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        national = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
        
        # Get carrier (India only)
        carrier = None
        if request.country_code == "IN":
            from phonenumbers import carrier as phone_carrier
            carrier = phone_carrier.name_for_number(parsed, "en")
        
        return {
            "valid": is_valid,
            "possible": is_possible,
            "type": type_name,
            "country_code": parsed.country_code,
            "national_number": parsed.national_number,
            "e164_format": e164,
            "international_format": international,
            "national_format": national,
            "carrier": carrier
        }
    except phonenumbers.NumberParseException as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid phone number: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Phone validation failed: {str(e)}"
        )


# ============================================================================
# HEALTH CHECK & ROOT
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Agent Utility API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": [
            "/api/slug/generate",
            "/api/slug/validate",
            "/api/slug/similarity",
            "/api/transliterate",
            "/api/ifsc/lookup",
            "/api/ifsc/validate/{ifsc}",
            "/api/timezone/lookup",
            "/api/phone/validate"
        ]
    }


# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
