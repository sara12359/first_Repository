"""
Views for the holidays app.
Fetches holiday data from AbstractAPI Holidays API.
"""
import requests
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings


# Country options for the dropdown
COUNTRIES = [
    ('AF', 'Afghanistan'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AR', 'Argentina'),
    ('AU', 'Australia'), ('AT', 'Austria'), ('BD', 'Bangladesh'), ('BE', 'Belgium'),
    ('BR', 'Brazil'), ('CA', 'Canada'), ('CL', 'Chile'), ('CN', 'China'),
    ('CO', 'Colombia'), ('HR', 'Croatia'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'),
    ('EG', 'Egypt'), ('FI', 'Finland'), ('FR', 'France'), ('DE', 'Germany'),
    ('GR', 'Greece'), ('HK', 'Hong Kong'), ('HU', 'Hungary'), ('IN', 'India'),
    ('ID', 'Indonesia'), ('IE', 'Ireland'), ('IL', 'Israel'), ('IT', 'Italy'),
    ('JP', 'Japan'), ('KE', 'Kenya'), ('KR', 'South Korea'), ('MY', 'Malaysia'),
    ('MX', 'Mexico'), ('NL', 'Netherlands'), ('NZ', 'New Zealand'), ('NG', 'Nigeria'),
    ('NO', 'Norway'), ('PK', 'Pakistan'), ('PH', 'Philippines'), ('PL', 'Poland'),
    ('PT', 'Portugal'), ('RO', 'Romania'), ('RU', 'Russia'), ('SA', 'Saudi Arabia'),
    ('SG', 'Singapore'), ('ZA', 'South Africa'), ('ES', 'Spain'), ('SE', 'Sweden'),
    ('CH', 'Switzerland'), ('TW', 'Taiwan'), ('TH', 'Thailand'), ('TR', 'Turkey'),
    ('UA', 'Ukraine'), ('AE', 'United Arab Emirates'), ('GB', 'United Kingdom'),
    ('US', 'United States'), ('VN', 'Vietnam'),
]


def index(request):
    """Main page with holiday search form."""
    years = list(range(2020, 2031))
    return render(request, 'holidays/index.html', {
        'countries': COUNTRIES,
        'years': years,
    })


def get_holidays(request):
    """Fetch holidays from AbstractAPI with Nager.Date fallback."""
    country = request.GET.get('country', 'US')
    year = request.GET.get('year', '2024')
    
    # Try AbstractAPI first
    try:
        api_key = settings.ABSTRACTAPI_KEY
        url = 'https://holidays.abstractapi.com/v1/'
        params = {
            'api_key': api_key,
            'country': country,
            'year': year,
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        # If AbstractAPI fails (e.g., 402 Payment Required), fallback to Nager.Date
        if response.status_code == 200:
            holidays = response.json()
            formatted_holidays = []
            for holiday in holidays:
                formatted_holidays.append({
                    'name': holiday.get('name', ''),
                    'name_local': holiday.get('name_local', ''),
                    'description': holiday.get('description', ''),
                    'country': holiday.get('country', ''),
                    'location': holiday.get('location', ''),
                    'type': holiday.get('type', ''),
                    'date': holiday.get('date', ''),
                    'date_year': holiday.get('date_year', ''),
                    'date_month': holiday.get('date_month', ''),
                    'date_day': holiday.get('date_day', ''),
                    'week_day': holiday.get('week_day', ''),
                })
            return JsonResponse({'holidays': formatted_holidays, 'success': True, 'source': 'AbstractAPI'})
        
        print(f"AbstractAPI failed with status {response.status_code}. Falling back to Nager.Date.")
    except Exception as e:
        print(f"AbstractAPI error: {e}. Falling back to Nager.Date.")

    # Fallback to Nager.Date
    try:
        fallback_url = f'https://date.nager.at/api/v3/PublicHolidays/{year}/{country}'
        fallback_response = requests.get(fallback_url, timeout=10)
        fallback_response.raise_for_status()
        holidays = fallback_response.json()
        
        formatted_holidays = []
        for holiday in holidays:
            # Nager.Date date format is YYYY-MM-DD
            date_parts = holiday.get('date', '').split('-')
            year_val = date_parts[0] if len(date_parts) > 0 else year
            month_val = date_parts[1] if len(date_parts) > 1 else ''
            day_val = date_parts[2] if len(date_parts) > 2 else ''
            
            formatted_holidays.append({
                'name': holiday.get('name', ''),
                'name_local': holiday.get('localName', ''),
                'description': '', # Nager.Date doesn't provide descriptions
                'country': holiday.get('countryCode', ''),
                'location': '',
                'type': ', '.join(holiday.get('types', [])),
                'date': holiday.get('date', ''),
                'date_year': year_val,
                'date_month': month_val,
                'date_day': day_val,
                'week_day': '', # Will be calculated by frontend or we could calculate here
            })
        
        return JsonResponse({'holidays': formatted_holidays, 'success': True, 'source': 'Nager.Date'})
    
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': f"All API sources failed. Last error: {str(e)}", 'success': False}, status=500)
