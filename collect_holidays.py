import requests
import csv
import json
import os
import time

def fetch_holidays(country_code, year):
    """Fetch holidays for a specific country and year using Nager.Date API."""
    url = f"https://date.nager.at/api/v3/PublicHolidays/{year}/{country_code}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch {country_code} for {year}: Status {response.status_code}")
            return []
    except Exception as e:
        print(f"Error fetching {country_code} for {year}: {e}")
        return []

def main():
    # Configuration
    countries = ['US', 'GB', 'CA', 'AU', 'DE', 'FR', 'IN', 'JP', 'BR', 'ZA']
    years = [2023, 2024, 2025]
    
    all_holidays = []
    
    print(f"Starting data collection for {len(countries)} countries and {len(years)} years...")
    
    for year in years:
        for country in countries:
            print(f"Fetching holidays for {country} in {year}...")
            holidays = fetch_holidays(country, year)
            
            for h in holidays:
                # Normalize data
                all_holidays.append({
                    'date': h.get('date'),
                    'local_name': h.get('localName'),
                    'name': h.get('name'),
                    'country_code': h.get('countryCode'),
                    'fixed': h.get('fixed'),
                    'global': h.get('global'),
                    'types': ', '.join(h.get('types', [])),
                    'year': year,
                    'month': h.get('date', '').split('-')[1] if '-' in h.get('date', '') else None
                })
            
            # Be polite to the API
            time.sleep(0.5)
    
    # Save as JSON
    json_path = 'holidays_dataset.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(all_holidays, f, indent=4, ensure_ascii=False)
    print(f"Saved {len(all_holidays)} records to {json_path}")
    
    # Save as CSV
    if all_holidays:
        csv_path = 'holidays_dataset.csv'
        headers = all_holidays[0].keys()
        with open(csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(all_holidays)
        print(f"Saved {len(all_holidays)} records to {csv_path}")

if __name__ == "__main__":
    main()
