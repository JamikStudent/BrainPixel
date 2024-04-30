import tkinter as tk
from PIL import Image, ImageTk, ImageEnhance
from tkinter import ttk
from shopp import *
import requests
from test import *

user1 = User()

# Создаем окно
root = tk.Tk()
# включаем полный экран
root.attributes("-fullscreen", True)
root.title("Brain Pixel")


# Получаем размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

#Переменная отвечающая за скин в настоящее время
global style
style = "Base"

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
            return True
        else:
            return False

def MakePhoto(name): #Функция загрузки фоток
    # Загружаем изображение
    image = Image.open(name)

    # Масштабируем изображение до размеров экрана
    image = image.resize((screen_width, screen_height), Image.ADAPTIVE)

    #image = ImageEnhance.Sharpness(image)
    #image = ImageEnhance.Brightness(image)
    #image = image.enhance(0.1)

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
MapButton = {"StartGame": {#Название кнопки
                "Login": True #Кнопки, к которым ведёт данная кнопка
            },
            "Login":{#Тут по аналогии
                "Registration": False,
                "Main": False
            },
            "Registration":{
                "Login": False,
                "Main": False
            },
             "Main": {
                 "Creators": False,
                 "Shop": False,
                 "Start": False,
                 "Settings": False,
                 "Map": False,
                 "Exit": False
                    },
             "Creators": {
                 "Back": False
             },
             "Shop": {
                 "Back": False,
                 "Earn": False,
                 "BuyFirstTip": False,
                 "BuySecondTip": False,
                 "BuySkin": False
             },
             "Start": {
                 "Back": False,
                 "Test": False
             },
             "Test":{
               "Finish": False
             },
             "Finish": {
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
                 "Back": False
             }
            }

PhotoStorage = {
    "Base":{
        "startPhoto": MakePhoto("image/start_page.png"),
        "mainPhoto": 1,
        "creatorsPhoto": 1,
        "mapPhoto": 1,
        "infoPhoto": 1,
        "testPhoto": 1,
        "settingsPhoto" : 1,
        "settingsBackPhoto":1,
        "shopPhoto" : 1,
        "helpPhoto" : 1,
        "finishPhoto" : 1,
        "loginPhoto" : 1,
        "registrationPhoto" : 1,
        "choosePhoto": 1
    },
    "Pink":{
        "mainPhoto" : 1,
        "creatorsPhoto" : 1,
        "mapPhoto" : 1,
        "infoPhoto" : 1,
        "testPhoto" : 1,
        "settingsPhoto" : 1,
        "settingsBackPhoto":1,
        "shopPhoto" : 1,
        "helpPhoto" : 1,
        "finishPhoto" : 1,
        "loginPhoto" : 1,
        "registrationPhoto" : 1,
        "choosePhoto": 1
    },
    "Green":{
        "mainPhoto" : 1,
        "creatorsPhoto" : 1,
        "mapPhoto" : 1,
        "infoPhoto" : 1,
        "testPhoto" : 1,
        "settingsPhoto" : 1,
        "settingsBackPhoto":1,
        "shopPhoto" : 1,
        "helpPhoto" : 1,
        "finishPhoto" : 1,
        "loginPhoto" : 1,
        "registrationPhoto" : 1,
        "choosePhoto": 1
    }
}

def LoadPhotoStorage():
        PhotoStorage["Base"]["mainPhoto"] = MakePhoto("image/main.png")
        PhotoStorage["Base"]["creatorsPhoto"] = MakePhoto("image/creators.png")
        PhotoStorage["Base"]["mapPhoto"] = MakePhoto("image/map.png")
        PhotoStorage["Base"]["infoPhoto"] = MakePhoto("image/info.png")
        PhotoStorage["Base"]["testPhoto"] = MakePhoto("image/test.png")
        PhotoStorage["Base"]["settingsPhoto"] = MakePhoto("image/settings.png")
        PhotoStorage["Base"]["settingsBackPhoto"] = MakePhotoBack("image/settings.png")
        PhotoStorage["Base"]["shopPhoto"] = MakePhoto("image/shop.png")
        PhotoStorage["Base"]["helpPhoto"] = MakePhoto("image/spravka.png")
        PhotoStorage["Base"]["finishPhoto"] = MakePhoto("image/0ball.png")
        PhotoStorage["Base"]["loginPhoto"] = MakePhoto("image/vkhod.png")
        PhotoStorage["Base"]["registrationPhoto"] = MakePhoto("image/registratsia.png")
        PhotoStorage["Base"]["choosePhoto"] = MakePhoto("image/skin.png")

        PhotoStorage["Pink"]["mainPhoto"] = MakePhoto("image/mainpink.png")
        PhotoStorage["Pink"]["creatorsPhoto"] = MakePhoto("image/creatorspink.png")
        PhotoStorage["Pink"]["mapPhoto"] = MakePhoto("image/mappink.png")
        PhotoStorage["Pink"]["infoPhoto"] = MakePhoto("image/infopink.png")
        PhotoStorage["Pink"]["testPhoto"] = MakePhoto("image/testpink.png")
        PhotoStorage["Pink"]["settingsPhoto"] = MakePhoto("image/settingspink.png")
        PhotoStorage["Pink"]["settingsBackPhoto"] = MakePhotoBack("image/settingspink.png")
        PhotoStorage["Pink"]["shopPhoto"] = MakePhoto("image/shoppink.png")
        PhotoStorage["Pink"]["helpPhoto"] = MakePhoto("image/spravkapink.png")
        PhotoStorage["Pink"]["finishPhoto"] = MakePhoto("image/0ballpink.png")
        PhotoStorage["Pink"]["loginPhoto"] = MakePhoto("image/vkhodpink.png")
        PhotoStorage["Pink"]["registrationPhoto"] = MakePhoto("image/registratsiapink.png")
        PhotoStorage["Pink"]["choosePhoto"] = MakePhoto("image/skinpink.png")

        PhotoStorage["Green"]["mainPhoto"] = MakePhoto("image/maingreen.png")
        PhotoStorage["Green"]["creatorsPhoto"] = MakePhoto("image/creatorsgreen.png")
        PhotoStorage["Green"]["mapPhoto"] = MakePhoto("image/mapgreen.png")
        PhotoStorage["Green"]["infoPhoto"] = MakePhoto("image/infogreen.png")
        PhotoStorage["Green"]["testPhoto"] = MakePhoto("image/testgreen.png")
        PhotoStorage["Green"]["settingsPhoto"] = MakePhoto("image/settingsgreen.png")
        PhotoStorage["Green"]["settingsBackPhoto"] = MakePhotoBack("image/settingsgreen.png")
        PhotoStorage["Green"]["shopPhoto"] = MakePhoto("image/shopgreen.png")
        PhotoStorage["Green"]["helpPhoto"] = MakePhoto("image/spravkagreen.png")
        PhotoStorage["Green"]["finishPhoto"] = MakePhoto("image/0ballgreen.png")
        PhotoStorage["Green"]["loginPhoto"] = MakePhoto("image/vkhodgreen.png")
        PhotoStorage["Green"]["registrationPhoto"] = MakePhoto("image/registratsiagreen.png")
        PhotoStorage["Green"]["choosePhoto"] = MakePhoto("image/skingreen.png")

LoadPhotoStorage()

# процентные координаты, х и у - один процент от длины своей координаты
xElement = screen_width * 0.01
yElement = screen_height * 0.01

# Создаем холст (Canvas)
canvas = tk.Canvas(root, width=screen_width, height=screen_height,highlightthickness=0)
canvas.pack()

val = 0
#Виджеты для ввода информации о пользователе
global login_widget
global password_widget
global username_widget

#Виджет для ползунка громкости
global win
def update_slider(value):
    # Функция обновления, которая будет вызываться при изменении положения ползунка
    global val
    val = value

# Устанавливаем изображение как фон холста
canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["startPhoto"])

#Функция для смены состояния кнопок - Используется, когда нажимаем на кнопку
def ChangeMapButton(name):
    for i in MapButton[name]:
        MapButton[name][i] = not MapButton[name][i]


def ManageEscape(event):
    exit()

# функция, принимающая координаты клика
def ManageButton(event):
    global win
    global login_widget
    global password_widget
    global username_widget
    global style
    global user_id
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
    MapBackButton = MyButton(xElement * 2.6, yElement * 8.5,xElement * 16.1, yElement * 16.9,"Back","Map","Main")
    StartBackButton = MyButton(xElement * 3, yElement * 6.2, xElement * 14.8, yElement * 13.2,"Back","Start","Main")
    StartTestButton = MyButton(xElement * 39.7, yElement * 88.4,xElement * 60.3, yElement * 96,"Test","Start","Test")
    TestFinishButton = MyButton(xElement * 33, yElement * 86.8, xElement * 62.2, yElement * 97.7,"Finish","Test","Finish")
    FinishBackButton = MyButton(xElement * 34.8, yElement * 66.7, xElement * 65.6, yElement * 83.5, "Back","Finish", "Main")
    ShopBackButton = MyButton(xElement * 4.2, yElement * 7.3, xElement * 15.9, yElement * 14.2, "Back","Shop","Main")
    ShopBuyFirstTipButton = MyButton(xElement * 11, yElement * 73.2, xElement * 22, yElement * 78.2, "BuyFirstTip","Shop","Shop")
    ShopBuySkinButton = MyButton(xElement * 77.9, yElement * 73.1, xElement * 89, yElement * 78.2, "BuySkin","Shop","Shop")
    ShopBuySecondTipButton = MyButton(xElement * 44.7, yElement * 73,xElement * 55.8, yElement * 78.2,"BuySecondTip","Shop","Shop")
    ShopEarnButton = MyButton(xElement * 76.8, yElement * 15, xElement * 98.4, yElement * 25.2,"Earn","Shop", "Shop")
    SettingsBackButton = MyButton(xElement * 3.5, yElement * 6.4, xElement * 15.1, yElement * 13.2, "Back","Settings","Main")
    SettingsHelpButton = MyButton(xElement * 62.8, yElement * 56, xElement * 90.2, yElement * 70.8, "Help","Settings","Help")
    SettingsChangeSkinButton = MyButton(xElement * 62.8, yElement * 75.5, xElement * 90.2, yElement * 90.5, "ChangeSkin","Settings","ChangeSkin")
    HelpBackButton = MyButton(xElement * 3.6, yElement * 5.9, xElement * 15.2, yElement * 12.6, "Back","Help","Settings")
    BaseSkinButton = MyButton(xElement*59,yElement*39.1,xElement*79.3,yElement*49.9,"BaseSkin","ChangeSkin","ChangeSkin")
    PinkSkinButton = MyButton(xElement * 59, yElement * 55.6, xElement * 79.3, yElement * 66.4,"PinkSkin","ChangeSkin","ChangeSkin")
    GreenSkinButton = MyButton(xElement * 59, yElement * 72.2, xElement * 79.3, yElement * 83.1,"GreenSkin","ChangeSkin","ChangeSkin")
    ChangeSkinBackButton = MyButton(xElement * 84.4, yElement * 29.2, xElement * 90.4, yElement * 38.5,"Back","ChangeSkin","Settings")

    # Проверяем, попадает ли координата нажатия мыши в заданную область

    # если точка в зоне кнопки
    if StartGameButton.wasClicked(event.x, event.y):
        login_window()
    elif RegistrationButton.wasClicked(event.x, event.y):
        canvas.delete(login_widget)
        canvas.delete(password_widget)
        registration_window()
    elif LoginButton.wasClicked(event.x, event.y):
        canvas.delete(login_widget)
        canvas.delete(password_widget)
        canvas.delete(username_widget)
        login_window()
    elif RegistrationMainButton.wasClicked(event.x, event.y):
        canvas.delete(login_widget)
        canvas.delete(password_widget)
        canvas.delete(username_widget)
        start_window_1()
    elif LoginMainButton.wasClicked(event.x, event.y):
        canvas.delete(login_widget)
        canvas.delete(password_widget)
        start_window_1()
    elif CreatorsButton.wasClicked(event.x, event.y):
        creators_window()
    elif CreatorsBackButton.wasClicked(event.x,event.y):
        start_window_1()
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
    elif MainMapButton.wasClicked(event.x, event.y):
        map_window()
    elif MapBackButton.wasClicked(event.x, event.y):
        start_window_1()
    elif MainStartButton.wasClicked(event.x, event.y):
        info_window()
    elif StartTestButton.wasClicked(event.x, event.y):
        test_window()
    elif TestFinishButton.wasClicked(event.x, event.y):
        finish_window()
    elif FinishBackButton.wasClicked(event.x , event.y):
        start_window_1()
    elif StartBackButton.wasClicked(event.x, event.y):
        start_window_1()
    elif ExitButton.wasClicked(event.x,event.y):
        exit()
    elif ShopBuySkinButton.wasClicked(event.x, event.y):
        canvas.delete("all")
        canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["shopPhoto"])
        user_id = 1
        skin_name = 'pink'
        buy_skin_url = f'http://localhost:8000/users/{user_id}/buy_skin/{skin_name}/'
        response = requests.post(buy_skin_url)
        if response.status_code == 200:
            data = response.json()
            user1.set_count_of_money(data['balance'])
            canvas.create_text(xElement * 84.5, yElement * 8, text=user1.get_count_of_money(), font="Impact 40")
        else:
            print("Error:", response.status_code)
        update_user_data()
        
    elif ShopEarnButton.wasClicked(event.x, event.y):
        user1.Earn()
        shop_window(0, None)

    elif ShopBuyFirstTipButton.wasClicked(event.x, event.y):
        user_id = 1
        shop_window(user_id, 'first')
    elif ShopBuySecondTipButton.wasClicked(event.x, event.y):
        user_id = 1
        shop_window(user_id, 'second')

    elif ShopBackButton.wasClicked(event.x, event.y):
        start_window_1()
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

def skin_window(user_skins):
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["settingsBackPhoto"])
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["choosePhoto"])

    # Создание кнопок для выбора скинов
    button_y = yElement * 10
    for skin_name, has_skin in user_skins.items():
        if has_skin:
            button = tk.Button(root, text=skin_name.capitalize(), command=lambda name=skin_name: change_skin(name))
            button.place(x=xElement * 20, y=button_y)
            button_y += yElement * 5
    #canvas.create_rectangle(xElement*59,yElement*39.1,xElement*79.3,yElement*49.9,fill="#80CBC4", outline="#004D40")
    #canvas.create_rectangle(xElement * 59, yElement * 55.6, xElement * 79.3, yElement * 66.4, fill="#80CBC4", outline="#004D40")
    #canvas.create_rectangle(xElement * 59, yElement * 72.2, xElement * 79.3, yElement * 83.1, fill="#80CBC4", outline="#004D40")
    #canvas.create_rectangle(xElement * 84.4, yElement * 29.2, xElement * 90.4, yElement * 38.5, fill="#80CBC4",outline="#004D40")
    return

def change_skin(skin_name):
    user_id = 1  # Замените это на реальный идентификатор пользователя

    # Отправка POST-запроса на сервер для изменения скина пользователя
    change_skin_url = f'http://localhost:8000/users/{user_id}/change_skin/{skin_name}/'
    response = requests.post(change_skin_url)
    if response.status_code == 200:
        print(f"Successfully changed skin to {skin_name}.")
    else:
        print("Error:", response.status_code)


def finish_window():
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["finishPhoto"])
    return
def settings_window():
    global win
    global val
    canvas.delete("all")

    # Отправка GET-запроса на сервер для получения информации о скинах пользователя
    user_id = 1  # Замените это на реальный идентификатор пользователя
    skin_info_url = f'http://localhost:8000/users/{user_id}/skin_info/'
    response = requests.get(skin_info_url)
    if response.status_code == 200:
        user_skins = response.json()
    else:
        print("Error:", response.status_code)
        user_skins = {}

    # Создание ползунка
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["settingsPhoto"])
    slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=update_slider,length=xElement*20)
    slider.set(val)
    slider.pack()
    canvas.update()

    # Размещение ползунка на холсте
    win = canvas.create_window(xElement*77, yElement*45, anchor=tk.CENTER, window=slider)
    canvas.pack()
    slider.pack_forget()
    canvas.pack()

    return

def help_window():
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["helpPhoto"])
    return
def test_window():
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["testPhoto"])
    return

def map_window():
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["mapPhoto"])

def creators_window():
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["creatorsPhoto"])

def registration_window():
    canvas.delete("all")
    global login_widget
    global password_widget
    global username_widget
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["registrationPhoto"])

    # Создание виджета для ввода текста
    login_widget = tk.Entry(root, background='#B3B6D5', width=round(xElement * 0.8), font='Constantia 30')
    password_widget = tk.Entry(root, background='#B3B6D5', width=round(xElement * 0.8), font='Constantia 30',show='*')
    username_widget = tk.Entry(root, background='#B3B6D5', width=round(xElement * 0.8), font='Constantia 30')

    #Расположение виджетов на холсте, затем приравниваем созданное окно, чтобы при листании удалять
    login_widget = canvas.create_window(xElement * 51, yElement * 54.2, window=login_widget)
    password_widget = canvas.create_window(xElement * 51, yElement * 67.7, window=password_widget)
    username_widget = canvas.create_window(xElement * 51, yElement * 40.7, window=username_widget)
    return
def login_window():
    canvas.delete("all")
    global login_widget
    global password_widget
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["loginPhoto"])

    login_widget = tk.Entry(root, background='#B3B6D5',width=round(xElement*0.8),font = 'Constantia 30')
    password_widget = tk.Entry(root, background='#B3B6D5',width=round(xElement*0.8),font = 'Constantia 30',show='*')
    login_widget = canvas.create_window(xElement*51, yElement*40.7, window=login_widget)
    password_widget = canvas.create_window(xElement * 51, yElement * 54.2, window=password_widget)

    # Функция, которая будет вызываться при нажатии кнопки "Вход"
    def login():
        # Получение введенных пользователем логина и пароля
        login = login_widget.get()
        password = password_widget.get()

        # URL для отправки запроса на сервер
        url = 'http://localhost:8000/auth/'

        # Параметры запроса (в данном случае логин и пароль)
        data = {'login': login, 'password': password}

        # Отправка POST запроса на сервер
        response = requests.post(url, json=data)

        # Печать ответа сервера
        print(response.text)

    return
def info_window():
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["infoPhoto"])

def start_window_1():
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=PhotoStorage[style]["mainPhoto"])

root.bind("<Button-1>", ManageButton)
root.bind("<Escape>",ManageEscape)
# Запускаем главный цикл событий

root.mainloop()