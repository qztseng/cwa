#!/usr/bin/env python3
import json
import sys
import argparse

def parse_weather(data, short=False, location_name=None, days=3):
    output = []
    
    # Header Info
    area = data['nearest_area'][0]
    if location_name:
        display_location = location_name
    else:
        display_location = f"{area['areaName'][0]['value']}, {area['country'][0]['value']}"
    
    # Only append coordinates if not already present in display_location
    if "[" not in display_location and "(" not in display_location:
        coords = f"({area['latitude']}, {area['longitude']})"
        output.append(f"Weather Forecast for: {display_location} {coords}")
    else:
        output.append(f"Weather Forecast for: {display_location}")

    # In full mode (default), show current condition
    if not short:
        current = data['current_condition'][0]
        output.append(f"Current Condition: {current['temp_C']}°C (Feels Like {current['FeelsLikeC']}°C), {current['weatherDesc'][0]['value']}, UV: {current['uvIndex']}, Vis: {current['visibility']}km")
    
    # Process requested number of days
    # short mode always limits to 1 day
    max_days = 1 if short else days
    days_to_process = data['weather'][:max_days]
    
    for day in days_to_process:
        date = day['date']
        output.append(f"\nDate: {date}")
        
        if not short:
            astro = day['astronomy'][0]
            output.append(f"  Moon: {astro['moon_phase']} ({astro['moon_illumination']}% illumination)")
            output.append(f"  Astronomy: Sunrise {astro['sunrise']}, Sunset {astro['sunset']}")

        # Target times: 9:00 (900), 15:00 (1500), 18:00 (1800)
        target_times = ["900", "1500", "1800"]
        
        hourly_data = day['hourly']
        for hour in hourly_data:
            time_str = hour['time']
            if short and time_str not in target_times:
                continue
                
            display_time = f"{int(time_str)//100:02d}:00"
            temp = hour['tempC']
            precip = hour['precipMM']
            desc = hour['weatherDesc'][0]['value']
            
            line = f"  {display_time}: {temp}°C, {precip}mm, {desc}"
            
            # If not short, add all metrics
            if not short:
                line += f", FeelsLike: {hour['FeelsLikeC']}°C, Humidity: {hour['humidity']}%, Wind: {hour['windspeedKmph']}km/h {hour['winddir16Point']}, UV: {hour['uvIndex']}, Vis: {hour['visibility']}km, Rain: {hour['chanceofrain']}%"
                
            output.append(line)
            
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Parse wttr.in JSON weather data.")
    parser.add_argument("--short", action="store_true", help="Return concise summary (9:00, 15:00, 18:00 today only)")
    parser.add_argument("--days", "-d", type=int, default=3, choices=[1, 2, 3], help="Number of days to include (1-3, default: 3)")
    parser.add_argument("--location_name", help="Override the location name in header")
    parser.add_argument("file", nargs="?", type=argparse.FileType("r"), default=sys.stdin)
    
    args = parser.parse_args()
    
    try:
        data = json.load(args.file)
        print(parse_weather(data, short=args.short, location_name=args.location_name, days=args.days))
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
