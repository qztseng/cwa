#!/usr/bin/env python3
import json
import sys
import os

def get_params(geo_result):
    try:
        # geo_result format: lat,lon|Address
        parts = geo_result.split('|')
        if len(parts) < 2:
            return None
        
        address = parts[1]
        address_parts = [p.strip() for p in address.split(',')]
        
        # Load dataset IDs
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir, '..', 'data', 'cwa_dataset_ids.json')
        with open(data_path, 'r', encoding='utf-8') as f:
            dataset_ids = json.load(f)
        
        # Look for city and district
        # Address format is usually: District, City, Country
        # But it can vary. We'll search for keys in dataset_ids.
        
        city = None
        dataset_id = None
        district = None
        
        for part in address_parts:
            # Handle variations like Taipei City vs 臺北市
            # But the geocoder seems to return Chinese for Taiwan locations
            if part in dataset_ids:
                city = part
                dataset_id = dataset_ids[part]
                break
        
        if not city:
            # Fallback to Taipei City if not found? No, better to fail or use a default.
            # Let's try to match "Taipei City" to "臺北市"
            mapping = {
                "Taipei City": "臺北市",
                "New Taipei City": "新北市",
                "Taoyuan City": "桃園市",
                "Taichung City": "臺中市",
                "Tainan City": "臺南市",
                "Kaohsiung City": "高雄市"
            }
            for part in address_parts:
                if part in mapping:
                    city = mapping[part]
                    dataset_id = dataset_ids[city]
                    break
        
        if dataset_id:
            # The first part is often the district
            district = address_parts[0]
            # If the district is actually the city or country, clear it
            if district == city or district == "臺灣" or district == "Taiwan":
                district = ""
            
            return f"{dataset_id}|{district}"
            
        return None
    except Exception as e:
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(1)
    
    result = get_params(sys.argv[1])
    if result:
        print(result)
    else:
        sys.exit(1)
