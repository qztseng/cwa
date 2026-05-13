# CWA Weather Skill

Taiwan Central Weather Administration (CWA) API integration for high-resolution weather data, with global fallback via `wttr.in`.

## Quick Start

1.  **Get a CWA API Key:** Register at the [CWA Open Data Platform](https://opendata.cwa.gov.tw/).
2.  **Set Environment Variable:**
    ```bash
    export CWA_API_KEY=your_api_key_here
    ```
    Alternatively, create a `.env` file in the root directory.
3.  **Run:**
    ```bash
    ./scripts/cwa.sh "Taipei"
    ```

## Documentation

See [GEMINI.md](GEMINI.md) for detailed project structure, conventions, and technical details.
See [SKILL.md](SKILL.md) for skill-specific tool definitions.

## License
MIT (or as specified in the repository)
