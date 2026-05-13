# wttr-hourly: Weather Skill Project (CWA API Integrated)

This project provides a CLI tool to fetch and parse weather data, optimized for terminal use and LLM consumption. It primarily uses Taiwan's **Central Weather Administration (CWA) API** for locations in Taiwan and falls back to `wttr.in` for international locations.

## Project Structure

- `scripts/cwa.sh`: Main entry point script. Orchestrates geocoding, parameter extraction, and parsing.
- `lib/geocode.py`: Uses OpenStreetMap's Nominatim API to resolve location names.
- `lib/get_cwa_params.py`: Maps geocoded Taiwan addresses to CWA dataset IDs and districts.
- `lib/cwa_parser.py`: Parses Taiwan CWA JSON data into a structured `wttr.in`-style text format.
- `lib/weather_parser.py`: Original parser for `wttr.in` JSON data.
- `data/cwa_dataset_ids.json`: Mapping of Taiwan cities to CWA dataset IDs.
- `.env`: Stores the `CWA_API_KEY`.

## Core Technologies

- **Languages**: Bash, Python 3
- **APIs**:
  - [Taiwan CWA Open Data](https://opendata.cwa.gov.tw/): Primary weather data source for Taiwan.
  - [wttr.in](https://wttr.in/): Fallback weather data source.
  - [OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/): Geocoding service.

## Building and Running

### Prerequisites
- Python 3
- `requests` library: `pip install requests`
- A valid CWA API Key stored in your environment or a `.env` file as `CWA_API_KEY`.

### Execution
```bash
# Get weather for a Taiwan district (using CWA API)
./scripts/cwa.sh "文山區"

# Get a concise summary
./scripts/cwa.sh "信義區" --short

# Get weather for an international city (using wttr.in fallback)
./scripts/cwa.sh "London"
```

## Development Conventions

- **Units**: Strictly uses metric units (Celsius, mm, km/h).
- **Output Format**: Designed to be pure text and easily readable by both humans and LLMs.
- **Piping**: Scripts are designed to work with standard streams (`sys.stdin`, `sys.stdout`).
- **Error Handling**: `lib/geocode.py` writes errors to `stderr` and exits with non-zero codes on failure.

## TODOs
- [ ] Add unit tests for `lib/weather_parser.py`.
- [ ] Handle API rate limits for Nominatim in `lib/geocode.py`.
- [ ] Add a `requirements.txt` file for easier dependency management.
