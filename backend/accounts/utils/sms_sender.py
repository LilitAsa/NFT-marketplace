import requests

def send_sms(phone, message):
    SMS_API_KEY = "B9367EF1-57CD-9705-D499-753BA9517A80"
    url = "https://sms.ru/sms/send"
    params = {
        "api_id": SMS_API_KEY,
        "to": phone,
        "msg": message,
        "json": 1
    }
    response = requests.get(url, params=params)
    return response.json()