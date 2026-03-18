# Agent Utility API

High-traffic utility endpoints for AI agents. x402 micropayment gated API accepting USDC on Base mainnet.

## 🚀 Endpoints

### 1. **Slug Intelligence API** 
- `POST /api/slug/generate` - Generate URL-safe slugs
- `POST /api/slug/validate` - Validate slug format
- `POST /api/slug/similarity` - Calculate slug similarity

### 2. **Indian Transliteration API**
- `POST /api/transliterate` - Roman ↔ Devanagari/Telugu/Tamil/Kannada/Malayalam/Bengali/Gujarati/Gurmukhi/Oriya

### 3. **IFSC Code Lookup**
- `POST /api/ifsc/lookup` - Full bank branch details
- `GET /api/ifsc/validate/{ifsc}` - Format validation only

### 4. **Timezone Detection**
- `POST /api/timezone/lookup` - Get timezone from coordinates

### 5. **Indian Phone Validation**
- `POST /api/phone/validate` - Format validation + carrier detection

## 💰 Payment

**Protocol**: x402 micropayment  
**Amount**: $0.001 USDC per API call  
**Recipient**: `0x41A024c1C89Fd30122c8b184de99cbE751eaC970`  
**Chain**: Base mainnet  

Include transaction hash in `x-payment` header:
```bash
curl -X POST https://your-api.railway.app/api/slug/generate \
  -H "Content-Type: application/json" \
  -H "x-payment: 0x123abc..." \
  -d '{"text": "Hello World", "max_length": 50}'
```

## 🛠️ Quick Start

### Local Development

```bash
# Clone and install
git clone <your-repo>
cd agent-utility-api
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env: set BYPASS_PAYMENT=true for local testing

# Run server
python main.py

# API docs available at http://localhost:8000/docs
```

### Railway Deployment

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up

# Set environment variables
railway variables set PAYMENT_WALLET=0x41A024c1C89Fd30122c8b184de99cbE751eaC970
railway variables set BASE_RPC_URL=https://mainnet.base.org
railway variables set PRICE_PER_CALL_USDC=0.001
railway variables set BYPASS_PAYMENT=false

# Get deployment URL
railway domain
```

## 📖 API Examples

### Slug Generation
```bash
curl -X POST http://localhost:8000/api/slug/generate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Building AI Agents with Claude",
    "max_length": 50,
    "separator": "-",
    "lowercase": true
  }'

# Response:
{
  "slug": "building-ai-agents-with-claude",
  "original": "Building AI Agents with Claude",
  "length": 31,
  "valid": true
}
```

### Transliteration
```bash
curl -X POST http://localhost:8000/api/transliterate \
  -H "Content-Type: application/json" \
  -d '{
    "text": "namaste",
    "from_script": "roman",
    "to_script": "devanagari"
  }'

# Response:
{
  "original": "namaste",
  "transliterated": "नमस्ते",
  "from_script": "roman",
  "to_script": "devanagari",
  "length": 7
}
```

### IFSC Lookup
```bash
curl -X POST http://localhost:8000/api/ifsc/lookup \
  -H "Content-Type: application/json" \
  -d '{"ifsc": "SBIN0000001"}'

# Response:
{
  "ifsc": "SBIN0000001",
  "valid_format": true,
  "bank": "State Bank of India",
  "branch": "New Delhi Main Branch",
  "address": "11, Sansad Marg, New Delhi",
  "city": "New Delhi",
  "state": "Delhi",
  "contact": "011-23374502",
  "micr": "110002001"
}
```

### Timezone Lookup
```bash
curl -X POST http://localhost:8000/api/timezone/lookup \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 19.0760,
    "longitude": 72.8777
  }'

# Response:
{
  "latitude": 19.076,
  "longitude": 72.8777,
  "timezone": "Asia/Kolkata",
  "current_time": "2024-03-18T15:30:00+05:30",
  "utc_offset": "+0530",
  "dst_active": false,
  "abbreviation": "IST"
}
```

### Phone Validation
```bash
curl -X POST http://localhost:8000/api/phone/validate \
  -H "Content-Type: application/json" \
  -d '{
    "phone": "+919876543210",
    "country_code": "IN"
  }'

# Response:
{
  "phone": "+919876543210",
  "valid": true,
  "possible": true,
  "type": "mobile",
  "carrier": "Airtel",
  "country_code": 91,
  "national_number": 9876543210,
  "formats": {
    "national": "098765 43210",
    "international": "+91 98765 43210",
    "e164": "+919876543210"
  }
}
```

## 🤖 MCP Integration

This API includes an MCP (Model Context Protocol) manifest for agent discovery:

```json
{
  "name": "agent-utility-api",
  "version": "1.0.0",
  "description": "High-traffic utility endpoints for AI agents",
  "tools": [
    {
      "name": "generate_slug",
      "description": "Generate URL-safe slug from text",
      "endpoint": "/api/slug/generate"
    },
    {
      "name": "transliterate_text",
      "description": "Transliterate between Roman and Indic scripts",
      "endpoint": "/api/transliterate"
    },
    {
      "name": "lookup_ifsc",
      "description": "Get Indian bank branch details from IFSC code",
      "endpoint": "/api/ifsc/lookup"
    },
    {
      "name": "detect_timezone",
      "description": "Get timezone from geographic coordinates",
      "endpoint": "/api/timezone/lookup"
    },
    {
      "name": "validate_phone",
      "description": "Validate Indian phone number and extract carrier",
      "endpoint": "/api/phone/validate"
    }
  ]
}
```

## 🔒 Production Readiness

### Security Checklist
- [ ] Enable payment verification (`BYPASS_PAYMENT=false`)
- [ ] Implement on-chain tx verification (TODO in middleware)
- [ ] Add rate limiting (100 req/min per IP)
- [ ] Enable HTTPS only
- [ ] Add API key authentication layer (optional)
- [ ] Monitor for abuse patterns

### Database Integration
For production IFSC lookups, integrate full database:
- Download RBI IFSC dataset (~160K branches)
- Load into PostgreSQL or SQLite
- Update `IFSC_DATABASE` to query real data

### Scaling Considerations
- Each endpoint is <1ms CPU time
- Stateless design = horizontal scaling
- Cache timezone lookups (already implemented with `@lru_cache`)
- Monitor payment verification latency

## 📊 Traffic Expectations

**High-volume endpoints** (agents call 10-100x per workflow):
- Slug generation: 1000+ req/day per agent
- Timezone detection: 500+ req/day
- Phone validation: 300+ req/day

**Medium-volume endpoints**:
- Transliteration: 200+ req/day
- IFSC lookup: 100+ req/day

**Revenue projection** at $0.001/call:
- 10 agents × 500 calls/day = $5/day = $150/month
- 100 agents × 500 calls/day = $50/day = $1,500/month

## 🛣️ Roadmap

### Phase 2 Endpoints
- GST calculation helper
- Pincode intelligence (distance, servicability)
- PAN/Aadhaar format validation
- Indian business day calculator
- URL metadata extractor

### Phase 3 Features
- Batch processing endpoints
- Webhook support for async operations
- GraphQL API layer
- WebSocket for real-time updates

## 📄 License

MIT License - free for commercial use

## 🤝 Support

- API Docs: `/docs` (Swagger UI)
- Issues: GitHub Issues
- Contact: [Your contact]

---

**Built for AI agents. Monetized via x402 micropayments. Deployed on Railway.**
