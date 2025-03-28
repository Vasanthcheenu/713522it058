import requests
from django.http import JsonResponse
from django.conf import settings
from .models import StoredNumber
from django.utils.timezone import now
from threading import Thread
import time

API_URLS = {
    'p': "https://api.prime-numbers.io/random",
    'f': "https://api.math.tools/numbers/fibonacci/random",
    'e': "https://api.math.tools/numbers/even/random",
    'r': "https://api.random.org/json-rpc/4/invoke"
}
TIMEOUT = 0.5  
WINDOW_SIZE = 10  

def fetch_number(qualification):
    url = API_URLS.get(qualification)
    if not url:
        return None
    
    try:
        response = requests.get(url, timeout=TIMEOUT)
        if response.status_code == 200:
            data = response.json()
            return data.get("number")  # API should return {'number': X}
    except requests.exceptions.RequestException:
        return None

def store_number(number):
    if not StoredNumber.objects.filter(value=number).exists():
        StoredNumber.objects.create(value=number)
    
    # Enforce sliding window size
    if StoredNumber.objects.count() > WINDOW_SIZE:
        oldest = StoredNumber.objects.order_by("created_at").first()
        if oldest:
            oldest.delete()

def get_stored_numbers():
   
    return list(StoredNumber.objects.values_list("value", flat=True))

def number_api(request, qualification):
    
    if qualification not in API_URLS:
        return JsonResponse({"error": "Invalid qualification"}, status=400)

    prev_state = get_stored_numbers() 
    num = fetch_number(qualification)

    if num is not None:
        store_number(num)

    curr_state = get_stored_numbers()  

    avg = round(sum(curr_state) / len(curr_state), 2) if curr_state else 0

    return JsonResponse({
        "windowPrevState": prev_state,
        "windowCurrState": curr_state,
        "numbers": [num] if num is not None else [],
        "avg": avg
    })
