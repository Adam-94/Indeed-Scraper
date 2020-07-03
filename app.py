from flask import Flask, render_template, jsonify
from flask import request, send_file, make_response, Response
from bs4 import BeautifulSoup


import requests
import urllib.request

import json
import time
import lxml


app = Flask(__name__)


# COUNTRY LIST
country_urls = {
        "Argentina": "https://ar.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Australia": "https://au.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Austria": "https://at.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Bahrain": "https://bh.indeed.com/jobs?q=Software+Developer&sort=date&l=",
        "Belgium": "https://be.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Brazil": "https://www.indeed.com.br/jobs?q=software+developer&sort=date&l=",
        "Canada": "https://ca.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Chile": "https://www.indeed.cl/jobs?q=software+developer&sort=date&l=",
        "China": "https://cn.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Colombia": "https://co.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Costa Rica": "https://cr.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Czech Republic": "https://cz.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Denmark": "https://dk.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Ecuador": "https://ec.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Egypt": "https://eg.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Finland": "https://www.indeed.fi/jobs?q=software+developer&sort=date&l=",
        "France": "https://www.indeed.fr/jobs?q=software+developer&sort=date&l=",
        "Germany": "https://de.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Greece": "https://gr.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Hong Kong": "https://www.indeed.hk/jobs?q=software+developer&sort=date&l=",
        "Hungary": "https://hu.indeed.com/jobs?q=software+developer&sort=date&l=",
        "India": "https://www.indeed.co.in/jobs?q=software+developer&sort=date&l=",
        "Indonesia": "https://id.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Ireland": "https://ie.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Israel": "https://il.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Italy": "https://it.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Japan": "https://jp.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Kuwait": "https://kw.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Luxembourg": "https://www.indeed.lu/jobs?q=software+developer&sort=date&l=",
        "Malaysia": "https://www.indeed.com.my/jobs?q=software+developer&sort=date&l=",
        "Mexico": "https://www.indeed.com.mx/jobs?q=software+developer&sort=date&l=",
        "Morocco": "https://ma.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Netherlands": "https://www.indeed.nl/jobs?q=software+developer&sort=date&l=",
        "New Zealand": "https://nz.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Nigeria": "https://ng.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Norway": "https://no.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Oman": "https://om.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Pakistan": "https://www.indeed.com.pk/jobs?q=software+developer&sort=date&l=",
        "Panama": "https://pa.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Peru": "https://www.indeed.com.pe/jobs?q=software+developer&sort=date&l=",
        "Philippines": "https://www.indeed.com.ph/jobs?q=software+developer&sort=date&l=",
        "Poland": "https://pl.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Portugal": "https://www.indeed.pt/jobs?q=software+developer&sort=date&l=",
        "Qatar": "https://qa.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Romania": "https://ro.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Russia": "https://ru.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Saudi Arabia": "https://sa.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Singapore": "https://www.indeed.com.sg/jobs?q=software+developer&sort=date&l=",
        "South Africa": "https://www.indeed.co.za/jobs?q=software+developer&sort=date&l=",
        "South Korea": "https://kr.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Spain": "https://www.indeed.es/jobs?q=software+developer&sort=date&l=",
        "Sweden": "https://se.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Switzerland": "https://www.indeed.ch/jobs?q=software+developer&sort=date&l=",
        "Taiwan": "https://tw.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Thailand": "https://th.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Turkey": "https://tr.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Ukraine": "https://ua.indeed.com/jobs?q=software+developer&sort=date&l=",
        "United Arab Emirates": "https://www.indeed.ae/jobs?q=software+developer&sort=date&l=",
        "United Kingdom": "https://www.indeed.co.uk/jobs?q=software+developer&sort=date&l=",
        "United States": "https://www.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Uruguay": "https://uy.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Venezuela": "https://ve.indeed.com/jobs?q=software+developer&sort=date&l=",
        "Vietnam": "https://vn.indeed.com/jobs?q=software+developer&sort=date&l=",
    }




start_time = 0
url_selction = ""
get_url = ""
location = ""
lang_count = []

@app.route('/')
def index():
      return render_template('index.html')

@app.route("/country-list", methods=['POST'])
def country_selection():
    # POST request
    if request.method == 'POST':
        print('Incoming...')
        global get_url
        message = request.get_json()
        location = message
        print(message)

        global url_selction
        for items in country_urls.keys():
            if items in message.values():
                url_selction = country_urls[items]
                print(country_urls[items])
                get_url = url_selction

    return jsonify(get_url)

@app.route("/searchTextField", methods=['POST'])
def get_Search_Location():
    global url_selction
    url_selction = get_url
    # POST request
    if request.method == 'POST':
        print('Incoming...')
        message = request.get_json()
        print(message)

        for key, value in message.items():
            url_selction += str.join('', value)
            url_selction = url_selction.replace(' ', '')
            url_selction += "&radius=25"
            print(url_selction)

        page_count = 0
        link_count = 0
        page_format = "&start=00"
        url_selction += page_format

        links = []
        formatted_links = []
        data = ""
        with requests.session() as session:
            while True:
                page = urllib.request.urlopen(url_selction)
                try:
                    page = urllib.request.urlopen(url_selction)
                except:
                    print("Error: opening page url!")

                page = urllib.request.urlopen(url_selction)
                soup = BeautifulSoup(page, 'lxml')
                page_format += str(page_count)

                divs = soup.find_all('h2', {'class': 'title'})
                for div in divs:
                    for a in div.find_all('a'):
                        formatted_links.append(a['href'])
                        print("URL: ", a['href'])

                if page_count < 100:
                    url_selction = url_selction[:-2]
                elif page_count < 1000:
                    url_selction = url_selction[:-3]
                else:
                    url_selction = url_selction[:-4]

                url_selction += str(page_count)
                page_count += 10
                if page_count == 30:
                    get_Job_data(url_selction, formatted_links)
                    break

                print(page_count)
    return jsonify(message)

def get_Job_data(url, link=[]):
    link_count = 0
    titles = []
    formatted_Titles = []

    languages = {
    "JavaScript": 0,
    "Python": 0,
    "Java": 0,
    "Golang": 0,
    "C++": 0,
    "Ruby": 0,
    "PHP": 0,
    "C#": 0,
    "Scala": 0,
    "Rust": 0,
    "Swift": 0,
    "Node.js": 0,
    "React": 0,
}

    global start_time
    start_time = time.time()
    while True:
                page = urllib.request.urlopen(url)
                try:
                    page = urllib.request.urlopen(url)
                except:
                    print("Error: opening page url!")

                soup = BeautifulSoup(page, 'lxml')
                if link_count == len(link):
                    print("iterated through list!")
                    break

                url = get_url
                data = get_url[:-39]
                data += link[link_count]
                url = data

                print(url)

                divs = soup.find_all("div", {"id": "jobDescriptionText"})
                for div in divs:
                    for txt in div.find_all('div'):
                        contents = txt.text
                        titles.append(contents)

                data = ""
                link_count += 1

    for items in languages.keys():
        for s in titles:
            if str(items) in s:
                    languages[items] += 1

    global lang_count
    lang_count = []
    for items in languages.values():
            lang_count.append(items)

@app.route('/live-chart')
def live_chart():
    global lang_count

    print(lang_count)
    data = lang_count
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True, threaded=True)