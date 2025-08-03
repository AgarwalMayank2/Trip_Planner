import requests
from datetime import datetime, timedelta

dest_url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchDestination"
hotels_url = "https://booking-com15.p.rapidapi.com/api/v1/hotels/searchHotels"
headers = {
    "x-rapidapi-key": "95923f6703mshe85e7e3776a3598p1d1af4jsn5a5112002170",
    "x-rapidapi-host": "booking-com15.p.rapidapi.com"
}

def search_hotels(cities_list, arrival_date):
    date_obj = datetime.strptime(arrival_date, "%Y-%m-%d")
    next_day = date_obj + timedelta(days = 1)
    departure_date = next_day.strptime("%Y-%m-%d")
    hotels = {}
    for city in cities_list:

        querystring = {"query":city}
        response = requests.get(dest_url, headers=headers, params=querystring)
        data = response.json()
        for element in data['data']:
            if element["search_type"] == "city":
                dest_id = element['dest_id']
                break

        querystring = {
            "dest_id": dest_id,
            "search_type": "city",
            "arrival_date": arrival_date,
            "departure_date": departure_date,
            "adults": "1",
            "room_qty": "1",
            "page_number": "1",
            "price_min": "10",
            "price_max": "500",
            "currency_code": "INR",
            "languagecode": "en-us"
        }
        response = requests.get(hotels_url, headers=headers, params=querystring)
        hotel_data = response.json()['data']['hotels']
        hotel_info = {}
        for hotel in hotel_data:
            hotel_info["name"] = hotel['property']['name']
            hotel_info["reviewScoreWord"] = hotel['property']['reviewScoreWord']
            hotel_info["reviewScore"] = hotel['property']['reviewScore']
            hotel_info["rate"] = hotel['property']['priceBreakdown']['grossPrice']['value'] + ' ' + hotel['property']['currency']
            hotel_info["checkIn_Time"] = hotel['property']['checkin']['fromTime'] + " to " + hotel['property']['checkin']['untilTime']
            hotel_info["checkOut_Time"] = hotel['property']['checkout']['fromTime'] + " to " + hotel['property']['checkout']['untilTime']

        hotels["city"] = hotel_info

    return hotels