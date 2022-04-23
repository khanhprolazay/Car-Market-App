from unicodedata import name
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.card import MDCard
import pandas as pd
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
import components.circular_avatar_image
import dataconn

class LoginForm(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def validate(self):
        if self.checkLogin(self.email.text, self.password.text):
            MainApp.sm.current = "listcarscreen"
            self.reset()
        else:
            messageBox('Warning!', 'Incorrect Username or Password')

    def reset(self):
        self.email.text = ""
        self.password.text = ""

    def checkLogin(self, email, password):
        index_list = MainApp.df.index.tolist()
        i = 0
        check = False
        while i <= len(index_list) - 1:
            if (email == MainApp.df.loc[i].at['Email']) and (password == MainApp.df.loc[i].at['Password']):
                check = True
            i += 1
        return check

class RegisterForm(Screen):
    fullname = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    confPass = ObjectProperty(None)

    def loginBtn(self):
        user = pd.DataFrame([[self.fullname.text, self.email.text, self.password.text]],
                            columns=['Name', 'Email', 'Password'])
        if self.email.text != "" or self.fullname.text != "" or self.password.text != "" or self.confPass.text != "":
            if self.email.text not in MainApp.users['Email'].unique():
                if self.password.text == self.confPass.text:
                    user.to_csv('login.csv', mode='a', header=False, index=False)
                    messageBox('Message', 'Register Done!')
                    MainApp.sm.current = 'login'
                    self.fullname.text = ""
                    self.email.text = ""
                    self.password.text = ""
                    self.confPass.text = ""
                else:
                    messageBox('Warning!', 'Password must be same Confirm Password')
                    self.confPass.text = ""
            else:
                messageBox('Warning!', 'Email already exist')
                self.email.text = ""
        else:
            messageBox('Invalid Form', 'Please fill in all inputs with valid information.')

class CarCard(MDCard):
    car_image = StringProperty()
    inform_car = StringProperty()
    price_car = StringProperty()
    status_car = StringProperty()
    manufacture_year_car = StringProperty()
    km_car = StringProperty()
    shift_stick_inform_car = StringProperty()
    place = StringProperty()
    day = StringProperty()
    idx = NumericProperty()

    def toFormDetailProduct(self):
        if MainApp.sm.current == 'listcarscreen':
            MainApp.toListScreen = True
        else:
            MainApp.toListScreen = False
        MainApp.idx = self.idx
        MainApp.sm.transition.direction = 'left'
        MainApp.sm.current = 'detailcarscreen'

    def settingCard(self, car_image, inform_car, price_car, status_car, manufacture_year_car, km_car, shift_stick_inform_car, place, day, idx):
        self.car_image = car_image
        self.inform_car = inform_car
        self.price_car = price_car
        self.status_car = status_car
        self.manufacture_year_car = manufacture_year_car
        self.km_car = km_car
        self.shift_stick_inform_car = shift_stick_inform_car
        self.place = place
        self.day = day
        self.idx = idx

class ListCarScreen(MDScreen):
    flag = True

    def on_pre_enter(self):
        if self.flag:
            Window.size = [300, 600]
            self.rightArrowIcon()

    def list_items(self, *args):
        limit = MainApp.idx + 20

        for i in range(MainApp.idx, limit):
            self.ids.listitem.add_widget(CarCard(   car_image = GetLink(MainApp.data[i][12], 0),
                                                    inform_car = MainApp.data[i][0],
                                                    price_car = MainApp.data[i][1],
                                                    status_car = MainApp.data[i][2],
                                                    manufacture_year_car = MainApp.data[i][8],
                                                    km_car = MainApp.data[i][4],
                                                    shift_stick_inform_car = MainApp.data[i][5],
                                                    place = MainApp.data[i][14],
                                                    day = MainApp.data[i][15],
                                                    idx = i))
  
        self.flag = False

    def update_list_item(self, *args):
        self.flag = True
        self.ids.listitem.clear_widgets()
        self.list_items()

    def leftArrowIcon(self):
        temp = MainApp.idx - 20
        if temp < 0:
            return
        MainApp.idx -= 20
        self.clock = Clock.schedule_once(self.update_list_item, 0.5)

    def rightArrowIcon(self):
        MainApp.idx += 20
        self.clock = Clock.schedule_once(self.update_list_item, 0.5)

    def toProfileForm(self):
        MainApp.sm.transition.direction = 'left'
        MainApp.sm.current = 'profile'
                                                    
class DetailCarScreen(MDScreen):
    car_image = StringProperty()
    car_image1 = StringProperty()
    car_image2 = StringProperty()
    car_image3 = StringProperty()
    car_image4 = StringProperty()
    inform_car = StringProperty()
    price_car = StringProperty()
    status_car = StringProperty()
    manufacture_year_car = StringProperty()
    km_car = StringProperty()
    shift_stick_inform_car = StringProperty()
    Dong_xe = StringProperty()
    Nhien_Lieu = StringProperty()
    Nguoi_Ban = StringProperty()
    Dan_dong = StringProperty()
    Mau_Xe = StringProperty()
    Xuat_Xu = StringProperty()
    Mo_Ta = StringProperty()
    place = StringProperty()
    day = StringProperty()

    def on_pre_enter(self):
        Window.size = [300, 600]
        self.car_image = GetLink(MainApp.data[MainApp.idx][12], 0)
        self.car_image1 = GetLink(MainApp.data[MainApp.idx][12], 1)
        self.car_image2 = GetLink(MainApp.data[MainApp.idx][12], 2)
        self.car_image3 = GetLink(MainApp.data[MainApp.idx][12], 3)
        self.car_image4 = GetLink(MainApp.data[MainApp.idx][12], 4)
        self.inform_car = MainApp.data[MainApp.idx][0]
        self.price_car = MainApp.data[MainApp.idx][1]
        self.status_car = MainApp.data[MainApp.idx][2]
        self.manufacture_year_car = MainApp.data[MainApp.idx][8]
        self.km_car = MainApp.data[MainApp.idx][4]
        self.shift_stick_inform_car = MainApp.data[MainApp.idx][5]
        self.Dong_xe = MainApp.data[MainApp.idx][3]
        self.Nhien_Lieu = MainApp.data[MainApp.idx][6]
        self.Nguoi_Ban = MainApp.data[MainApp.idx][7]
        self.Dan_dong= MainApp.data[MainApp.idx][9]
        self.Mau_Xe = MainApp.data[MainApp.idx][10]
        self.Xuat_Xu = MainApp.data[MainApp.idx][11]
        self.Mo_Ta = MainApp.data[MainApp.idx][13].strip("[] '")
        self.place = MainApp.data[MainApp.idx][14]
        self.day = MainApp.data[MainApp.idx][15]

    def changeScreen(self):
        if MainApp.toListScreen:
            MainApp.sm.transition.direction = 'right'
            MainApp.sm.current = "listcarscreen"
        else:
            MainApp.sm.transition.direction = 'right'
            MainApp.sm.current = "profile"

class ProfileScreen(MDScreen):
    profile_picture = 'assets/profile_picture.png'
    flag = True

    def on_pre_enter(self):
        if self.flag:
            self.clock = Clock.schedule_once(self.list_items, 0.5)

    def list_items(self, *args):
        Window.size = [300, 600]
        for i in range(1, 4):
            self.ids.listitem.add_widget(CarCard(   car_image = GetLink(MainApp.data[i][12], 0),
                                                    inform_car = MainApp.data[i][0],
                                                    price_car = MainApp.data[i][1],
                                                    status_car = MainApp.data[i][2],
                                                    manufacture_year_car = MainApp.data[i][8],
                                                    km_car = MainApp.data[i][4],
                                                    shift_stick_inform_car = MainApp.data[i][5],
                                                    place = MainApp.data[i][14],
                                                    day = MainApp.data[i][15],
                                                    idx = i))
        self.flag = False

    def toFormListCar(self):
        MainApp.sm.transition.direction = 'right'
        MainApp.sm.current = 'listcarscreen'
        self.ids.listitem.clear_widgets()
        self.flag = True
    
def GetLink(links, pos):
    try:
        link = links.split()[pos]
        link = "".join(c for c in link if c != '[' and c != ',' and c != "'" and c != ']')
        return link
    except:
        return ""

def messageBox(title, content):
    pop = Popup(title=title,
                content=Label(text=content),
                size_hint=(None, None), size=(400, 400))
    pop.open()

def load_all_kivy_file():
    Builder.load_file('screen_manager/list_car_screen.kv')
    Builder.load_file('components/car_card.kv')
    Builder.load_file('screen_manager/login_screen.kv')
    Builder.load_file('screen_manager/detail_car_screen.kv')
    Builder.load_file('screen_manager/profile_screen.kv')
    Builder.load_file('components/circular_avatar_image.kv')

class MainApp(MDApp):
    sm = ScreenManager()
    users = pd.read_csv('assets/login.csv')
    df = pd.DataFrame(users)
    data = dataconn.select_all_table("assets/database.sqlite", "Car_data")
    idx = -20
    toListScreen = None

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.sm.add_widget(LoginForm(name='login'))
        self.sm.add_widget(ListCarScreen(name='listcarscreen'))
        self.sm.add_widget(RegisterForm(name='register'))
        self.sm.add_widget(ProfileScreen(name = 'profile'))
        self.sm.add_widget(DetailCarScreen(name = 'detailcarscreen'))
        return self.sm

if __name__ == '__main__':
    load_all_kivy_file()
    Window.size = (375, 667)

    MainApp().run()
