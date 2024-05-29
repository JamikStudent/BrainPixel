import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk, ImageEnhance
from tkinter import ttk
from shopp import *
import requests
import pygame
from test import *

user1 = User()

# Создаем окно
root = tk.Tk()
pygame.init()
# включаем полный экран
root.attributes("-fullscreen", True)
root.title("Brain Pixel")

# Получаем размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#Переменные, отвечающие за музыку в игре
global main_song
global button_song
main_song = pygame.mixer.Sound('music\main_song.mp3')
button_song = pygame.mixer.Sound('music\click_song.mp3')

#Переменная отвечающая за скин в настоящее время
global style
style = "Blue"

#Переменная, отвечающая за то, какой тест откроется у пользователя
global current_test
current_test = 1

global authenticated
global registration
authenticated = False
registration = False

#Класс , созданный для кнопок в приложении
class MyButton:
    def __init__(self, x,y,X,Y,name,where,to):
        self.x = x
        self.y = y
        self.X = X
        self.Y = Y
        self.name = name  # Название кнопки
        self.where = where  # С какой кнопки мы пришли к этой кнопке
        self.to = to  # Куда ведёт эта кнопка (к каким кнопкам она ведёт)

    def changeState(self):
        ChangeMapButton(self.where)  #Там, откуда пришли, кнопки отключаем
        ChangeMapButton(self.to)  # Куда идём кнопки включаем

    def wasClicked(self, x, y):  #Функция проверки был ли клик, если да, меняем значения кнопок
        if self.x <= x <= self.X and self.y <= y <= self.Y and (MapButton.get(self.where)).get(self.name) == True:
            self.changeState()
            button_song.play()
            return True
        else:
            return False

def MakePhoto(name): #Функция загрузки фоток
    # Загружаем изображение
    image = Image.open(name)

    # Масштабируем изображение до размеров экрана
    image = image.resize((screen_width, screen_height), Image.ADAPTIVE)

    # Создаем изображение Tkinter
    image = ImageTk.PhotoImage(image)
    return image

def MakeNeedPhoto(name,w,h): #Функция загрузки фоток
    # Загружаем изображение
    image = Image.open(name)

    # Масштабируем изображение до размеров экрана
    image = image.resize((w, h), Image.ADAPTIVE)

    # Создаем изображение Tkinter
    image = ImageTk.PhotoImage(image)
    return image

def MakePhotoBack(name):  #Функция загрузки затемнённых фоток (при использовании всплывающих окон)
    # Загружаем изображение
    image = Image.open(name)

    # Масштабируем изображение до размеров экрана
    image = image.resize((screen_width, screen_height), Image.ADAPTIVE)

    #Затемняем фото
    image = ImageEnhance.Brightness(image)
    image = image.enhance(0.5)

    # Создаем изображение Tkinter
    image = ImageTk.PhotoImage(image)
    return image
# Словарь для кнопок
MapButton = {"StartGame": { #Название кнопки
                "Login": True #Кнопки, к которым ведёт данная кнопка
            },
            "Login":{ #Тут по аналогии
                "Registration": False,
                "Main": False
            },
            "Registration":{
                "Login": False,
                "Main": False
            },
             "Main": {
                 "Login": False,
                 "Shop": False,
                 "Start": False,
                 "Settings": False,
                 "Map": False,
                 "Exit": False
                    },
             "Shop": {
                 "Back": False,
                 "Earn": False,
                 "BuyFirstTip": False,
                 "BuySecondTip": False,
                 "BuySkin": False
             },
             "BuySkin":{
                 "PinkSkin":False,
                 "BuyPink":False,
                 "GreenSkin":False,
                 "BuyGreen":False,
                 "Back":False
             },
             "Start": {
                 "Back": False,
                 "Test": False
             },
             "Test":{
                "Finish": False,
                "Previous": False,
                "Next": False
             },
             "Finish": {
                 "NoFinish":False,!
                 "YesFinish": False
             },
             "YesFinish":{
                 "Back": False
             },
             "Settings":{
                 "Back": False,
                 "ChangeSkin": False,
                 "Help": False
             },
             "ChangeSkin":{
                 "BaseSkin": False,
                 "PinkSkin": False,
                 "GreenSkin": False,
                 "Back": False
             },
             "Help": {
                 "Back": False
             },
             "Map": {
                 "First":False,
                 "Second": False,
                 "Third": False,
                 "Fourth": False,
                 "Fifth": False,
                 "Sixth": False,
                 "Seventh": False,
                 "Back": False
             },
            "AboutTask":{
                "Map":False
            }
            }

# процентные координаты, х и у - один процент от длины своей координаты
xElement = screen_width * 0.01
yElement = screen_height * 0.01

#Хранилище фото для краткой информации по теме на карте
MapStorage = {
    1:MakePhoto("image/tema1.png"),
    2:MakePhoto("image/tema2.png"),
    3:MakePhoto("image/tema3.png"),
    4:MakePhoto("image/tema4.png"),
    5:MakePhoto("image/tema5.png"),
    6:MakePhoto("image/tema6.png"),
    7:MakePhoto("image/tema7.png"),
}

#Хранилище координат для персонажа по заданиям
ChudoCordsStorage = {
    1:[xElement * 12.5, yElement * 43],
    2:[xElement * 31.3, yElement * 67],
    3:[xElement * 56.7, yElement * 76.8],
    4:[xElement * 77.7, yElement * 55],
    5:[xElement * 81.8, yElement * 20],
    6:[xElement * 56.8, yElement * 21],
    7:[xElement * 32.5, yElement * 9]
}


PhotoStorage = {#Хранилище фотографий для всех скинов
    "Base":{#Фотки для базового скина
        "startPhoto": MakePhoto("image/start_page.png"),
        "mainPhoto": MakePhoto("image/main.png"),
        "mapPhoto": MakePhoto("image/map.png"),
        "mapBackPhoto": MakePhotoBack("image/map.png"),
        "infoPhoto": MakePhoto("image/info.png"),
        "testPhoto": MakePhoto("image/test.png"),
        "testBackPhoto":MakePhotoBack("image/test.png"),
        "settingsPhoto" : MakePhoto("image/settings.png"),
        "settingsBackPhoto":MakePhotoBack("image/settings.png"),
        "shopPhoto" : MakePhoto("image/shop.png"),
        "shopBackPhoto": MakePhotoBack("image/shop.png"),
        "helpPhoto" : MakePhoto("image/spravka.png"),
        "finishPhoto": MakePhoto("image/miniwindow.png"),
        "yesfinishPhoto" : MakePhoto("image/0ball.png"),
        "loginPhoto" : MakePhoto("image/vkhod.png"),
        "registrationPhoto" : MakePhoto("image/registratsia.png"),
        "choosePhoto": MakePhoto("image/skin.png"),
        "chudoPhoto": MakeNeedPhoto("image/chudo.png",round(xElement*5),round(yElement*9)) 
    },
    "Pink":{ #Фотки заставок для розового скина
        "mainPhoto": MakePhoto("image/mainpink.png"),
        "mapPhoto": MakePhoto("image/mappink.png"),
        "mapBackPhoto": MakePhotoBack("image/mappink.png"),
        "infoPhoto": MakePhoto("image/infopink.png"),
        "testPhoto": MakePhoto("image/testpink.png"),
        "testBackPhoto": MakePhotoBack("image/testpink.png"),
        "settingsPhoto": MakePhoto("image/settingspink.png"),
        "settingsBackPhoto": MakePhotoBack("image/settingspink.png"),
        "shopPhoto": MakePhoto("image/shoppink.png"),
        "shopBackPhoto": MakePhotoBack("image/shoppink.png"),
        "helpPhoto": MakePhoto("image/spravkapink.png"),
        "finishPhoto": MakePhoto("image/miniwindow.png"),
        "yesfinishPhoto": MakePhoto("image/0ballpink.png"),
        "loginPhoto": MakePhoto("image/vkhodpink.png"),
        "registrationPhoto": MakePhoto("image/registratsiapink.png"),
        "choosePhoto": MakePhoto("image/skinpink.png"),
        "buyskinPhoto": MakePhoto("image/buyskinpink.png"),
        "chudoPhoto": MakeNeedPhoto("image/chudopink.png",round(xElement*5),round(yElement*9))  
    },
    "Green":{ #Фотки заставок для розового скина
        "mainPhoto": MakePhoto("image/maingreen.png"),
        "mapPhoto": MakePhoto("image/mapgreen.png"),
        "mapBackPhoto": MakePhotoBack("image/mapgreen.png"),
        "infoPhoto": MakePhoto("image/infogreen.png"),
        "testPhoto": MakePhoto("image/testgreen.png"),
        "testBackPhoto": MakePhotoBack("image/testgreen.png"),
        "settingsPhoto": MakePhoto("image/settingsgreen.png"),
        "settingsBackPhoto": MakePhotoBack("image/settingsgreen.png"),
        "shopPhoto": MakePhoto("image/shopgreen.png"),
        "shopBackPhoto": MakePhotoBack("image/shopgreen.png"),
        "helpPhoto": MakePhoto("image/spravkagreen.png"),
        "finishPhoto": MakePhoto("image/miniwindow.png"),
        "yesfinishPhoto": MakePhoto("image/0ballgreen.png"),
        "loginPhoto": MakePhoto("image/vkhodgreen.png"),
        "registrationPhoto": MakePhoto("image/registratsiagreen.png"),
        "choosePhoto": MakePhoto("image/skingreen.png"),
        "buyskinPhoto": MakePhoto("image/buyskingreen.png"),
        "chudoPhoto": MakeNeedPhoto("image/chudogreen.png",round(xElement*5),round(yElement*9))
    }
}

# Создаем холст (Canvas)
canvas = tk.Canvas(root, width=screen_width, height=screen_height,highlightthickness=0)
canvas.pack()

#Значение ползунка
global val
val = 50

#Виджеты для ввода информации о пользователе
global login_widget
global password_widget
global email_entry
global login_entry
global password_entry

#Виджет для ползунка громкости
global win
def update_slider(value):
    # Функция обновления, которая будет вызываться при изменении положения ползунка
    global val
    global main_song
    val = value
    main_song.set_volume(int(value) / 100)

# Устанавливаем изображение как фон холста
canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["startPhoto"])
main_song.play(-1)
main_song.set_volume(0.5)

#Функция для смены состояния кнопок - Используется, когда нажимаем на кнопку
def ChangeMapButton(name):
    for i in MapButton[name]:
        MapButton[name][i] = not MapButton[name][i]


def ManageEscape(event):
    exit()

selected_topic_id = 1  # Здесь 1 - это пример topic_id выбранной темы
current_question_index = 0
questions = []

# функция, принимающая координаты клика
def ManageButton(event):
    global win
    global login_widget
    global password_widget
    global email_entry
    global login_entry
    global password_entry
    global style
    global user_id
    global current_question_index
    global current_test # NEW: Какой из 7 тестов сейчас будет
    # NEW: Новые кнопки
    YesFinishBackButton = MyButton(xElement * 34.8, yElement * 66.7, xElement * 65.6, yElement * 83.5, "Back", "YesFinish", "Main")
    YesFinishButton = MyButton(xElement * 53, yElement * 45.2, xElement * 63.4, yElement * 51.5, "YesFinish", "Finish", "YesFinish")
    NoFinishButton = MyButton(xElement*35,yElement*45.2,xElement*45.1,yElement*51.5, "NoFinish", "Finish","Test")
    ChooseSkinBackButton = MyButton(xElement * 84.6, yElement * 29, xElement * 90.4, yElement * 38.5, "Back", "BuySkin", "Shop")
    ChooseSkinGreenButton = MyButton(xElement * 53.5, yElement * 67, xElement * 74, yElement * 78, "GreenSkin", "BuySkin", "BuySkin")
    ChooseSkinPinkButton = MyButton(xElement * 53.5, yElement * 44.6, xElement * 74, yElement * 55.3, "PinkSkin", "BuySkin", "BuySkin")
    BuySkinGreenButton = MyButton(xElement * 75.5, yElement * 67, xElement * 88.3, yElement * 78, "BuyGreen", "BuySkin", "BuySkin")
    BuySkinPinkButton = MyButton(xElement * 75.5, yElement * 45, xElement * 88.3, yElement * 55.2, "BuyPink", "BuySkin", "BuySkin")
    MapFirstButton = MyButton(xElement * 12.5, yElement * 43, xElement * 17.5, yElement * 50.8, "First","Map","AboutTask")
    MapSecondButton = MyButton(xElement * 31.3, yElement * 67, xElement * 36.5, yElement * 75,"Second","Map","AboutTask")
    MapThirdButton = MyButton(xElement * 56.7, yElement * 76.8, xElement * 62, yElement * 85,"Third","Map","AboutTask")
    MapFourthButton = MyButton(xElement * 77.7, yElement * 55, xElement * 82.7, yElement * 63,"Fourth","Map","AboutTask")
    MapFifthButton = MyButton (xElement * 81.8, yElement * 20, xElement * 86.8, yElement * 28,"Fifth","Map","AboutTask")
    MapSixthButton = MyButton(xElement * 56.8, yElement * 21, xElement * 61.8, yElement * 29,"Sixth","Map","AboutTask")
    MapSeventhButton = MyButton(xElement * 32.5, yElement * 9, xElement * 37.5, yElement * 17,"Seventh","Map","AboutTask")
    AboutTaskBackButton = MyButton(0,0,xElement*100,yElement*100, "Map","AboutTask","Map")

    StartGameButton = MyButton(xElement * 75.2, yElement * 39.7, xElement * 14 + xElement * 75.2, yElement * 22 + yElement * 39.7,"Login","StartGame","Login")
    RegistrationButton = MyButton(xElement * 41.4, yElement * 25.7, xElement * 61.6, yElement * 34.4,"Registration","Login","Registration")
    RegistrationMainButton = MyButton(xElement * 28, yElement * 81.8, xElement * 54.6, yElement *88.4, "Main","Registration","Main")
    LoginMainButton = MyButton(xElement * 28, yElement * 81.8, xElement * 54.6, yElement *88.4, "Main","Login","Main")
    LoginButton = MyButton(xElement * 20.9, yElement * 25.7, xElement * 40.8, yElement *34.4,"Login","Registration","Login")
    CreatorsButton = MyButton(xElement*3.2, yElement*27.8,xElement*18.6, yElement*74.8, "Creators","Main","Creators")
    ShopButton = MyButton(xElement * 21.2, yElement * 27.8,xElement * 37.3, yElement * 74.8, "Shop","Main","Shop")
    MainStartButton = MyButton(xElement * 41.1, yElement * 27.8,xElement * 57.4, yElement * 74.8,"Start","Main","Start")
    SettingsButton = MyButton(xElement * 61.5, yElement * 27.8,xElement * 76.6, yElement * 74.8,"Settings","Main","Settings")
    MainMapButton = MyButton(xElement * 80.4, yElement * 27.8,xElement * 96.5, yElement * 74.8,"Map","Main","Map")
    ExitButton = MyButton(xElement * 80.6, yElement * 11.8,xElement * 97.4, yElement * 17.5,"Exit","Main","Main")
    CreatorsBackButton = MyButton(xElement * 4.5, yElement * 6.5,xElement * 16.6, yElement * 13.6,"Back","Creators","Main")
    MapBackButton = MyButton(xElement * 1.8, yElement * 3, xElement * 13.4, yElement * 10, "Back", "Map", "Main")# UPDATED
    StartBackButton = MyButton(xElement * 3, yElement * 6.2, xElement * 14.8, yElement * 13.2,"Back","Start","Main")
    StartTestButton = MyButton(xElement * 39.7, yElement * 88.4,xElement * 60.3, yElement * 96,"Test","Start","Test")
    TestFinishButton = MyButton(xElement * 33, yElement * 86.8, xElement * 62.2, yElement * 97.7,"Finish","Test","Finish")
    FinishBackButton = MyButton(xElement * 34.8, yElement * 66.7, xElement * 65.6, yElement * 83.5, "Back","Finish", "Main")
    ShopBackButton = MyButton(xElement * 4.2, yElement * 7.3, xElement * 15.9, yElement * 14.2, "Back","Shop","Main")
    ShopBuyFirstTipButton = MyButton(xElement * 11, yElement * 73.2, xElement * 22, yElement * 78.2, "BuyFirstTip","Shop","Shop")
    ShopBuySkinButton = MyButton(xElement * 77.9, yElement * 73.1, xElement * 89, yElement * 78.2, "BuySkin","Shop","BuySkin")# UPDATED
    ShopBuySecondTipButton = MyButton(xElement * 44.7, yElement * 73,xElement * 55.8, yElement * 78.2,"BuySecondTip","Shop","Shop")
    ShopEarnButton = MyButton(xElement * 76.8, yElement * 15, xElement * 98.4, yElement * 25.2,"Earn","Shop", "Shop")
    SettingsBackButton = MyButton(xElement * 3.5, yElement * 6.4, xElement * 15.1, yElement * 13.2, "Back","Settings","Main")
    SettingsHelpButton = MyButton(xElement * 62.8, yElement * 56, xElement * 90.2, yElement * 70.8, "Help","Settings","Help")
    SettingsChangeSkinButton = MyButton(xElement * 62.8, yElement * 75.5, xElement * 90.2, yElement * 90.5, "ChangeSkin","Settings","ChangeSkin")
    HelpBackButton = MyButton(xElement * 3.6, yElement * 5.9, xElement * 15.2, yElement * 12.6, "Back","Help","Settings")
    BaseSkinButton = MyButton(xElement*59,yElement*39.1,xElement*79.3,yElement*49.9,"BlueSkin","ChangeSkin","ChangeSkin")
    PinkSkinButton = MyButton(xElement * 59, yElement * 55.6, xElement * 79.3, yElement * 66.4,"PinkSkin","ChangeSkin","ChangeSkin")
    GreenSkinButton = MyButton(xElement * 59, yElement * 72.2, xElement * 79.3, yElement * 83.1,"GreenSkin","ChangeSkin","ChangeSkin")
    ChangeSkinBackButton = MyButton(xElement * 84.4, yElement * 29.2, xElement * 90.4, yElement * 38.5,"Back","ChangeSkin","Settings")
    TestPreviousButton = MyButton(xElement * 24.2, yElement * 80.3, xElement * 34.7, yElement * 86.8,"Previous","Test","Test")
    TestNextButton = MyButton(xElement * 64.8, yElement * 80.1, xElement * 75.3, yElement * 86.6,"Previous","Test","Test")
    MainLoginButton = MyButton(xElement*3.2, yElement*27.8,xElement*18.6, yElement*74.8, "Login","Main","Login")

    # Проверяем, попадает ли координата нажатия мыши в заданную область

    # если точка в зоне кнопки
    if StartGameButton.wasClicked(event.x, event.y):
        login_window()
    elif RegistrationButton.wasClicked(event.x, event.y):
        registration_window()
    elif LoginButton.wasClicked(event.x, event.y):
        login_window()
    elif RegistrationMainButton.wasClicked(event.x, event.y):
        if registration_user():
            start_window_1()
    elif LoginMainButton.wasClicked(event.x, event.y):
        if login_user():
            start_window_1()
    elif CreatorsButton.wasClicked(event.x, event.y):
        creators_window()
    elif MainLoginButton.wasClicked(event.x, event.y):
        login_window()
    elif ShopButton.wasClicked(event.x,event.y):
        shop_window(0, None)
    elif SettingsButton.wasClicked(event.x,event.y):
        settings_window()
    elif SettingsBackButton.wasClicked(event.x, event.y):
        canvas.delete(win)
        start_window_1()
    elif SettingsHelpButton.wasClicked(event.x, event.y):
        canvas.delete(win)
        help_window()
    elif SettingsChangeSkinButton.wasClicked(event.x,event.y):
        canvas.delete(win)
        skin_window("Blue")
    elif BaseSkinButton.wasClicked(event.x,event.y):
        style = "Blue"
        skin_window("Blue")
    elif PinkSkinButton.wasClicked(event.x, event.y):
        style = "Pink"
        skin_window("Pink")
    elif GreenSkinButton.wasClicked(event.x, event.y):
        style = "Green"
        skin_window("Green")
    elif ChangeSkinBackButton.wasClicked(event.x,event.y):
        settings_window()
    elif HelpBackButton.wasClicked(event.x,event.y):
        settings_window()
    elif MainMapButton.wasClicked(event.x, event.y) or AboutTaskBackButton.wasClicked(event.x, event.y):# NEW
        map_window(current_test)
    elif MapBackButton.wasClicked(event.x, event.y):
        start_window_1()
    elif MainStartButton.wasClicked(event.x, event.y):
        info_window(1)
    elif StartTestButton.wasClicked(event.x, event.y):
        test_window(1)
    elif TestNextButton.wasClicked(event.x,event.y):
        global current_question_index
        if current_question_index < len(questions) - 1:
            submit_answer()
            current_question_index += 1
            test_window(current_question_index)
        else:
            print("Вопросы закончились")
            #submit_answer()
            #cs = submit_all_answers()
            #finish_window(cs)
    elif TestPreviousButton.wasClicked(event.x, event.y):
        if current_question_index > 0:
            submit_answer()
            current_question_index -= 1
            test_window(current_question_index)
    elif YesFinishButton.wasClicked(event.x, event.y):# UPDATED : Переименовано
        submit_answer()
        cs = submit_all_answers()
        yesfinish_window(cs)# UPDATED : Переименовано
        if current_test < 7:# NEW : Нужно заносить в базу данных новое значение текущего теста
            current_test += 1

    elif YesFinishBackButton.wasClicked(event.x , event.y):# UPDATED : Переименовано
        start_window_1()
    elif StartBackButton.wasClicked(event.x, event.y):
        start_window_1()
    elif ExitButton.wasClicked(event.x,event.y):
        exit()
    elif ShopBuySkinButton.wasClicked(event.x, event.y):
        canvas.delete("all")
        canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["shopPhoto"])
        user_id = 1
        skin_pink = 'pink'
        skin_green = 'green'
        buy_skin_url = f'http://localhost:8000/users/{user_id}/buy_skin/{skin_pink}/'
        buy_skin_url1 = f'http://localhost:8000/users/{user_id}/buy_skin/{skin_green}/'
        response = requests.post(buy_skin_url)
        response1 = requests.post(buy_skin_url1)
        if response.status_code == 200:
            data = response.json()
            data1 = response1.json()
            user1.set_count_of_money(data['balance'])
            user1.set_count_of_money(data1['balance'])
            canvas.create_text(xElement * 84.5, yElement * 8, text=user1.get_count_of_money(), font="Impact 40")
        else:
            print("Error:", response.status_code)
        update_user_data()
    elif ShopEarnButton.wasClicked(event.x, event.y):
        user_id = 1
        bonus_coin_url = f'http://localhost:8000/users/{user_id}/bonus_coin/'
        response = requests.post(bonus_coin_url)

        if response.status_code == 200:
            data = response.json()
            user1.set_count_of_money(data['balance'])
            canvas.create_text(xElement * 84.5, yElement * 8, text=user1.get_count_of_money(), font="Impact 40")
        else:
            print("Error:", response.status_code)
        update_user_data()
    elif ShopBuyFirstTipButton.wasClicked(event.x, event.y):
        user_id = 1
        shop_window(user_id, 'first')
    elif ShopBuySecondTipButton.wasClicked(event.x, event.y):
        user_id = 1
        shop_window(user_id, 'second')
    elif ShopBackButton.wasClicked(event.x, event.y):
        start_window_1()

    # NEW
    #Покупка зелёного скина
    elif BuySkinGreenButton.wasClicked(event.x, event.y):
        style = "Green"
    #Покупка розового скина
    elif BuySkinPinkButton.wasClicked(event.x, event.y):
        style="Pink"
    #Выбор розового скина для осмотра
    elif ChooseSkinPinkButton.wasClicked(event.x, event.y):
        buyskin_window("Pink")
    #Вывод окна вы точно хотите завершить тест?
    elif TestFinishButton.wasClicked(event.x, event.y):
        finish_window()
    #Возврат в магазин из окна выбора скинов
    elif ChooseSkinBackButton.wasClicked(event.x, event.y):
        shop_window()
    #Вывод краткой информации о тестах
    elif MapFirstButton.wasClicked(event.x,event.y):
        abouttask_window(1)
    elif MapSecondButton.wasClicked(event.x,event.y):
        abouttask_window(2)
    elif MapThirdButton.wasClicked(event.x,event.y):
        abouttask_window(3)
    elif MapFourthButton.wasClicked(event.x,event.y):
        abouttask_window(4)
    elif MapFifthButton.wasClicked(event.x,event.y):
        abouttask_window(5)
    elif MapSixthButton.wasClicked(event.x,event.y):
        abouttask_window(6)
    elif MapSeventhButton.wasClicked(event.x,event.y):
        abouttask_window(7)
    #Если пользователь нажал, что не хочет завершить тест
    elif NoFinishButton.wasClicked(event.x, event.y):
        test_window(current_question_index)

    else:
        return

def update_user_data(user_id, skin_name):
    url = f'http://localhost:8000/users/{user_id}/buy_skin/{skin_name}/'
    response = requests.post(url)
    if response.status_code == 200:
        data = response.json()
        user1.set_count_of_money(data['balance'])
        canvas.create_text(xElement * 84.5, yElement * 8, text=user1.get_count_of_money(), font="Impact 40")
    else:
        print("Error:", response.status_code)

def shop_window(user_id, type_of_tip):
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["shopPhoto"])
    def update_user_data():
        url = f'http://localhost:8000/users/{user_id}/buy_tips/{type_of_tip}/'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            user1.set_count_of_money(data['balance'])
            canvas.create_text(xElement * 84.5, yElement * 8, text=user1.get_count_of_money(), font="Impact 40")
        else:
            print("Error:", response.status_code)

    update_user_data()

def skin_window(style):
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["settingsBackPhoto"])
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["choosePhoto"])

    return
    #canvas.create_rectangle(xElement*59,yElement*39.1,xElement*79.3,yElement*49.9,fill="#80CBC4", outline="#004D40")
    #canvas.create_rectangle(xElement * 59, yElement * 55.6, xElement * 79.3, yElement * 66.4, fill="#80CBC4", outline="#004D40")
    #canvas.create_rectangle(xElement * 59, yElement * 72.2, xElement * 79.3, yElement * 83.1, fill="#80CBC4", outline="#004D40")
    #canvas.create_rectangle(xElement * 84.4, yElement * 29.2, xElement * 90.4, yElement * 38.5, fill="#80CBC4",outline="#004D40")

def change_skin(skin_name):
    user_id = 1
    change_skin_url = f'http://localhost:8000/users/{user_id}/change_skin/{skin_name}/'
    response = requests.post(change_skin_url)
    if response.status_code == 200:
        print(f"Successfully changed skin to {skin_name}.")
    else:
        print("Error:", response.status_code)

def get_skin_info():
    user_id = 1
    skin_info_url = f'http://localhost:8000/users/{user_id}/skin_info/'
    response = requests.get(skin_info_url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error:", response.status_code)
        return None

def create_button(x, y, text, command):
    button = tk.Button(canvas, text=text, command=command)
    button.place(x=x, y=y, width=100, height=50)

def yesfinish_window(score):#Функция для завершения теста
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["finishPhoto"])
    canvas.create_text(xElement * 50, yElement * 30, text=f'Вы набрали {score} баллов!', fill="Black", font="Impact 30")
    return

def abouttask_window(id):#Функция вывода краткой информации о тесте
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["mapBackPhoto"])
    canvas.create_image(ChudoCordsStorage[id][0], ChudoCordsStorage[id][1], anchor=tk.NW,
                        image=PhotoStorage[style]["chudoPhoto"])
    canvas.create_image(xElement * 33, yElement * 20, anchor=tk.NW, image=MapStorage[id])

def buyskin_window(style_skin):
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["shopBackPhoto"])
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style_skin]["buyskinPhoto"])

def finish_window():#Окно вы точно хотите завершить тест?
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["testBackPhoto"])
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["finishPhoto"])
    
def settings_window():
    global win
    global val
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["settingsPhoto"])
    slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=update_slider,length=xElement*20)
    slider.set(val)
    slider.pack()
    canvas.update()
    win = canvas.create_window(xElement*77, yElement*45, anchor=tk.CENTER, window=slider)
    canvas.pack()
    slider.pack_forget()
    canvas.pack()

    return

def help_window():
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["helpPhoto"])
    return

def load_questions():
    global questions
    url = f'http://localhost:8000/questions/1/'
    response = requests.get(url)
    if response.status_code == 200:
        questions = response.json()
        return True
    else:
        print("Ошибка при загрузке вопросов:", response.status_code)
        return False

answer_vars = []

def test_window(topic_id):
    global current_question_index, answer_vars
    color = GetColorByStyle(style)

    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["testPhoto"])

    if not load_questions():
        return

    if current_question_index < len(questions):
        question = questions[current_question_index]
        print("Debug: Текущий вопрос:", question)
        if 'answer_true' not in question or 'answer_false_1' not in question \
                or 'answer_false_2' not in question or 'answer_false_3' not in question:
            print("Ошибка: Не найдены варианты ответов для текущего вопроса.")
            return None

        # Вопрос в тесте
        question_label = tk.Label(root, text=f"Вопрос {current_question_index + 1}: {question['question_text']}", wraplength=xElement*80, bg=color, font=("Constantia", 27, "bold"))
        canvas.create_window(xElement*50, yElement*23, window=question_label)

        answer_options = [
                question['answer_true'],
                question['answer_false_1'],
                question['answer_false_2'],
                question['answer_false_3']
        ]

        # Создать переменные IntVar для хранения состояния каждого Checkbutton
        answer_vars = [tk.IntVar() for _ in range(len(answer_options))]

        # Отобразить варианты ответов с помощью Checkbutton
        for j, (answer_text, answer_var) in enumerate(zip(answer_options, answer_vars)):
            answer_checkbox = tk.Checkbutton(root, text=answer_text, bg=color, activebackground=color, font="Constantia 25", variable=answer_var)
            canvas.create_window(xElement*10, yElement*(35+j*10), window=answer_checkbox, anchor=tk.W)

    else:
        print("Вопросы закончились")
        submit_all_answers()



 # Добавить кнопку "Ответить"
        #submit_button = tk.Button(root, text="Ответить", command=lambda: submit_answer(answer_vars))
        #canvas.create_window(xElement*50, yElement*90, window=submit_button)
    
    #Чекбоксы
    #Answer1 = tk.Checkbutton(root,text=A1Text,bg=color,activebackground=color,font="Constantia 25",variable=FirstAnswer)
    #canvas.create_window(xElement*10,yElement*35,window=Answer1,anchor=tk.W)
    #Answer2 = tk.Checkbutton(root, text=A2Text, bg=color,activebackground=color,font="Constantia 25",variable=SecondAnswer)
    #canvas.create_window(xElement * 10, yElement * 45, window=Answer2,anchor=tk.W)
    #Answer3 = tk.Checkbutton(root, text=A3Text, bg=color,activebackground=color,font="Constantia 25",variable=ThirdAnswer)
    #canvas.create_window(xElement * 10, yElement * 55, window=Answer3,anchor=tk.W)
    #Answer4 = tk.Checkbutton(root, text=A4Text, bg=color,activebackground=color,font="Constantia 25",variable=FourthAnswer)
    #canvas.create_window(xElement * 10, yElement * 65, window=Answer4,anchor=tk.W)

global question_num
global question_limit
global FirstAnswer,SecondAnswer,ThirdAnswer,FourthAnswer
FirstAnswer = tk.IntVar()
SecondAnswer = tk.IntVar()
ThirdAnswer = tk.IntVar()
FourthAnswer = tk.IntVar()

def PrintAnswers(QNum):
    print(QNum)
    print(f'1: {FirstAnswer.get()}')
    print(f'2: {SecondAnswer.get()}')
    print(f'3: {ThirdAnswer.get()}')
    print(f'4: {FourthAnswer.get()}\n')
    FirstAnswer.set(0)
    SecondAnswer.set(0)
    ThirdAnswer.set(0)
    FourthAnswer.set(0)

def GetColorByStyle(style):
    if style == "Blue":
        return "#4e76bf"
    elif style == "Pink":
        return "#bf4e7f"
    elif style == "Green":
        return "#469e48"

answers = []

#def select_topic(topic):
#    global selected_topic_id
#    selected_topic_id = topic
#    display_questions(selected_topic_id)

#def display_questions(topic_id):
#    global answers, current_question_index
#    clear_questions()

    # Загрузить вопросы только для выбранной темы
#    if not load_questions(topic_id):
#        return

    # Отобразить текущий вопрос
#    if current_question_index < len(questions):
#        question = questions[current_question_index]
#        print("Debug: Current question:", question)
#        if 'answer_true' not in question or 'answer_false_1' not in question \
#                or 'answer_false_2' not in question or 'answer_false_3' not in question:
#            print("Ошибка: Не найдены варианты ответов для текущего вопроса.")
#            return

#        question_label = tk.Label(root, text=f"Вопрос {current_question_index + 1}: {question['question_text']}")
#        question_label.pack()

        # Создать список ответов
#        answer_options = [
 #           question['answer_true'],
  #          question['answer_false_1'],
   #         question['answer_false_2'],
    #        question['answer_false_3']
     #   ]

        # Создать переменные IntVar для хранения состояния каждого Checkbutton
      #  answer_vars = [tk.IntVar() for _ in range(len(answer_options))]

        # Отобразить варианты ответов с помощью Checkbutton
       # for j, (answer_text, answer_var) in enumerate(zip(answer_options, answer_vars)):
        #    answer_checkbox = tk.Checkbutton(root, text=answer_text, variable=answer_var, onvalue=1, offvalue=0)
        #    answer_checkbox.pack(anchor="w")

        # Создать кнопку "Ответить"
        #submit_button = tk.Button(root, text="Ответить", command=lambda vars=answer_vars: submit_answer(vars))
        #submit_button.pack()

        # Создать кнопку "Следующий вопрос"
        #next_button = tk.Button(root, text="Следующий вопрос", command=next_question)
        #next_button.pack()

        # Создать кнопку "Назад"
        #if current_question_index > 0:
        #    previous_button = tk.Button(root, text="Назад", command=previous_question)
        #    previous_button.pack()
    #else:
    #    print("Вопросы закончились")

        # После завершения всех вопросов отправляем все ответы на проверку
     #   submit_all_answers()
      #  start_window_1()

# Функция для сохранения ответов
def submit_answer():
    global current_question_index, answer_vars
    # Получить выбранные пользователем ответы
    selected_answers = [var.get() for var in answer_vars]
    print(f"Ответ на вопрос {current_question_index + 1}: {selected_answers}")

    # Проверяем наличие нужных ключей в вопросе
    question = questions[current_question_index]
    if 'answer_true' in question and len(question['answer_true']) > 0:
        answer_options = [
            question['answer_true'],
            question['answer_false_1'],
            question['answer_false_2'],
            question['answer_false_3']
        ]
        answer_text = answer_options[selected_answers.index(1)] if 1 in selected_answers else ""
        # Сохраняем ответ
        answers.append({
            'question_id': question['id'],
            'answer_text': answer_text
        })
    else:
        print("Ошибка: Не найдены варианты ответов для текущего вопроса.")

# Функция для отправки всех ответов на сервер
def submit_all_answers():
    url = 'http://localhost:8000/submit_answers/'
    data = {'answers': answers}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        result = response.json()
        score = result.get('score', 0)
        message = result.get('message', '')
        print(f"Все ответы успешно отправлены! Очки: {score}. {message}")
        #finish_window(score) # Вызываем finish_window() после получения результатов

        # Отобразить количество набранных очков на экране
        score_label = tk.Label(root, text=f"Вы набрали: {score} очков.")
        score_label.pack()
        return round(score)
    else:
        print("Ошибка при отправке ответов:", response.status_code)
    return

#def next_question():
#    global current_question_index
#   current_question_index += 1
#    display_questions(selected_topic_id)

#def previous_question():
#    global current_question_index
#    if current_question_index > 0:
#        current_question_index -= 1
#        display_questions(selected_topic_id)

#def clear_questions():
#    for widget in root.winfo_children():
#        widget.destroy()

def map_window(id):#Окно для карты приложения #ИЗМЕНЕНО 
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["mapPhoto"])
    canvas.create_image(ChudoCordsStorage[id][0], ChudoCordsStorage[id][1],anchor=tk.NW, image=PhotoStorage[style]["chudoPhoto"])

def creators_window():
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["creatorsPhoto"])

def registration_user():
    global login_entry
    global password_entry
    global email_entry
    global registration
    
    login = login_entry.get()
    password = password_entry.get()
    email = email_entry.get()
    url = "http://localhost:8000/v/auth/users/"
    data = {
        "username": login,
        "password": password,
        "email": email
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Успешная регистрация!")
        registration = True
        return True
    else:
        print("Ошибка при регистрации:", response.text)
        registration = False
        return False

def registration_window():
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["registrationPhoto"])
    global login_entry
    global password_entry
    global email_entry

    # Создание виджета для ввода текста
    login_entry = tk.Entry(root, background='#B3B6D5', width=round(xElement * 0.8), font='Constantia 30')
    password_entry = tk.Entry(root, background='#B3B6D5', width=round(xElement * 0.8), font='Constantia 30', show='*')
    email_entry = tk.Entry(root, background='#B3B6D5', width=round(xElement * 0.8), font='Constantia 30')

    # Расположение виджетов на холсте, затем приравниваем созданное окно, чтобы при листании удалять
    canvas.create_window(xElement * 51, yElement * 54.2, window=login_entry)
    canvas.create_window(xElement * 51, yElement * 67.7, window=password_entry)
    canvas.create_window(xElement * 51, yElement * 40.7, window=email_entry)
    return

def login_user():
    global login_widget
    global password_widget
    global authenticated
    login = login_widget.get()
    password = password_widget.get()
    
    url = "http://localhost:8000/auth/token/login/"
    data = {
        "username": login,
        "password": password
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Успешная авторизация!")
        authenticated = True
        return True
    else:
        print("Ошибка при авторизации:", response.text)
        authenticated = False
        return False

def start_window_1_if_authenticated():
    if authenticated or registration:
        start_window_1()
    else:
        print("Доступ запрещен. Пожалуйста, авторизуйтесь или зарегистрируйтесь.")

def login_window():
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["loginPhoto"])
    global login_widget
    global password_widget
    login_widget = tk.Entry(root, background='#B3B6D5', width=round(xElement*0.8), font='Constantia 30')
    password_widget = tk.Entry(root, background='#B3B6D5', width=round(xElement*0.8), font='Constantia 30', show='*')
    
    canvas.create_window(xElement*51, yElement*40.7, window=login_widget)
    canvas.create_window(xElement*51, yElement*54.2, window=password_widget)

    return

def info_window(topic_id):
    canvas.delete("all")
    color = GetColorByStyle(style)
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["infoPhoto"])

    # Make the HTTP request to fetch topic information
    response = requests.get(f"http://localhost:8000/topics/{topic_id}/")
    if response.status_code == 200:
        topic_data = response.json()
        topic_title = topic_data.get('topic_title', 'Unknown Topic')
        topic_info = topic_data.get('topic_info', 'No information available')
        topic_question_number = topic_data.get('topic_question_number', 0)

        st = ScrolledText(root, width=round(xElement*7), height=round(yElement*2), font=("Arial", 20, "bold"), bg=color)
        st.insert(1.0, f"   Тема: {topic_title}\n\n{topic_info}")
        st.configure(state=tk.DISABLED)
        canvas.create_window(xElement*50, yElement*50, window=st)
    else:
        print("Failed to fetch topic information")
    #canvas.delete("all")
    #canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["infoPhoto"])
    #url = ('http://localhost:8000/topics/')
    #response = requests.get(url)
    #data = response.text
    #print(data)
    #canvas.create_text(10, 10, font="Arial 14", anchor=NW, text=data, fill="#004D40")

def start_window_1():
    if not authenticated and not registration:
        print("Доступ запрещен. Пожалуйста, авторизуйтесь.")
        return
    else:
        canvas.delete("all")
        canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["mainPhoto"])

root.bind("<Button-1>", ManageButton)
root.bind("<Escape>",ManageEscape)
# Запускаем главный цикл событий

root.mainloop()

'''
    # Проверяем статус авторизации перед отображением основного окна
    if not authenticated and not registration:
        print("Доступ запрещен. Пожалуйста, авторизуйтесь.")
        return
    else:
        # Отображаем основное окно приложения
'''