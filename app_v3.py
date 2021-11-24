import re

import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
prefs = {
    'profile.default_content_setting_values': {'cookies': 2, 'images': 2, 'plugins': 2, 'popups': 2, 'geolocation': 2,
                                               'notifications': 2, 'auto_select_certificate': 2, 'fullscreen': 2,
                                               'mouselock': 2, 'mixed_script': 2, 'media_stream': 2,
                                               'media_stream_mic': 2, 'media_stream_camera': 2, 'protocol_handlers': 2,
                                               'ppapi_broker': 2, 'automatic_downloads': 2, 'midi_sysex': 2,
                                               'push_messaging': 2, 'ssl_cert_decisions': 2,
                                               'metro_switch_to_desktop': 2, 'protected_media_identifier': 2,
                                               'app_banner': 2, 'site_engagement': 2, 'durable_storage': 2}}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=options)
driver.get("https://soongguri.com/main.php?mkey=2&w=3&l=1")


@app.route('/food', methods=['GET', 'POST'])
def food_func():
    # req = request.get_json()

    url = "https://soongguri.com/main.php?mkey=2&w=3&l=1"
    res = requests.get(url)

    soup = BeautifulSoup(res.content.decode('utf-8', 'replace'), "html.parser")

    data = soup.find("div", attrs={"class": "detail_center"})

    table = data.find("table")

    trs = table.find_all("tr")
    dodam_trs = trs[14]

    qkq = dodam_trs.find("b")

    print(qkq)

    dodam = "[오늘의 도담식당 메뉴] : \n" + test(qkq)

    answer = dodam
    print(answer)

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "simpleText": {
                        "text": answer
                    }
                }
            ],
            'quickReplies': [
                {
                    'label': '🏠',
                    'action': 'message',
                    'messageText': '🏠'
                }
            ]
        }
    }
    return jsonify(res)


def test(s):
    tokens = "" + str(s)
    hangul = re.compile('[^ ㄱ-ㅣ가-힣+]')
    result = hangul.sub('', tokens)
    return result


@app.route('/notice', methods=['GET', 'POST'])
def notice_func():
    req = request.get_json()

    url = "https://scatch.ssu.ac.kr/%ea%b3%b5%ec%a7%80%ec%82%ac%ed%95%ad/page/1/"
    res = requests.get(url)
    res.raise_for_status()

    soup = BeautifulSoup(res.text)

    notices = soup.find_all("a", attrs={"class": "text-decoration-none d-block text-truncate"})
    answer_cal = []
    answer_link = []
    for n in notices:
        calums = n.find("span", attrs={"class": "d-inline-blcok m-pt-5"})
        link = "https://scatch.ssu.ac.kr/" + n["href"]
        answer_cal.append(calums.text)
        answer_link.append(link)

    res = {
        "version": "2.0",
        "template": {
            "outputs": [
                {
                    "carousel": {
                        "type": "basicCard",
                        "items": [
                            {
                                "title": answer_cal[0],
                                "description": "",
                                "thumbnail": {
                                    "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                                },
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "보러가기",
                                        "webLinkUrl": answer_link[0]
                                    },
                                    {
                                        "action": "webLink",
                                        "label": "홈페이지로 가기",
                                        "webLinkUrl": "https://scatch.ssu.ac.kr/%ea%b3%b5%ec%a7%80%ec%82%ac%ed%95%ad/page/1/"
                                    }
                                ],
                            },
                            {
                                "title": answer_cal[1],
                                "description": "",
                                "thumbnail": {
                                    "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                                },
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "보러가기",
                                        "webLinkUrl": answer_link[1]
                                    },
                                    {
                                        "action": "webLink",
                                        "label": "홈페이지로 가기",
                                        "webLinkUrl": "https://scatch.ssu.ac.kr/%ea%b3%b5%ec%a7%80%ec%82%ac%ed%95%ad/page/1/"
                                    }
                                ]
                            },
                            {
                                "title": answer_cal[2],
                                "description": "",
                                "thumbnail": {
                                    "imageUrl": "http://k.kakaocdn.net/dn/83BvP/bl20duRC1Q1/lj3JUcmrzC53YIjNDkqbWK/i_6piz1p.jpg"
                                },
                                "buttons": [
                                    {
                                        "action": "webLink",
                                        "label": "보러가기",
                                        "webLinkUrl": answer_link[2]
                                    },
                                    {
                                        "action": "webLink",
                                        "label": "홈페이지로 가기",
                                        "webLinkUrl": "https://scatch.ssu.ac.kr/%ea%b3%b5%ec%a7%80%ec%82%ac%ed%95%ad/page/1/"
                                    }
                                ]
                            }
                        ]
                    }
                }
            ],
            'quickReplies': [
                {
                    'label': '🏠',
                    'action': 'message',
                    'messageText': '🏠'
                }
            ]
        }
    }

    return jsonify(res)


# 메인 함수
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
