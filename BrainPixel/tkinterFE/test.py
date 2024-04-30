class User:
    def __init__(self):
        self.CountOfMoney = 0
        self.CountOfFirstTips = 0
        self.CountOfSecondTips = 0
        self.CountOfSkins = 0

    def set_count_of_money(self, count):
        self.CountOfMoney = count

    def get_count_of_money(self):
        return self.CountOfMoney

    def set_count_of_first_tips(self, count):
        self.CountOfFirstTips = count

    def get_count_of_first_tips(self):
        return self.CountOfFirstTips

    def set_count_of_second_tips(self, count):
        self.CountOfSecondTips = count

    def get_count_of_second_tips(self):
        return self.CountOfSecondTips

    def set_count_of_skins(self, count):
        self.CountOfSkins = count

    def get_count_of_skins(self):
        return self.CountOfSkins
