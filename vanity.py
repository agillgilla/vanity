import requests
from bs4 import BeautifulSoup
from enum import Enum

class PlateResult(Enum):
    available = 1
    taken = 2
    invalid_info = 3

URL_INIT = 'http://www.dmv.ca.gov/wasapp/ipp2/initPers.do'
URL_START = 'http://www.dmv.ca.gov/wasapp/ipp2/startPers.do'
URL_AUTH = 'http://www.dmv.ca.gov/wasapp/ipp2/processPers.do'
URL_CHECK = 'http://www.dmv.ca.gov/wasapp/ipp2/processConfigPlate.do'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'

def check_plate(curr_plate, curr_vin, plate_name):
    plate_length = len(plate_name)

    session = requests.Session()

    headers = {
        'authority': 'www.dmv.ca.gov',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': USER_AGENT,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'en-US,en;q=0.9'
    }

    response = session.get(URL_INIT, headers=headers)

    headers = {
        'authority': 'www.dmv.ca.gov',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://www.dmv.ca.gov',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': USER_AGENT,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.dmv.ca.gov/wasapp/ipp2/initPers.do',
        'accept-language': 'en-US,en;q=0.9'
    }

    data = {
      'acknowledged': 'true',
      '_acknowledged': 'on'
    }

    response = session.post(URL_START, headers=headers, data=data)

    headers = {
        'authority': 'www.dmv.ca.gov',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://www.dmv.ca.gov',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': USER_AGENT,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.dmv.ca.gov/wasapp/ipp2/startPers.do',
        'accept-language': 'en-US,en;q=0.9'
    }

    data = {
      'imageSelected': 'none',
      'vehicleType': 'AUTO',
      'licPlateReplaced': curr_plate,
      'last3Vin': curr_vin,
      'isRegExpire60': 'no',
      'isVehLeased': 'no',
      'plateType': 'Z'
    }

    response = session.post(URL_AUTH, headers=headers, data=data)

    #print(response.text)

    if ('you have entered are invalid' in response.text):
        return PlateResult.invalid_info

    headers = {
        'authority': 'www.dmv.ca.gov',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://www.dmv.ca.gov',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': USER_AGENT,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.dmv.ca.gov/wasapp/ipp2/processPers.do',
        'accept-language': 'en-US,en;q=0.9'
    }

    data = {
      'kidsPlate': '',
      'plateType': 'Z',
      'plateLength': plate_length,
      'plateNameLow': '1960 legacy'
    }

    for i in range(plate_length):
    	plate_char = plate_name[i]
    	data['plateChar' + str(i)] = plate_char

    response = session.post(URL_CHECK, headers=headers, data=data)

    soup = BeautifulSoup(response.text, features="html.parser")

    alert_divs = soup.find_all("div", {"class": "alert__content"})

    if len(alert_divs) > 0:
        return PlateResult.taken
    else:
        return PlateResult.available
