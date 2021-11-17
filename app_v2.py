import urllib

from django.utils.datetime_safe import date
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

app = Flask(__name__)
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
prefs = {'profile.default_content_setting_values': {'cookies' : 2, 'images': 2, 'plugins' : 2, 'popups': 2, 'geolocation': 2, 'notifications' : 2, 'auto_select_certificate': 2, 'fullscreen' : 2, 'mouselock' : 2, 'mixed_script': 2, 'media_stream' : 2, 'media_stream_mic' : 2, 'media_stream_camera': 2, 'protocol_handlers' : 2, 'ppapi_broker' : 2, 'automatic_downloads': 2, 'midi_sysex' : 2, 'push_messaging' : 2, 'ssl_cert_decisions': 2, 'metro_switch_to_desktop' : 2, 'protected_media_identifier': 2, 'app_banner': 2, 'site_engagement' : 2, 'durable_storage' : 2}}
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome(options=options)


driver.get("https://soongguri.com/main.php?mkey=2&w=3&l=1")

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

@app.route('/food', methods=['GET', 'POST'])
def food_func():
    req = request.get_json()
    user_menu = req['userRequest']
    user_menu = user_menu['block']
    user_menu = user_menu['name']

    # url = "https://soongguri.com/main.php?mkey=2&w=3&l=1"
    # res = requests.get(url)
    # soup = BeautifulSoup(res.content.decode('utf-8', 'replace'), "html.parser")
    # if "자동등록방지" in soup.text:
    #   print("캡챠 실행됨")
    #  print(driver.page_source)
    # driver.find_element_by_tag_name("input").click()
    res = driver.page_source
    soup = BeautifulSoup(res, 'html.parser')
    # print("끝")
    data = soup.find("div", attrs={"class": "detail_center"})
    table = data.find("table")
    trs = table.find_all("tr")
    haksik_trs = trs[5]
    dodam_trs = trs[7]

    dodam_launch_route_1 = dodam_trs.find("table")
    dodam_launch_route_2 = dodam_launch_route_1.find("td", attrs={
        "style": "width:283.33333333333px;text-align:left;padding:3px;border:1px dotted #999999;vertical-align:top;"})

    dodam_launch_route_3 = dodam_launch_route_2.find_all("div")
    dodam_launch = ""

    rr = 0
    while True:
        dd = ""
        for d in dodam_launch_route_3[rr].children:
            dd = str(d)
        if dd == "<strong><br/></strong>" or "<font><br/></font>" in dd or rr > 10:
            break
        dodam_launch += dodam_launch_route_3[rr].get_text()
        if "<br/>" in dd:
            dodam_launch += "\n"
        rr += 1

    dodam_dinner_route_1 = dodam_trs.find("table")
    dodam_dinner_route_2 = dodam_dinner_route_1.find_all("td", attrs={
        "style": "width:283.33333333333px;text-align:left;padding:3px;border:1px dotted #999999;vertical-align:top;"})
    dodam_dinner_route_3 = dodam_dinner_route_2[2].find_all("div")
    dodam_dinner = ""

    rr = 0
    while True:
        dd = ""
        for d in dodam_dinner_route_3[rr].children:
            dd = str(d)
        if dd == "<strong><br/></strong>" or '<b><font color="#009900"><br/></font></b>' in dd or rr > 10:
            break
        dodam_dinner += dodam_dinner_route_3[rr].get_text()
        if "<br/>" in dd:
            dodam_dinner += "\n"
        rr += 1

    url = "https://ssudorm.ssu.ac.kr:444/SShostel/mall_main.php?viewform=B0001_foodboard_list&board_no=1"
    res = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(res, "html.parser")

    table = soup.find("table", attrs={"class": "boxstyle02"})
    dorm_trs = table.find_all("tr")

    answer_haksik = []
    answer_dorm = ""

    for haksik in haksik_trs.find_all("td"):
        answer_haksik.append(haksik.text)

    dorm_today = date.today().weekday() + 1
    for index, dorm in enumerate(dorm_trs[dorm_today].find_all("td")):
        if index == 0:
            answer_dorm += "[아침]\n"
            answer_dorm += dorm.text.strip()
        elif index == 1:
            answer_dorm += "\n\n[점심]\n"
            answer_dorm += dorm.text.strip()
        elif index == 2:
            answer_dorm += "\n\n[저녁]\n"
            answer_dorm += dorm.text.strip()

    dodam = "[오늘의 도담]\n" + "[점심]\n" + dodam_launch + "\n\n[저녁]\n" + dodam_dinner

    answer = ""
    if user_menu == "학생 식당":
        answer = "[오늘의 학식]\n" + answer_haksik[0]
    elif user_menu == "도담 식당":
        answer = dodam
    elif user_menu == "기숙사 식당":
        answer = "[오늘의 기식]\n" + answer_dorm
    else:
        answer = "다시 입력해주세요!"
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, threaded=True)
