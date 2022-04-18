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
    i = 1
    j = 21

    def on_pre_enter(self):
        if self.flag:
            Window.size = [300, 600]
            self.clock = Clock.schedule_once(self.list_items, 0.5)

    def list_items(self, *args):
        for i in range(self.i, self.j):
            self.ids.listitem.add_widget(CarCard(   car_image = GetLink(MainApp.data['Link_image'][i]),
                                                    inform_car = MainApp.data['Tieu_de'][i],
                                                    price_car = MainApp.data['gia'][i],
                                                    status_car = MainApp.data['Tinh_trang'][i],
                                                    manufacture_year_car = MainApp.data['Nam_san_xuat'][i],
                                                    km_car = MainApp.data['Km_da_di'][i],
                                                    shift_stick_inform_car = MainApp.data['Hop_so'][i],
                                                    place = MainApp.data['Dia_diem'][i],
                                                    day = MainApp.data['Thoi_gian'][i],
                                                    idx = i))
        self.flag = False

    def update_list_item(self, *args):
        self.flag = True
        self.ids.listitem.clear_widgets()
        self.list_items()

    def leftArrowIcon(self):
        if self.i < 21:
            return
        self.i -= 20
        self.j -= 20
        self.clock = Clock.schedule_once(self.update_list_item, 0.5)

    def rightArrowIcon(self):
        self.i += 20
        self.j += 20
        self.clock = Clock.schedule_once(self.update_list_item, 0.5)
                                                    
class DetailCarScreen(MDScreen):
    car_image = StringProperty()
    car_image1 = StringProperty()
    car_image2 = StringProperty()
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

    def on_enter(self):
        Window.size = [300, 600]
        self.car_image = GetLink(MainApp.data['Link_image'][MainApp.idx])
        self.car_image1 = GetLink1(MainApp.data['Link_image'][MainApp.idx])
        self.car_image2 = GetLink2(MainApp.data['Link_image'][MainApp.idx])
        self.inform_car = MainApp.data['Tieu_de'][MainApp.idx]
        self.price_car = MainApp.data['gia'][MainApp.idx]
        self.status_car = MainApp.data['Tinh_trang'][MainApp.idx]
        self.manufacture_year_car = MainApp.data['Nam_san_xuat'][MainApp.idx]
        self.km_car = MainApp.data['Km_da_di'][MainApp.idx]
        self.shift_stick_inform_car = MainApp.data['Hop_so'][MainApp.idx]
        self.Dong_xe = MainApp.data['Dong_xe'][MainApp.idx]
        self.Nhien_Lieu = MainApp.data['Nhien_lieu'][MainApp.idx]
        self.Nguoi_Ban = MainApp.data['Nguoi_ban'][MainApp.idx]
        self.Dan_dong= MainApp.data['Dan_dong'][MainApp.idx]
        self.Mau_Xe = MainApp.data['Mau_xe'][MainApp.idx]
        self.Xuat_Xu = MainApp.data['Xuat_xu'][MainApp.idx]
        self.Mo_Ta = MainApp.data['Mo_ta'][MainApp.idx].strip("[] '")
        self.place = MainApp.data['Dia_diem'][MainApp.idx]
        self.day = MainApp.data['Thoi_gian'][MainApp.idx]

def GetLink(links):
    link = links.split()[0]
    link = "".join(c for c in link if c != '[' and c != ',' and c != "'")
    return link

def GetLink1(links):
    link = links.split()[1]
    link = "".join(c for c in link if c != '[' and c != ',' and c != "'")
    return link

def GetLink2(links):
    link = links.split()[2]
    link = "".join(c for c in link if c != '[' and c != ',' and c != "'")
    return link

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

class MainApp(MDApp):
    sm = ScreenManager()
    users = pd.read_csv('assets/login.csv')
    df = pd.DataFrame(users)
    data = pd.read_csv('assets/Car_data.csv')
    idx = 3

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.sm.add_widget(LoginForm(name='login'))
        self.sm.add_widget(RegisterForm(name='register'))
        self.sm.add_widget(DetailCarScreen(name = 'detailcarscreen'))
        self.sm.add_widget(ListCarScreen(name='listcarscreen'))
        return self.sm

if __name__ == '__main__':
    load_all_kivy_file()
    Window.size = (375, 667)
    MainApp().run()
