#!/bin/bash

# Agent Utility API - Railway Deployment Script
# Run this to deploy in 2 minutes

set -e

echo "🚀 Deploying Agent Utility API to Railway"
echo "=========================================="
echo ""

# Step 1: Check Railway CLI
if ! command -v railway &> /dev/null; then
    echo "📦 Installing Railway CLI..."
    npm install -g @railway/cli
fi

echo "✅ Railway CLI installed"
echo ""

# Step 2: Login
echo "🔐 Logging into Railway..."
echo "   → This will open your browser for authentication"
railway login
echo ""

# Step 3: Create project
echo "📁 Creating Railway project..."
railway init
echo ""

# Step 4: Deploy
echo "🚀 Deploying application..."
railway up
echo ""

# Step 5: Set environment variables
echo "⚙️  Setting environment variables..."
railway variables set PAYMENT_WALLET=0x41A024c1C89Fd30122c8b184de99cbE751eaC970
railway variables set BASE_RPC_URL=https://mainnet.base.org
railway variables set PRICE_PER_CALL_USDC=0.001
railway variables set BYPASS_PAYMENT=false
echo ""

# Step 6: Generate domain
echo "🌐 Generating public domain..."
railway domain
echo ""

# Step 7: Get deployment URL
echo "✨ Deployment complete!"
echo ""
echo "📊 Getting your deployment URL..."
DOMAIN=$(railway domain 2>&1 | grep -oP 'https://[^\s]+' | head -1)

if [ -n "$DOMAIN" ]; then
    echo ""
    echo "🎉 Your API is live at: $DOMAIN"
    echo ""
    echo "📚 API Documentation: $DOMAIN/docs"
    echo "🏥 Health Check: $DOMAIN/health"
    echo ""
    echo "Test it now:"
    echo "  curl $DOMAIN/health"
else
    echo ""
    echo "⚠️  Run 'railway domain' to see your deployment URL"
fi

echo ""
echo "📝 Next steps:"
echo "  1. Test: python test_api.py $DOMAIN"
echo "  2. View logs: railway logs"
echo "  3. Monitor: railway status"
echo ""
