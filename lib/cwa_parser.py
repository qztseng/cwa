#!/usr/bin/env python3
import json
import sys
import argparse
from datetime import datetime

def parse_cwa_weather(data, short=False, days=3):
    output = []
    
    try:
        locations = data['records']['Locations'][0]['Location']
    except (KeyError, IndexError):
        return "Error: Invalid CWA JSON structure"

    for loc in locations:
        loc_name = loc['LocationName']
        lat = loc['Latitude']
        lon = loc['Longitude']
        output.append(f"Weather Forecast for: {loc_name} ({lat}, {lon})")

        elements = {e['ElementName']: e['Time'] for e in loc['WeatherElement']}
        
        # Elements mapping
        temp_list = elements.get('溫度', [])
        apparent_temp_list = elements.get('體感溫度', [])
        humidity_list = elements.get('相對濕度', [])
        wind_speed_list = elements.get('風速', [])
        wind_dir_list = elements.get('風向', [])
        rain_prob_list = elements.get('3小時降雨機率', [])
        weather_list = elements.get('天氣現象', [])
        
        # Group by date
        forecast_by_date = {}
        
        # Wind direction mapping
        wind_dir_map = {
            "北風": "N", "東北風": "NE", "東風": "E", "東南風": "SE",
            "南風": "S", "西南風": "SW", "西風": "W", "西北風": "NW",
            "偏北風": "N", "偏東北風": "NE", "偏東風": "E", "偏東南風": "SE",
            "偏南風": "S", "偏西南風": "SW", "偏西風": "W", "偏西北風": "NW",
            "靜風": "Calm"
        }

        # We'll use Temperature (溫度) as the primary time reference
        for t in temp_list:
            dt_str = t['DataTime']
            dt = datetime.fromisoformat(dt_str)
            date_key = dt.date().isoformat()
            
            if date_key not in forecast_by_date:
                forecast_by_date[date_key] = []
            
            w_dir_cn = next((e['ElementValue'][0]['WindDirection'] for e in wind_dir_list if e.get('DataTime') == dt_str), "N/A")
            w_dir_en = wind_dir_map.get(w_dir_cn, w_dir_cn)

            # Find matching values for other elements at this DataTime
            hour_data = {
                'time': dt,
                'temp': t['ElementValue'][0]['Temperature'],
                'feels_like': next((e['ElementValue'][0]['ApparentTemperature'] for e in apparent_temp_list if e.get('DataTime') == dt_str), "N/A"),
                'humidity': next((e['ElementValue'][0]['RelativeHumidity'] for e in humidity_list if e.get('DataTime') == dt_str), "N/A"),
                'wind_speed': next((e['ElementValue'][0]['WindSpeed'] for e in wind_speed_list if e.get('DataTime') == dt_str), "N/A"),
                'wind_dir': w_dir_en,
                # Rain probability is often 3-hourly, so we find the one that covers this time
                'rain_prob': next((e['ElementValue'][0]['ProbabilityOfPrecipitation'] for e in rain_prob_list if e.get('StartTime') <= dt_str < e.get('EndTime')), "0"),
                'weather': next((e['ElementValue'][0]['Weather'] for e in weather_list if e.get('StartTime') <= dt_str < e.get('EndTime')), "N/A")
            }
            forecast_by_date[date_key].append(hour_data)

        # Output formatting
        sorted_dates = sorted(forecast_by_date.keys())
        
        # Current Condition (using first available point)
        if not short and sorted_dates:
            first_day = forecast_by_date[sorted_dates[0]]
            if first_day:
                curr = first_day[0]
                output.append(f"Current Condition: {curr['temp']}°C (Feels Like {curr['feels_like']}°C), {curr['weather']}, Hum: {curr['humidity']}%")

        days_processed = 0
        
        for date in sorted_dates:
            if days_processed >= (1 if short else days):
                break
            
            output.append(f"\nDate: {date}")
            
            # Target times for wttr-like 3-hour intervals: 0, 3, 6, 9, 12, 15, 18, 21
            target_hours = [0, 3, 6, 9, 12, 15, 18, 21]
            if short:
                target_hours = [9, 15, 18]
                
            for hour_data in forecast_by_date[date]:
                h = hour_data['time'].hour
                if h not in target_hours:
                    continue
                
                display_time = f"{h:02d}:00"
                temp = hour_data['temp']
                rain = hour_data['rain_prob']
                desc = hour_data['weather']
                
                line = f"  {display_time}: {temp}°C, {rain}% rain, {desc}"
                
                if not short:
                    feels = hour_data['feels_like']
                    hum = hour_data['humidity']
                    # Convert m/s to km/h (CWA wind speed is typically m/s)
                    try:
                        wind_kmh = round(float(hour_data['wind_speed']) * 3.6)
                    except ValueError:
                        wind_kmh = hour_data['wind_speed']
                    
                    line += f", FeelsLike: {feels}°C, Humidity: {hum}%, Wind: {wind_kmh}km/h {hour_data['wind_dir']}"
                
                output.append(line)
            
            days_processed += 1
            
    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Parse CWA JSON weather data.")
    parser.add_argument("--short", action="store_true", help="Return concise summary (9:00, 15:00, 18:00 today only)")
    parser.add_argument("--days", "-d", type=int, default=3, help="Number of days to include (default: 3)")
    parser.add_argument("file", nargs="?", type=argparse.FileType("r"), default=sys.stdin)
    
    args = parser.parse_args()
    
    try:
        data = json.load(args.file)
        print(parse_cwa_weather(data, short=args.short, days=args.days))
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
