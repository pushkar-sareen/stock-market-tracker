import requests
from twilio.rest import Client


account_sid = 'kindly use your own sid'
auth_token = 'kindly use your own auth token'
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = 'kindly use your oen api key'
STOCK_ENDPOINT = (f"https://www.alphavantage.co/query/{STOCK_API_KEY}")


NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
GET_NEWS_API = 'kindly use your own api'

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(url= STOCK_ENDPOINT, params= stock_params)
data = response.json()['Time Series (Daily)']
data_list = [(key, value) for (key, value)  in data.items()]
yesterday_data= data_list[0]
yesterday_closing_price = float(yesterday_data[1]['4. close'])

day_before_yesterday = yesterday_data= data_list[1]
day_before_yesterday_closing_price = float(day_before_yesterday[1]['4. close'])
difference_between_stocks = day_before_yesterday_closing_price - yesterday_closing_price

# updown = None

if difference_between_stocks > 0:
    updown = "🔺"
else:
    updown = "🔻"


percentage_change = (difference_between_stocks / day_before_yesterday_closing_price) * 100
change_percentage = int(percentage_change)
if abs(change_percentage) > 4:
    news_params = {
        'q': 'TSLA'
    }
    headers = {
        'Authorization': GET_NEWS_API
    }
    data = requests.get(url=NEWS_ENDPOINT, headers=headers, params= news_params)
    news_data = data.json()['articles']
    news_titles = news_data[:3]
    formatted_articles = [f"{STOCK_NAME}: {updown} {change_percentage}%\nHeadline: {article['title']}.\nBrief: {article['description']} " for article in news_titles]
    print(formatted_articles)


    for article in formatted_articles:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            from_='kindly get number from twilio',
            body= article,
            to= 'kindly use your own number'
        )
        print(message.status)