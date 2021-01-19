import requests
import json
from datetime import datetime
import time
import http.client
import random
import re

global k
k=0


TOKEN="1561527689:AAFhXNjYbdMo2ogv2LmoB5vnGEslFtbQRhM"

url="https://api.telegram.org/bot{}/getUpdates?timeout=100".format(TOKEN)
def telegram(url,offset=None):

	if offset:
		url+="&offset={}".format(offset)
	response=requests.get(url)

	print(url)
	if response.status_code==404:
		print("error")
		return
	
	result=response.content.decode("utf-8")
	get_json=json.loads(result)
	return get_json
	
def last_message(url):
	text=telegram(url)
	n=len(text["result"])
	return text["result"][n-1]


def send_message(text,chat_id):
	send_url="https://api.telegram.org/bot{}/sendMessage?text={}&chat_id={}".format(	TOKEN,text,chat_id)
	telegram(send_url)

def send_photo(photo_url,chat_id,caption=None):


	if caption:	
		send_url="https://api.telegram.org/bot{}/sendPhoto?chat_id={}&photo={}&caption={}".format(
		TOKEN,chat_id,photo_url,caption)

		telegram(send_url)

	else:
		send_url="https://api.telegram.org/bot{}/sendPhoto?chat_id={}&photo={}".format(
		TOKEN,chat_id,photo_url)
		
		telegram(send_url)
	

def last_chat_id(url):
	text=last_message(url)
	return (text['message']['chat']['id'],text["update_id"])

def max_update(url):
	text=telegram(url)
	
	ma=0
	for i in text["result"]:
		ma=max(ma,int(i["update_id"]))
	return ma


def hina():
	response=requests.get("https://api.thecatapi.com/v1/images/search")
	
	cats=response.content.decode("utf-8")
	
	cats=json.loads(cats)
	
	return cats[0]['url']
	

def av(query):
	conn = http.client.HTTPSConnection("adult-movie-provider.p.rapidapi.com")

	headers = {
    	'x-rapidapi-key': "38061515bdmsh784f945bbb7e4ecp1e2628jsn9794ed2b02e1",
    	'x-rapidapi-host': "adult-movie-provider.p.rapidapi.com"
    	}

	url="/api/video/FindVideo?keyword={}&offset=0&next=5".format(query)
	conn.request("GET", url, headers=headers)

	res = conn.getresponse()
	data = res.read()

	data=data.decode("utf-8")

	f=json.loads(data)
	r=random.randint(0,len(f)-1)

	return (f[r]['thumbs'][0],f[r]['embed_url'])

	

def update(p):
	chat_id,date=last_chat_id(url)
	
	if p==(chat_id,date):
		return
	
	text=last_message(url)
	
	text=text["message"]["text"]
	text=text.replace("/","")
	text=text.strip()
	print(text)
	
	if text[:4]=="porn":
		(photo_url,caption)=av(text[5:].strip())
		send_photo(photo_url,chat_id,caption)

	if text[:3]=="uwu":
		photo_url=hina()	
		send_photo(photo_url,chat_id)
	

	
def test():
	f=telegram(url)
	print(f["result"][0])
def main():
	p=last_chat_id(url)
	while True:
		text=telegram(url)	
		if len(text["result"])>0:
			update(p)
			p=last_chat_id(url)

if __name__=="__main__":
	main()







