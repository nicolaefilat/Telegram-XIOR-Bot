import json

import requests

url_post = "https://www.xior-booking.com/ajax/space-search"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-CSRF-TOKEN": "96TzZywH4bFUOiIWwJIZD8Vsr5HLliEVMAYFaFY0",
    "X-Requested-With": "XMLHttpRequest",
    "Alt-Used": "www.xior-booking.com",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "Cookie": "XSRF-TOKEN=eyJpdiI6IjVheFBla3JmM2QxaHFmaUlnWk8rUEE9PSIsInZhbHVlIjoieWl3WWRyL0F6SlVaakg0QnF5RVJZSTJsclM2MEVtWGJzR2JCT01QbVBqckJxRWlKM0VVV3R0TU9VWkV1bWwwZE5GTHd4N3dBSEhtUW1JMzBKZGhKaXo0T2xaTGpza2hMbUR1dFRZNDdHcFBLVHJMbDRRZnZ0UWRidUFLTlcycmIiLCJtYWMiOiIyNzhlZDhhMjBlZGE1ZDNjNGM1N2MxNDdmYWZmOWRmNzIwMTE4ZDE3ZDEwMGIxYjgzY2NmNmZjZGMyNDJiZTlkIn0%3D; laravel_session=eyJpdiI6IkkvUlhzTWV2NGZRV2k0NGRnaEQxV2c9PSIsInZhbHVlIjoiQzJJWEt6NmY0cFI4RVdBaGZWek1vcERjeWZsT25uVlAzTUM3M2JaYXNNRDc4OFpVSisvcDRhMVRVSjF1QjV0Z1dTek9vczREVEh4YTRWQ01pNW1xOW9ZWk5sSnhsVktDZzd4SWpOdW1rQ2NBazhmSzBDKzhSbVJJMWtMaDRBMkYiLCJtYWMiOiJhYThiZDE2YTJmNzY4YzhkMTQ0MDgwM2YwODhlOWQ1MWJkN2NhNjczZjliYTE0N2E1ZGNiNDQyYWRiOTE3NjEzIn0%3D"
}
city = "Delft"
data_delft = "country=528&city=21&location=&space_type=&min_price=0&max_price=1838&min_surface=10&max_surface=116&order=&unlock_key=&page=1&pagination=true"
working_data = "country=56&city=&location=&space_type=&min_price=0&max_price=1838&min_surface=10&max_surface=116&order=&unlock_key=&page=1&pagination=false"


def get_results(data_to_post):
    response = requests.post(url_post, data_to_post, headers=headers)
    elements = json.loads(response.content)

    results = []
    for space in elements['spaces']:
        results.append(f"{space['city']} price: {space['price']}")
    return results


def get_delft():
    return get_results(data_delft)


def get_working_data():
    return get_results(working_data)


