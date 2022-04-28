from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.factory import Factory
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivymd.utils.fitimage import FitImage
import pandas as pd
from kivymd.uix.screen import MDScreen
from kivy.clock import Clock
import components.fit_image
import components.circular_avatar_image
import dataconn

class LoginForm(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def validate(self):
        if self.checkLogin(self.email.text, self.password.text):
            query = "SELECT Name FROM Login WHERE email = '%s'"
            MainApp.sm.current = "listcarscreen"
            MainApp.username = dataconn.executeQueryOneContion(MainApp.conn, query, self.email.text)[0][0] 
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
    heart_color = StringProperty()
    idx = NumericProperty()

    def toFormDetailProduct(self):
        if MainApp.sm.current == 'listcarscreen':
            MainApp.toListScreen = True
        else:
            MainApp.toListScreen = False
        MainApp.idx = self.idx
        MainApp.sm.transition.direction = 'left'
        MainApp.sm.current = 'detailcarscreen'

    def changeColorIcon(self):
        black_color = get_color_from_hex("#000000")
        if self.ids['heart_icon'].text_color != black_color:
            self.ids['heart_icon'].text_color = black_color
        else:
            self.ids['heart_icon'].text_color = get_color_from_hex('#EB144C')

class ListCarScreen(MDScreen):
    flag = True
    begin = -20

    def on_pre_enter(self):
        if self.flag:
            Window.size = [300, 600]
            self.rightArrowIcon()

    def list_items(self, *args):
        query = "SELECT * FROM Car_data LIMIT 20 OFFSET " + str(self.begin)
        data = dataconn.executeQuery(MainApp.conn, query)

        query = "SELECT car_id FROM LIKE"
        like_car_id = dataconn.executeQuery(MainApp.conn, query)

        for i in data:
            car_index = int(i[16])

            color = "#000000"
            for k in like_car_id:
                if car_index == k[0]:
                    color = "#EB144C"
                    break

            self.ids.listitem.add_widget(CarCard(   car_image = GetLink(i[12], 0),
                                                    inform_car = i[0],
                                                    price_car = i[1],
                                                    status_car = i[2],
                                                    manufacture_year_car = i[8],
                                                    km_car = i[4],
                                                    shift_stick_inform_car = i[5],
                                                    place = i[14],
                                                    day = i[15],
                                                    heart_color = color,
                                                    idx = car_index))
  
        self.flag = False

    def update_list_item(self, *args):
        self.flag = True
        self.ids.listitem.clear_widgets()
        self.list_items()

    def leftArrowIcon(self):
        temp = self.begin - 20
        if temp < 0:
            return
        self.begin -= 20
        self.clock = Clock.schedule_once(self.update_list_item, 0.5)

    def rightArrowIcon(self):
        self.begin += 20
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

        query = "SELECT * FROM Car_data WHERE id = '%d'"
        data = dataconn.executeQueryOneContion(MainApp.conn, query, MainApp.idx)

        self.car_image = GetLink(data[0][12], 0)
        self.car_image1 = GetLink(data[0][12], 1)
        self.car_image2 = GetLink(data[0][12], 2)
        self.car_image3 = GetLink(data[0][12], 3)
        self.car_image4 = GetLink(data[0][12], 4)
        self.inform_car = data[0][0]
        self.price_car = data[0][1]
        self.status_car = data[0][2]
        self.manufacture_year_car = data[0][8]
        self.km_car = data[0][4]
        self.shift_stick_inform_car = data[0][5]
        self.Dong_xe = data[0][3]
        self.Nhien_Lieu = data[0][6]
        self.Nguoi_Ban = data[0][7]
        self.Dan_dong= data[0][9]
        self.Mau_Xe = data[0][10]
        self.Xuat_Xu = data[0][11]
        self.Mo_Ta = data[0][13].strip("[] '")
        self.place = data[0][14]
        self.day = data[0][15]

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
            Window.size = [300, 600]
            self.ids.listitem.add_widget(ProfileCard())
            self.ids.listitem.add_widget(components.fit_image.Fit_Image())

    def update_list_item(self, data):
        self.ids.listitem.clear_widgets()
        self.ids.listitem.add_widget(ProfileCard())

        query = "SELECT car_id FROM Like"
        like_car_id = dataconn.executeQuery(MainApp.conn, query)

        for i in data:
            car_index = int(i[16])

            color = "#000000"
            for k in like_car_id:
                if car_index == k[0]:
                    color = "#EB144C"
                    break

            self.ids.listitem.add_widget(CarCard(   car_image = GetLink(i[12], 0),
                                                    inform_car = i[0],
                                                    price_car = i[1],
                                                    status_car = i[2],
                                                    manufacture_year_car = i[8],
                                                    km_car = i[4],
                                                    shift_stick_inform_car = i[5],
                                                    place = i[14],
                                                    day = i[15],
                                                    heart_color = color,
                                                    idx = car_index))
            self.flag = False
    
    def toFormListCar(self):
        MainApp.sm.transition.direction = 'right'
        MainApp.sm.current = 'listcarscreen'
        self.ids.listitem.clear_widgets()
        self.flag = True

class ProfileCard(MDCard):
    id = StringProperty()

    def toFormListCar(self):
        MainApp.sm.get_screen("profile").toFormListCar()

    def toFormLogin(self):
        MainApp.sm.transition.direction = 'right'
        MainApp.sm.current = 'login'
    
    def likeIcon(self):
        self.clock = Clock.schedule_once(self.Like, 0.5)

    def historyIcon(self):
        self.clock = Clock.schedule_once(self.History, 0.5)

    def Like(self, *args):
        query = "SELECT * FROM Car_data WHERE id in (SELECT car_id FROM Like where username = '%s')"
        data = dataconn.executeQueryOneContion(MainApp.conn, query, MainApp.username)
        MainApp.sm.get_screen("profile").update_list_item(data)

    def History(self, *args):
        query = "SELECT * FROM Car_data WHERE id in (SELECT car_id FROM History where username = '%s')"
        data = dataconn.executeQueryOneContion(MainApp.conn, query, MainApp.username)
        MainApp.sm.get_screen("profile").update_list_item(data)

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
    Builder.load_file('components/fit_image.kv')
    Builder.load_file('components/profile_card.kv')

class MainApp(MDApp):
    sm = ScreenManager()
    users = pd.read_csv('assets/login.csv')
    df = pd.DataFrame(users)
    idx = None
    flag = -20
    toListScreen = None
    conn = dataconn.create_connection("assets/database.sqlite")
    username = "Le Minh"

    def build(self):
        self.theme_cls.primary_palette = "Blue"
        self.sm.add_widget(ListCarScreen(name='listcarscreen'))
        self.sm.add_widget(LoginForm(name='login'))
        #self.sm.add_widget(ListCarScreen(name='listcarscreen'))
        self.sm.add_widget(RegisterForm(name='register'))
        self.sm.add_widget(DetailCarScreen(name = 'detailcarscreen'))
        self.sm.add_widget(ProfileScreen(name = 'profile'))
        return self.sm

if __name__ == '__main__':
    load_all_kivy_file()
    Window.size = (375, 667)

    MainApp().run()
