from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.card import MDCard
import pandas as pd
from kivymd.uix.screen import MDScreen

class LoginForm(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def validate(self):
        if self.checkLogin(self.email.text, self.password.text):
            MainApp.sm.current = "screensimpledata"
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

    def toFormDetailProduct(self):
        #MainApp.sm.current = "register"
        pass

class ScreenSimpleData(MDScreen):
    def on_pre_enter(self):
        self.list_items()

    def list_items(self):
        Window.size = [300, 600]
        for i in range(101, 120):
            self.ids.listitem.add_widget(CarCard(   car_image = GetLink(MainApp.data['Link_image'][i]),
                                                    inform_car = MainApp.data['Tieu_de'][i],
                                                    price_car = MainApp.data['gia'][i],
                                                    status_car = MainApp.data['Tinh_trang'][i],
                                                    manufacture_year_car = MainApp.data['Nam_san_xuat'][i],
                                                    km_car = MainApp.data['Km_da_di'][i],
                                                    shift_stick_inform_car = MainApp.data['Hop_so'][i],
                                                    place = MainApp.data['Dia_diem'][i],
                                                    day = MainApp.data['Thoi_gian'][i]))

def GetLink(links):
    link = links.split()[0]
    link = "".join(c for c in link if c != '[' and c != ',' and c != "'")
    return link

def messageBox(title, content):
    pop = Popup(title=title,
                content=Label(text=content),
                size_hint=(None, None), size=(400, 400))
    pop.open()

class MainApp(MDApp):
    sm = ScreenManager()
    users = pd.read_csv('assets/login.csv')
    df = pd.DataFrame(users)
    data = pd.read_csv('assets/Car_data.csv')

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.sm.add_widget(LoginForm(name='login'))
        self.sm.add_widget(RegisterForm(name='register'))
        self.sm.add_widget(ScreenSimpleData(name='screensimpledata'))
        return self.sm

if __name__ == '__main__':
    Builder.load_file('screen_manager/screen_simple_data.kv')
    Builder.load_file('components/car_card.kv')
    Builder.load_file('screen_manager/login_screen.kv')

    Window.size = (375, 667)

    MainApp().run()
