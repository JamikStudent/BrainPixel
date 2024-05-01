# TO-DO Что делать с переменными цен подсказок

CostOfFirstTip = 50
CostOfSecondTip = 100
CostOfSkin = 150


class User:
    # Инициализация человечка
    def __init__(self, CountOfMoney, CountOfFirstTips, CountOfSecondTips, CountOfSkins):
        self.CountOfMoney = CountOfMoney
        self.CountOfFirstTips = CountOfFirstTips
        self.CountOfSecondTips = CountOfSecondTips
        self.CountOfSkins = CountOfSkins

    # Покупка 1 подсказки
    def BuyFirstTip(self):
        if (self.CountOfMoney >= CostOfFirstTip):
            self.CountOfMoney -= CostOfFirstTip
            self.CountOfFirstTips += 1
            return True
        else:
            return False


    # Покупка 2 подсказки
    def BuySecondTip(self):
        if (self.CountOfMoney >= CostOfSecondTip):
            self.CountOfMoney -= CostOfSecondTip
            self.CountOfSecondTips += 1
            return True
        else:
            return False

    # Покупка 3 подсказки
    def BuySkin(self):
        if (self.CountOfMoney >= CostOfSkin):
            self.CountOfMoney -= CostOfSkin
            self.CountOfSkins += 1
            return True
        else:
            return False
    def GetCountOfMoney(self):
        return self.CountOfMoney
    def Earn(self):
        self.CountOfMoney+= 50

# Функция покупки 1 - 3 подсказок
def BuyFirstTip(user):
    if (user.CountOfMoney >= CostOfFirstTip):
        user.BuyFirstTip()
        return True
    else:
        return False

def BuySecondTip(user):
    if(user.CountOfMoney >= CostOfSecondTip):
        user.BuySecondTip()
        return True
    else:
        return False

def BuySkin(user):
    if(user.CountOfMoney >= CostOfSkin):
        user.BuyThirdTip()
        return True
    else:
        return False

def main():
    user1 = User(100,0,0,0)
    user2 = User(5,0,0,0)

    if(BuyFirstTip(user2)):
        print("privet")

main()



