---
name: cwa-weather
description: Get detailed weather forecasts for Taiwan (via CWA) and worldwide (via wttr.in fallback).
tools:
  - name: cwa
    description: Fetches and parses weather data for a location. Optimized for Taiwan districts.
    arguments:
      location:
        type: string
        description: District name (e.g., '文山區'), City, or international location.
      options:
        type: string
        description: Use '--short' for a concise summary, or '-d [1-3]' for forecast days.
---

# CWA Weather Skill (Taiwan & Global)

Get high-resolution weather information for Taiwan directly from the Central Weather Administration (CWA) and worldwide weather from `wttr.in`.

## Features
- **Taiwan-Specific Data**: Fetches precise district-level data for Taiwan using the CWA Open Data API.
- **Global Fallback**: Automatically switches to `wttr.in` for international locations.
- **AI-Optimized Output**: Returns clean, structured text designed for LLM analysis or terminal viewing.
- **Metric by Default**: Temperature in Celsius, wind in km/h, rain in mm.

## Usage

### Taiwan District Forecast
```bash
./scripts/cwa.sh "文山區"
```

### Concise Today Summary
```bash
./scripts/cwa.sh "信義區" --short
```

### International Forecast
```bash
./scripts/cwa.sh "London"
```

## Setup
1. Ensure you have an API key from the [CWA Open Data Platform](https://opendata.cwa.gov.tw/).
2. Set the `CWA_API_KEY` environment variable in your system or your agent's configuration.
3. (Optional) Create a `.env` file in the root directory:
   ```env
   CWA_API_KEY=your_api_key_here
   ```
4. Install dependencies: `pip install requests`.

## Folder Structure
- `scripts/cwa.sh`: Main entry script.
- `lib/`: Python logic for geocoding, parameter mapping, and parsing.
- `data/`: Reference data (dataset IDs).
- `.env`: API credentials.
