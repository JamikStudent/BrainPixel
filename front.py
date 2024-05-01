import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from shopp import *

user1 = User(100,0,0,0)



def MakePhoto(name):
    # Загружаем изображение
    image = Image.open(name)

    # Масштабируем изображение до размеров экрана
    image = image.resize((screen_width, screen_height), Image.ADAPTIVE)

    # Создаем изображение Tkinter
    image = ImageTk.PhotoImage(image)
    return image

# Словарь для кнопок
MapButton = {"StartGame": True,
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
             "Help": {
                 "Back": False
             },
             "Map": {
                 "Back" :False
             }
            }

# Создаем окно
root = tk.Tk()
# включаем полный экран
root.attributes("-fullscreen", True)
root.title("Brain Pixel")

# Получаем размеры экрана
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# процентные координаты, х и у - один процент от длины своей координаты
xElement = screen_width * 0.01
yElement = screen_height * 0.01

# Создаем изображение Tkinter
photo = MakePhoto("start_page.png")
photo1 = MakePhoto("page_2.png")
creatorsPhoto = MakePhoto("creators.png")
mapPhoto = MakePhoto("map.png")
infoPhoto = MakePhoto("info.png")
testPhoto = MakePhoto("test.png")
endTestPhoto = MakePhoto("0ball.png")
settingsPhoto = MakePhoto("settings.png")
shopPhoto = MakePhoto("shop.png")
helpPhoto = MakePhoto("spravka.png")
finishPhoto = MakePhoto("0ball.png")

# Создаем холст (Canvas)
canvas = tk.Canvas(root, width=screen_width, height=screen_height,highlightthickness=0)
canvas.pack()

val = 0
global win
def update_slider(value):
    # Функция обновления, которая будет вызываться при изменении положения ползунка
    global val
    val = value



# Устанавливаем изображение как фон холста
canvas.create_image(0, 0, anchor=tk.NW, image=photo)

def ChangeMapButton(name):
    for i in MapButton[name]:
        MapButton[name][i] = not MapButton[name][i]

# функция, принимающая координаты клика
def ManageButton(event):
    global win
    xStart, yStart = xElement * 75.2, yElement * 39.7   # координата левого верхнего угла
    xStart_, yStart_ = xElement * 14 + xStart, yElement * 22 + yStart # координата правого нижнего угла

    xMainCreators, yMainCreators = xElement*3.2, yElement*27.8
    xMainCreators_, yMainCreators_ = xElement*18.6, yElement*74.8

    xMainShop, yMainShop = xElement * 21.2, yElement * 27.8
    xMainShop_, yMainShop_ = xElement * 37.3, yElement * 74.8

    xMainStart, yMainStart = xElement * 41.1, yElement * 27.8
    xMainStart_, yMainStart_ = xElement * 57.4, yElement * 74.8

    xMainSettings, yMainSettings = xElement * 61.5, yElement * 27.8
    xMainSettings_, yMainSettings_ = xElement * 76.6, yElement * 74.8

    xMainMap, yMainMap = xElement * 80.4, yElement * 27.8
    xMainMap_, yMainMap_ = xElement * 96.5, yElement * 74.8

    xMainExit, yMainExit = xElement * 80.6, yElement * 11.8
    xMainExit_ , yMainExit_ = xElement * 97.4, yElement * 17.5

    xMainCreatorsBack, yMainCreatorsBack = xElement * 4.5, yElement * 6.5
    xMainCreatorsBack_, yMainCreatorsBack_ = xElement * 16.6, yElement * 13.6

    xMainMapBack, yMainMapBack = xElement * 2.6, yElement * 8.5
    xMainMapBack_, yMainMapBack_ = xElement * 16.1, yElement * 16.9

    xMainStartBack, yMainStartBack = xElement * 3, yElement * 6.2
    xMainStartBack_, yMainStartBack_ = xElement * 14.8, yElement * 13.2

    xMainStartTest, yMainStartTest = xElement * 39.7, yElement * 88.4
    xMainStartTest_, yMainStartTest_ = xElement * 60.3, yElement * 96

    xMainStartTestFinish, yMainStartTestFinish = xElement * 33, yElement * 86.8
    xMainStartTestFinish_, yMainStartTestFinish_ = xElement * 62.2, yElement * 97.7

    xMainStartTestFinishBack, yMainStartTestFinishBack = xElement * 34.8, yElement * 66.7
    xMainStartTestFinishBack_, yMainStartTestFinishBack_ = xElement * 65.6, yElement * 83.5

    xMainShopBack, yMainShopBack = xElement * 4.2, yElement * 7.3
    xMainShopBack_, yMainShopBack_ = xElement * 15.9, yElement * 14.2

    xMainShopBuyFirstTip,yMainShopBuyFirstTip = xElement * 11, yElement * 73.2
    xMainShopBuyFirstTip_, yMainShopBuyFirstTip_ = xElement * 22, yElement * 78.2

    xMainShopBuySkin, yMainShopBuySkin = xElement * 77.9, yElement * 73.1
    xMainShopBuySkin_, yMainShopBuySkin_ = xElement * 89, yElement * 78.2

    xMainShopBuySecondTip, yMainShopBuySecondTip = xElement * 44.7, yElement * 73
    xMainShopBuySecondTip_, yMainShopBuySecondTip_ = xElement * 55.8, yElement * 78.2

    xMainShopEarn, yMainShopEarn =xElement * 76.8, yElement * 15
    xMainShopEarn_ ,yMainShopEarn_ = xElement * 98.4, yElement * 25.2

    xMainSettingsBack, yMainSettingsBack = xElement * 3.5, yElement * 6.4
    xMainSettingsBack_, yMainSettingsBack_ = xElement * 15.1, yElement * 13.2

    xMainSettingsHelp, yMainSettingsHelp = xElement * 62.8, yElement * 56
    xMainSettingsHelp_, yMainSettingsHelp_ = xElement * 90.2, yElement * 70.8

    xMainSettingsHelpBack, yMainSettingsHelpBack = xElement * 3.6, yElement * 5.9
    xMainSettingsHelpBack_, yMainSettingsHelpBack_ = xElement * 15.2, yElement * 12.6
    # Проверяем, попадает ли координата нажатия мыши в заданную область

    # если точка в зоне кнопки
    if xStart <= event.x <= xStart_ and yStart <= event.y <= yStart_ and MapButton.get("StartGame") == True :
        MapButton["StartGame"] = False
        ChangeMapButton("Main")
        start_window_1()

    elif xMainCreators <= event.x <= xMainCreators_ and yMainCreators <= event.y <= yMainCreators_ and (MapButton.get("Main")).get("Creators") == True:
        ChangeMapButton("Main")
        ChangeMapButton("Creators")
        creators_window()
    elif xMainCreatorsBack <= event.x <= xMainCreatorsBack_ and yMainCreatorsBack <= event.y <= yMainCreatorsBack_ and (MapButton.get("Creators")).get("Back") == True:
        ChangeMapButton("Main")
        ChangeMapButton("Creators")
        start_window_1()
    elif xMainShop <= event.x <= xMainShop_ and yMainShop <= event.y <= yMainShop_ and (MapButton.get("Main")).get("Shop") == True:
        ChangeMapButton("Main")
        ChangeMapButton("Shop")
        shop_window()
    elif xMainSettings <= event.x <= xMainSettings_ and yMainSettings <= event.y <= yMainSettings_ and (MapButton.get("Main")).get("Settings") == True:
        ChangeMapButton("Main")
        ChangeMapButton("Settings")
        settings_window()
    elif xMainSettingsBack <= event.x <= xMainSettingsBack_ and yMainSettingsBack <= event.y <= yMainSettingsBack_ and (MapButton.get("Settings")).get("Back") == True:
        ChangeMapButton("Main")
        ChangeMapButton("Settings")
        canvas.delete(win)
        start_window_1()
    elif xMainSettingsHelp <= event.x <= xMainSettingsHelp_ and yMainSettingsHelp <= event.y <= yMainSettingsHelp_ and (MapButton.get("Settings")).get("Help") == True:
        ChangeMapButton("Settings")
        ChangeMapButton("Help")
        canvas.delete(win)
        help_window()
    elif xMainSettingsHelpBack <= event.x <= xMainSettingsHelpBack_ and yMainSettingsHelpBack <= event.y <= yMainSettingsHelpBack_ and (MapButton.get("Help")).get("Back") == True:
        ChangeMapButton("Settings")
        ChangeMapButton("Help")
        settings_window()
    elif xMainMap <= event.x <= xMainMap_ and yMainMap <= event.y <= yMainMap_ and (MapButton.get("Main")).get("Map") == True:
        ChangeMapButton("Main")
        ChangeMapButton("Map")
        map_window()
    elif xMainMapBack <= event.x <= xMainMapBack_ and yMainMapBack <= event.y <= yMainMapBack_ and (MapButton.get("Map")).get("Back") == True:
        ChangeMapButton("Main")
        ChangeMapButton("Map")
        start_window_1()
    elif xMainStart <= event.x <= xMainStart_ and yMainStart <= event.y <= yMainStart_ and (MapButton.get("Main")).get("Start") == True:
        ChangeMapButton("Main")
        ChangeMapButton("Start")
        info_window()
    elif xMainStartTest <= event.x <= xMainStartTest_ and yMainStartTest <= event.y <= yMainStartTest_ and (MapButton.get("Start")).get("Test") == True:
        ChangeMapButton("Start")
        ChangeMapButton("Test")
        test_window()
    elif xMainStartTestFinish <= event.x <= xMainStartTestFinish_ and yMainStartTestFinish <= event.y <= yMainStartTestFinish_ and (MapButton.get("Test")).get("Finish") == True:
        ChangeMapButton("Test")
        ChangeMapButton("Finish")
        finish_window()
    elif xMainStartTestFinishBack <= event.x <= xMainStartTestFinishBack_ and yMainStartTestFinishBack <= event.y <= yMainStartTestFinishBack_ and (MapButton.get("Finish")).get("Back") == True:
        ChangeMapButton("Finish")
        ChangeMapButton("Main")
        start_window_1()
    elif xMainStartBack <= event.x <= xMainStartBack_ and yMainStartBack <= event.y <= yMainStartBack_ and (MapButton.get("Start")).get("Back") == True:
        ChangeMapButton("Main")
        ChangeMapButton("Start")
        start_window_1()
    elif xMainExit <= event.x <= xMainExit_ and yMainExit <= event.y <= yMainExit_ and (MapButton.get("Main")).get("Exit") == True:
        exit()
    elif xMainShopBuyFirstTip <= event.x <= xMainShopBuyFirstTip_ and yMainShopBuyFirstTip <= event.y <= yMainShopBuyFirstTip_ and (MapButton.get("Shop")).get("BuyFirstTip") == True:
        user1.BuyFirstTip()
        shop_window()
    elif xMainShopBuySecondTip <= event.x <= xMainShopBuySecondTip_ and yMainShopBuySecondTip <= event.y <= yMainShopBuySecondTip_ and (MapButton.get("Shop")).get("BuySecondTip") == True:
        user1.BuySecondTip()
        shop_window()
    elif xMainShopBuySkin <= event.x <= xMainShopBuySkin_ and yMainShopBuySkin <= event.y <= yMainShopBuySkin_ and (MapButton.get("Shop")).get("BuySkin") == True:
        user1.BuySkin()
        shop_window()
    elif xMainShopEarn <= event.x <= xMainShopEarn_ and yMainShopEarn <= event.y <= yMainShopEarn_ and (MapButton.get("Shop")).get("Earn") == True:
        user1.Earn()
        shop_window()
    elif xMainShopBack <= event.x <= xMainShopBack_ and yMainShopBack <= event.y <= yMainShopBack_ and (MapButton.get("Shop")).get("Back") == True:
        ChangeMapButton("Main")
        ChangeMapButton("Shop")
        start_window_1()
    else:
        return

def shop_window():
    canvas.create_image(0, 0, anchor=tk.NW, image=shopPhoto)
    canvas.create_text(xElement*84.5,yElement*8,text=user1.GetCountOfMoney(),font="Impact 40")
    #canvas.create_rectangle(xElement * 4.2, yElement * 7.3, xElement * 15.9, yElement * 14.2, fill="#80CBC4",
    #                        outline="#004D40")
    #canvas.create_rectangle(xElement * 4.2, yElement * 7.3, xElement * 15.9, yElement * 14.2, fill="#80CBC4",                        outline="#004D40")
    #canvas.create_rectangle(xElement * 11, yElement * 73.2, xElement * 22, yElement * 78.2, fill="#80CBC4",
    #                     outline="#004D40")
    #canvas.create_rectangle(xElement * 44.7, yElement * 73, xElement * 55.8, yElement * 78.2, fill="#80CBC4",
     #                       outline="#004D40")
    #canvas.create_rectangle(xElement * 77.9, yElement * 73.1, xElement * 89, yElement * 78.2, fill="#80CBC4",
     #                      outline="#004D40")
    #canvas.create_rectangle(xElement * 76.8, yElement * 15, xElement * 98.4, yElement * 25.2, fill="#80CBC4",
     #                  outline="#004D40")
    return
def finish_window():
    canvas.create_image(0, 0, anchor=tk.NW, image=finishPhoto)
    #canvas.create_rectangle(xElement * 34.8, yElement * 66.7, xElement * 65.6, yElement * 83.5, fill="#80CBC4",outline="#004D40")
    return
def settings_window():
    global win
    global val
    canvas.create_image(0, 0, anchor=tk.NW, image=settingsPhoto)
    slider = tk.Scale(root, from_=0, to=100, orient=tk.HORIZONTAL, command=update_slider,length=xElement*20)
    slider.set(val)
    slider.pack()
    canvas.update()

    # Размещение ползунка на холсте
    win = canvas.create_window(xElement*77, yElement*45, anchor=tk.CENTER, window=slider)
    canvas.pack()
    slider.pack_forget()
    canvas.pack()

    #canvas.create_rectangle(xElement * 3.5, yElement * 6.4, xElement * 15.1, yElement * 13.2, fill="#80CBC4", outline="#004D40")
    #canvas.create_rectangle(xElement * 62.8, yElement * 56, xElement * 90.2, yElement * 70.8, fill="#80CBC4",                        outline="#004D40")
    return

def help_window():
    canvas.create_image(0, 0, anchor=tk.NW, image=helpPhoto)
    #canvas.create_rectangle(xElement * 3.6, yElement * 5.9, xElement * 15.2, yElement * 12.6, fill="#80CBC4",outline="#004D40")
    return
def test_window():
    canvas.create_image(0, 0, anchor=tk.NW, image=testPhoto)
    #canvas.create_rectangle(xElement * 33, yElement * 86.8, xElement * 62.2, yElement * 97.7, fill="#80CBC4",outline="#004D40")
    return

def map_window():
    canvasMap = tk.Canvas(root, width=screen_width, height=screen_height)
    canvasMap.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=mapPhoto)
    #canvas.create_rectangle(xElement * 2.6, yElement * 8.5, xElement * 16.1, yElement * 16.9, fill="#80CBC4",outline="#004D40")

def creators_window():
    canvasCreators = tk.Canvas(root, width=screen_width, height=screen_height,highlightthickness=0)
    canvasCreators.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=creatorsPhoto)
    #canvas.create_rectangle(xElement * 4.5, yElement * 6.5, xElement * 16.6, yElement * 13.6, fill="#80CBC4",
     #                       outline="#004D40")
def info_window():
    canvas.create_image(0, 0, anchor=tk.NW, image=infoPhoto)
    #canvas.create_rectangle(xElement * 3, yElement * 6.2, xElement * 14.8, yElement * 13.2, fill="#80CBC4",
     #                       outline="#004D40")
    #canvas.create_rectangle(xElement * 39.7, yElement * 88.4, xElement * 60.3, yElement * 96, fill="#80CBC4",outline="#004D40")
def start_window_1():
    canvas.create_image(0, 0, anchor=tk.NW, image=photo1)

    #canvas.create_rectangle(xElement*3.2, yElement*27.8, xElement*18.6, yElement*74.8, fill="#80CBC4", outline="#004D40")

    #canvas.create_rectangle(xElement * 3.2 + xElement*18, yElement * 27.8, xElement * 18.6+ xElement*18.7, yElement * 74.8, fill="#80CBC4",
     #                       outline="#004D40")
    #canvas.create_rectangle(xElement * 41.1, yElement * 27.8, xElement * 57.4,
     #                       yElement * 74.8, fill="#80CBC4",
      #                      outline="#004D40")
    #canvas.create_rectangle(xElement * 61.5, yElement * 27.8, xElement * 76.6,
     #                       yElement * 74.8, fill="#80CBC4",
      #                      outline="#004D40")
    #canvas.create_rectangle(xElement * 80.4, yElement * 27.8, xElement * 96.5,
     #                       yElement * 74.8, fill="#80CBC4",
      #                      outline="#004D40")

    #canvas.create_rectangle(xElement * 80.6, yElement * 11.8, xElement * 97.4,
     #                       yElement * 17.5, fill="#80CBC4",
      #                      outline="#004D40")

root.bind("<Button-1>", ManageButton)
# Запускаем главный цикл событий
root.mainloop()
