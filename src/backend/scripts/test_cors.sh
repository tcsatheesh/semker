#!/bin/bash

# CORS Configuration Test Script
# Tests CORS headers for the Semker API

echo "🧪 Testing CORS Configuration for Semker API"
echo "=============================================="

API_URL="http://localhost:8000"
FRONTEND_ORIGIN="http://localhost:3000"

echo ""
echo "1. Testing preflight request (OPTIONS)..."
echo "-------------------------------------------"

PREFLIGHT_RESPONSE=$(curl -s -I \
  -H "Origin: $FRONTEND_ORIGIN" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -X OPTIONS \
  "$API_URL/messages")

if echo "$PREFLIGHT_RESPONSE" | grep -i "access-control-allow-origin" > /dev/null; then
    echo "✅ CORS preflight: PASSED"
    echo "   - Origin allowed: $(echo "$PREFLIGHT_RESPONSE" | grep -i "access-control-allow-origin" | cut -d' ' -f2- | tr -d '\r')"
    echo "   - Methods allowed: $(echo "$PREFLIGHT_RESPONSE" | grep -i "access-control-allow-methods" | cut -d' ' -f2- | tr -d '\r')"
    echo "   - Headers allowed: $(echo "$PREFLIGHT_RESPONSE" | grep -i "access-control-allow-headers" | cut -d' ' -f2- | tr -d '\r')"
else
    echo "❌ CORS preflight: FAILED"
    echo "   No CORS headers found"
fi

echo ""
echo "2. Testing actual POST request..."
echo "--------------------------------"

POST_RESPONSE=$(curl -s -w "\n%{http_code}" \
  -H "Origin: $FRONTEND_ORIGIN" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{"message":"CORS test message"}' \
  "$API_URL/messages")

HTTP_CODE=$(echo "$POST_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$POST_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "201" ]; then
    echo "✅ POST request: PASSED"
    echo "   - HTTP Status: $HTTP_CODE"
    echo "   - Response: $RESPONSE_BODY"
else
    echo "❌ POST request: FAILED"
    echo "   - HTTP Status: $HTTP_CODE"
    echo "   - Response: $RESPONSE_BODY"
fi

echo ""
echo "3. Testing GET request..."
echo "------------------------"

GET_RESPONSE=$(curl -s -w "\n%{http_code}" \
  -H "Origin: $FRONTEND_ORIGIN" \
  "$API_URL/health")

HTTP_CODE=$(echo "$GET_RESPONSE" | tail -n1)
RESPONSE_BODY=$(echo "$GET_RESPONSE" | head -n -1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ GET request: PASSED"
    echo "   - HTTP Status: $HTTP_CODE"
    echo "   - Backend status: $(echo "$RESPONSE_BODY" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)"
else
    echo "❌ GET request: FAILED"
    echo "   - HTTP Status: $HTTP_CODE"
    echo "   - Response: $RESPONSE_BODY"
fi

echo ""
echo "🎉 CORS testing complete!"
echo ""
echo "Configuration can be customized via environment variables:"
echo "  - CORS_ORIGINS (current default: http://localhost:3000,http://127.0.0.1:3000)"
echo "  - CORS_ALLOW_CREDENTIALS (current default: true)"
echo "  - CORS_ALLOW_METHODS (current default: *)"
echo "  - CORS_ALLOW_HEADERS (current default: *)"
echo ""
echo "See .env.example for full configuration options."
