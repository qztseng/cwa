#!/bin/bash
# Usage: ./cwa.sh [location] [options]

# API Key handling
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LIB_DIR="$BASE_DIR/lib"

# Load local .env as fallback if key is not already in environment
if [ -z "$CWA_API_KEY" ] && [ -f "$BASE_DIR/.env" ]; then
    export $(grep -v '^#' "$BASE_DIR/.env" | xargs)
fi

if [ -z "$CWA_API_KEY" ]; then
    echo "Error: CWA_API_KEY not found. Please set it in your environment or a .env file."
    exit 1
fi

LOCATION="${1:-臺北市}"
shift # Remove location from arguments

# Resolve location
GEO_RESULT=$("$LIB_DIR/geocode.py" "$LOCATION" 2>/dev/null)

if [ -n "$GEO_RESULT" ]; then
    CWA_PARAMS=$("$LIB_DIR/get_cwa_params.py" "$GEO_RESULT")
    
    if [ -n "$CWA_PARAMS" ]; then
        DATASET_ID=$(echo "$CWA_PARAMS" | cut -d'|' -f1)
        LOCATION_NAME=$(echo "$CWA_PARAMS" | cut -d'|' -f2)
        
        API_URL="https://opendata.cwa.gov.tw/api/v1/rest/datastore/${DATASET_ID}?Authorization=${CWA_API_KEY}"
        
        if [ -n "$LOCATION_NAME" ]; then
            ENCODED_LOCATION=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$LOCATION_NAME'))")
            API_URL="${API_URL}&LocationName=${ENCODED_LOCATION}"
        fi
        
        # Fetch from CWA
        curl -s -X 'GET' "$API_URL" -H 'accept: application/json' | python3 "$LIB_DIR/cwa_parser.py" "$@"
    else
        # Fallback to wttr.in for non-Taiwan locations
        echo "Location not in Taiwan or mapping not found. Falling back to wttr.in..." >&2
        QUERY_LOCATION=$(echo "$GEO_RESULT" | cut -d'|' -f1)
        curl -s "wttr.in/${QUERY_LOCATION}?format=j1" | python3 "$LIB_DIR/weather_parser.py" "$@"
    fi
else
    # Total fallback if geocoding failed
    curl -s "wttr.in/${LOCATION}?format=j1" | python3 "$LIB_DIR/weather_parser.py" "$@"
fi
