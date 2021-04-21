import time
import datetime
import sys
import urllib.request
import webbrowser as wb

import cv2
import psutil
import pyautogui
import pyjokes
import pyttsx3
import requests
import smtplib
import speech_recognition as sr
import wikipedia

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer, QTime, QDate, pyqtSignal
from PyQt5.QtWidgets import *
from bs4 import BeautifulSoup
from requests import get
from selenium import webdriver
from tkcalendar import *
from tkinter import *
from playsound import playsound
from arfoUi import Ui_ARFOUi
from music import *

engine = pyttsx3.init()


def screenshot():
    usage = str(psutil.cpu_percent())
    speak("CPUは" + usage)
    battery = psutil.sensors_battery()
    speak("バッテリーは")
    speak(battery.percent)


def jokes():
    print(pyjokes.get_joke())
    speak(pyjokes.get_joke())


def sendEmail(to, content):
    server = smtplib.SMTP("", 587)
    server.ehlo()
    server.starttls()
    server.login("arfo88seiryu@gmail.com", "4152464f38356d663838")
    server.sendmail("arfo88seiryu@gmail.com", to, content)
    server.close()


def cpu():
    usage = str(psutil.cpu_percent())
    print("CPU is at" + usage)
    speak("CPU is at" + usage)
    battery = psutil.sensors_battery()
    print("Battery is at")
    speak("Battery is at")
    print(battery.percent)
    speak(battery.percent)


def weather():
    url = "https://weather.com/ja-JP/weather/today/l/7119d28e6aa6bc757e888763cb3653a597972e341baa437e08289c7f4344ad0f"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    location = soup.find("h1", class_="CurrentConditions--location--1Ayv3").text
    temperature = soup.find("span", class_="CurrentConditions--tempValue--3KcTQ").text
    weather = soup.find("div", class_="CurrentConditions--phraseValue--2xXSr").text
    print(location)
    speak("今日の天気は" + str(location))
    print(temperature)
    speak("では" + str(temperature))
    print(weather)
    speak(str(weather) + "です")


def news():
    url = "https://news.yahoo.co.jp/rss/topics/domestic.xml"
    response = urllib.request.urlopen(url)

    html = BeautifulSoup(response, "html.parser")

    topics = html.find_all("title")
    speak("国内のニュースは")
    i = 0
    for item in topics:
        if i > 0:
            print("{0}: {1}".format(i, item.string))
            speak("{0}: {1}".format(i, item.string))
        else:
            print(item.string)
        i += 1

    url = "https://news.yahoo.co.jp/rss/topics/world.xml"
    response = urllib.request.urlopen(url)

    html = BeautifulSoup(response, "html.parser")

    topics = html.find_all("title")
    speak("国際的なニュースは")
    i = 0
    for item in topics:
        if i > 0:
            print("{0}: {1}".format(i, item.string))
            speak("{0}: {1}".format(i, item.string))
        else:
            print(item.string)
        i += 1

    url = "https://news.yahoo.co.jp/rss/topics/it.xml"
    response = urllib.request.urlopen(url)

    html = BeautifulSoup(response, "html.parser")

    topics = html.find_all("title")
    speak("ＩＴ関連のニュースは")
    i = 0
    for item in topics:
        if i > 0:
            print("{0}: {1}".format(i, item.string))
            speak("{0}: {1}".format(i, item.string))
        else:
            print(item.string)
        i += 1

    url = "https://news.yahoo.co.jp/rss/topics/business.xml"
    response = urllib.request.urlopen(url)

    html = BeautifulSoup(response, "html.parser")

    topics = html.find_all("title")
    speak("経済的なニュースは")
    i = 0
    for item in topics:
        if i > 0:
            print("{0}: {1}".format(i, item.string))
            speak("{0}: {1}".format(i, item.string))
        else:
            print(item.string)
        i += 1


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def nowtime():
    NowTime = datetime.datetime.now().strftime("%I:%M %p")
    print("現在の時刻は" + NowTime)
    speak("現在の時刻は")
    speak(NowTime)


def date():
    year = int(datetime.datetime.now().year)
    month = int(datetime.datetime.now().month)
    date = int(datetime.datetime.now().day)
    print("今日は" + str(year) + "年" + str(month) + "月" + str(date) + "日")
    speak("きょうは" + str(year) + " ねん" + str(month) + " 月" + str(date) + " 日")


def wishme():
    print("おかえりなさい、ボス！")
    speak("おかえりなさい、ボス！")
    nowtime()
    date()
    hour = datetime.datetime.now().hour
    if hour >= 6 and hour < 12:
        print("おはよう、ボス！")
        speak("おはよう、ボス！")
    elif hour >= 12 and hour < 18:
        print("こんにちは、ボス！")
        speak("こんにちは、ボス！")
    elif hour >= 18 and hour < 24:
        print("こんばんは、ボス！")
        speak("こんばんは、ボス！")
    else:
        print("良い夜を、ボス！")
        speak("良い夜を、ボス！")
    print("ARFOに何か手伝う事はありますか？")
    speak("ARFOに何か手伝う事はありますか？")


def wish():
    speak("起きてます")


def standBy():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("聞いています・・・")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("待ってください・・・")
        query = r.recognize_google(audio, language="ja-in")
        print(f"user said: {query}")
    except Exception as e:
        print(e)
        print("もう一度話してください")
        return "None"
    return query


class MainThread(QThread):

    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("聞いています・・・")
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            print("待ってください・・・")
            query = r.recognize_google(audio, language="ja-in")
            print(f"user said: {query}")
        except Exception as e:
            print(e)
            speak("もう一度話してください")
            return "None"
        return query

    def TaskExecution(self):
        wishme()
        while True:
            self.query = self.takeCommand()
            if "時間" in self.query:
                nowtime()
            elif "日にち" in self.query:
                date()
            elif "アラーム" in self.query:
                speak("何時何分にセットしますか？")
                speak("何時に")
                Hour = self.takeCommand().lower()
                speak("何分に")
                Minute = self.takeCommand().lower()
                speak(f"{Hour}:{Minute}にセットしました")
                alarmtime = f"{Hour}:{Minute}"
                while True:
                    lcltime = datetime.datetime.now().strftime("%H:%M")
                    if lcltime == alarmtime:
                        speak("おはようございます、ボス。歯を磨いて、コーヒーブレイクをかましましょう！")
                        playsound("C:/Users/maske/Music/alarm.wav")
                        speak("今日の天気は")
                        weather()
                        speak("今日のニュースは")
                        news()
                        break
                    else:
                        print("not yet")
                        time.sleep(1)
            elif "Wikipedia" in self.query:
                try:
                    wikipedia.set_lang("ja")
                    speak("検索中...")
                    query = self.query.replace("wikipedia", "")
                    result = wikipedia.summary(query, sentences=2)
                    speak("検索しました")
                    print(result)
                    speak(result)
                except Exception as e:
                    speak(f"{self.query} + は検索できませんでした")
            elif "Chrome を開いて" in self.query:
                speak("何を検索しますか？")
                chromepath = "C:/Users/maske/AppData/Local/Google/Chrome/Application/chrome.exe %s"
                search = self.takeCommand().lower()
                wb.get(chromepath).open_new_tab(search + ".com")
            elif "Chrome を閉じて" in self.query:
                speak("分かりました")
                os.system("taskkill /f /im chrome.exe")
            elif "ログアウト" in self.query:
                os.system("shutdown -l")
            elif "シャットダウン" in self.query:
                os.system("shutdown /s /t l")
            elif "リスタート" in self.query:
                os.system("shutdown /r /t l")
            elif "スリープ" in self.query:
                os.system("rundll32.exe powrprof.dll, SetSuspendState 0,1,0")
            elif "モード" in self.query:
                speak("スタンバイしますか")
                a = standBy().lower()
                if a == "スタンバイ":
                    speak("スタンバイします")
                    b = standBy().lower()
                    c = ""
                    d = "起きてる"
                    while b != c:
                        if b == d:
                            speak("起きてます")
                            break
                        elif b == c:
                            time.sleep(1)
                        else:
                            time.sleep(1)
                        b = standBy().lower()
                    print("スタンバイモード解除")
                elif a == "レスト":
                    time.sleep(5)
            elif "音楽" in self.query:
                music1 = Music("maskers85miyabi@icloud.com", "4152464f38356d663838")
            elif "メモ帳を開いて" in self.query:
                speak("メモ帳を開きます")
                npath = "C:\\WINDOWS\\system32\\notepad.exe"
                os.startfile(npath)
            elif "メモ帳を閉じて" in self.query:
                speak("オッケー、メモ帳を閉じます。")
                os.system("taskkill /f /im notepad.exe")
            elif "コマンドを開いて" in self.query:
                speak("コマンドを開きます")
                os.system("start cmd")
            elif "コマンドを閉じて" in self.query:
                speak("コマンドを閉じます")
                os.system("taskkill /f /im cmd.exe")
            elif "カメラ" in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow("webcam", img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break;
                cap.release()
                cv2.destroyAllwindows()
            elif "YouTube を開いて" in self.query:
                speak("開きます。")
                chromepath = "C:/Users/maske/AppData/Local/Google/Chrome/Application/chrome.exe %s"
                wb.get(chromepath).open("www.youtube.com")
            elif "Youtube を閉じて" in self.query:
                speak("分かりました")
                os.system("taskkill /f /im chrome.exe")
            elif "Instagram" in self.query:
                print("ボス、アカウントの確認をします。")
                speak("ボス、アカウントの確認をします。")
                speak("メールアドレスを入力してください")
                name = input("ユーザー名を入力してください：")
                chromepath = "C:/Users/maske/AppData/Local/Google/Chrome/Application/chrome.exe %s"
                wb.get(chromepath).open(f"www.instagram.com/{name}")
                speak(f"ここはボスのプロフィールになります")
            elif "Google で検索" in self.query:
                speak("何を検索しますか?")
                cmd = self.takeCommand().lower()
                driver = webdriver.Chrome("C:/Program Files/chromedriver.exe")
                driver.get("https://google.com")
                searchbox = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[1]/div/div[2]/input')
                searchbox.send_keys(f"{cmd}")
                searchButton = driver.find_element_by_xpath('//*[@id="tsf"]/div[2]/div[1]/div[3]/center/input[1]')
                searchButton.click()
            elif "Google を閉じて" in self.query:
                speak("分かりました")
                os.system("taskkill /f /im chromedriver.exe")
            elif "ニュース" in self.query:
                speak("待ってくださいボス、最近のニュースは")
                news()
            elif "天気" in self.query:
                speak("データを取りに行っています")
                speak("持ってきました、今日の天気予報は")
                weather()
            elif "メール" in self.query:
                try:
                    speak("何を書きますか？")
                    content = self.takeCommand().lower()
                    to = "wakazishi85shiyu@gmail.com"
                    sendEmail(to, content)
                    speak("Emailを送りました。")
                except Exception as e:
                    print(e)
                    speak("すみません、ボス。送る事は出来ませんでした。")
            elif "記録" in self.query:
                data = self.takeCommand()
                speak("あなたは、" + data + "を記録してと言いました。")
                remember = open("data.txt", "w")
                remember.write(data)
                remember.close()
            elif "何　記録？" in self.query:
                remember = open("data.txt", "r")
                speak("あなたが言った" + remember.read() + "を知っています。")
            elif "スクリーンショット" in self.query:
                speak("ボス、スクリーンショットのファイル名を教えてください")
                name = self.takeCommand().lower()
                speak("少しお待ちください、スクリーンショットをします")
                img = pyautogui.screenshot()
                img.save(f"{name}.png")
                speak("完了しましたボス。スクリーンショットをフォルダーに保存しました。")
            elif "現在地" in self.query or "ここはどこ" in self.query:
                speak("待ってください、ボス。確認しています。")
                try:
                    ipAdd = requests.get("https://api.ipify.org").text
                    print(ipAdd)
                    url = "https://get.geojs.io/v1/ip/geo/" + ipAdd + ".json"
                    geo_requests = requests.get(url)
                    geo_data = geo_requests.json()
                    # print(geo_data)
                    city = geo_data["city"]
                    # state = geo_data["state"]
                    country = geo_data["country"]
                    print(f"ボスが現在一番近い位置情報は、{country}の{city}市になります")
                    speak(f"ボスが現在一番近い位置情報は、{country}の{city}市になります")
                except Exception as e:
                    speak("すいません、ボス。現在地の取得に失敗しました")
                    pass
            elif "IP アドレス" in self.query:
                ip = get('https://api.ipify.org').text
                print(f"your IP address is {ip}")
                speak(f"your IP address is {ip}")
            elif "cpu" in self.query:
                cpu()
            elif "ジョーク" in self.query:
                jokes()
            elif "オフライン" in self.query or "断る" in self.query:
                print("おやすみなさい、ボス！")
                speak("おやすみなさい、ボス！")
                quit()
            elif "ありがとう" in self.query:
                speak("Thaks for using me Boss. Have a Good Day.")
                sys.exit()
            print("ボス、何をしましょうか？")
            speak("ボス、何をしましょうか？")


startExecution = MainThread()

class Main(QMainWindow, QtWidgets.QPlainTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_ARFOUi()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton.clicked.connect(self.weatherDisplay)
        self.ui.pushButton.clicked.connect(self.name)
        self.ui.pushButton_2.clicked.connect(self.close)


    def startTask(self):
        self.ui.movie = QtGui.QMovie()
        self.ui.movie.setFileName("C:/Users/maske/Pictures/black.jpg")
        self.ui.ARFOUi.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie()
        self.ui.movie.setFileName("C:/Users/maske/Pictures/arfoofcore.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie()
        self.ui.movie.setFileName("C:/Users/maske/Pictures/xvoice.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie()
        self.ui.movie.setFileName("C:/Users/maske/Pictures/weatherimage.gif")
        self.ui.label_3.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString("hh:mm:ss")
        label_date = current_date.toString("yyyy/MM/dd")
        self.ui.arfoUI.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

    def weatherDisplay(self):
        url = "https://weather.com/ja-JP/weather/today/l/7119d28e6aa6bc757e888763cb3653a597972e341baa437e08289c7f4344ad0f"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        location = soup.find("h1", class_="CurrentConditions--location--1Ayv3").text
        temperature = soup.find("span", class_="CurrentConditions--tempValue--3KcTQ").text
        weather_display = soup.find("div", class_="CurrentConditions--phraseValue--2xXSr").text
        self.ui.textEdit.setPlainText(location)
        self.ui.textEdit_2.setPlainText(temperature)
        self.ui.textEdit_3.setPlainText(weather_display)

    def name(self):
        name = "A.R.F.O"
        self.ui.textEdit_4.setPlainText(name)






app = QApplication(sys.argv)
arfo = Main()
arfo.show()
sys.exit(app.exec_())
