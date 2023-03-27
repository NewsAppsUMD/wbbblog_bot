import os
from datetime import datetime, timedelta
from dateutil.parser import parse
from dateutil import tz
import pytz
import requests
from bs4 import BeautifulSoup

from slack import WebClient
from slack.errors import SlackApiError

slack_token = os.environ.get('SLACK_API_TOKEN')
client = WebClient(token=slack_token)

# set the timezone to Eastern
eastern = pytz.timezone("US/Eastern")
tzinfos = {"EST": tz.gettz("US/Eastern")}

def last_updated(soup):
    return soup.find('meta', {'property': 'article:modified_time'}).get('content')

def soupify(url):
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    if response.status_code == 429:
      time.sleep(int(response.headers["Retry-After"]))
      r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    return BeautifulSoup(r.text, "html.parser") 

def coaching_changes():
    # the json url for that page
    url = "https://wbbblog.com/wp-json/wp/v2/posts/33126"
    # grab the url with requests and save the json
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    json = r.json()
    # setup current time with timezone
    now_utc = datetime.now(pytz.utc)
    now_eastern = now_utc.astimezone(eastern)
    # check to see if the page's last modified time is greater than (most recent) an hour ago
    if eastern.localize(parse(json['modified'], tzinfos=tzinfos)) > now_eastern - timedelta(hours=1):
        msg = "WBBBlog has updated its coaching changes page, see https://wbbblog.com/womens-basketball-coaching-changes-tracker-2023/"
        try:
            response = client.chat_postMessage(
                channel="slack-bots",
                text=msg,
                unfurl_links=True, 
                unfurl_media=True
            )
            print("success!")
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")

def transfers():
    url = "https://wbbblog.com/wp-json/wp/v2/posts/30448"
    r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    json = r.json()
    now_utc = datetime.now(pytz.utc)
    now_eastern = now_utc.astimezone(eastern)
    if eastern.localize(parse(json['modified'], tzinfos=tzinfos)) > now_eastern - timedelta(hours=1):
        msg = "WBBBlog has updated its transfers page, see https://wbbblog.com/womens-basketball-transfers-d-i-2022-23/"
        try:
            response = client.chat_postMessage(
                channel="slack-bots",
                text=msg,
                unfurl_links=True, 
                unfurl_media=True
            )
            print("success!")
        except SlackApiError as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            print(f"Got an error: {e.response['error']}")

if __name__ == "__main__":
    coaching_changes()
    transfers()