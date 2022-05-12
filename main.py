from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivymd.uix.card import MDCard
from kivy.uix.image import Image
from kivy.utils import get_color_from_hex
from kivymd.utils.fitimage import FitImage
import pandas as pd
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import OneLineAvatarListItem
from kivy.clock import Clock
import components.fit_image
import dataconn
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.uix.dialog import MDDialog
from assets.image import *
from hot_reload.hotreload import Main

class LoginForm(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def validate(self):
        if self.checkLogin(self.email.text, self.password.text):
            query = "SELECT Name FROM Login WHERE email = '%s'"
            MainApp.username = dataconn.executeSelectQueryOneContion(MainApp.conn, query, self.email.text)[0][0]
            MainApp.sm.transition.direction = 'left'
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

class CarCard(RecycleDataViewBehavior, MDCard):
    car_image = StringProperty()
    inform_car = StringProperty()
    price_car = StringProperty()
    status_car = StringProperty()
    manufacture_year_car = StringProperty()
    km_car = StringProperty()
    shift_stick_inform_car = StringProperty()
    place = StringProperty()
    day = StringProperty()
    heart_color = StringProperty("#000000")
    idx = NumericProperty()

    def toFormDetailProduct(self):
        if MainApp.sm.current == 'listcarscreen':
            MainApp.toListScreen = True
        else:
            MainApp.toListScreen = False
        query = '''INSERT INTO History(username, car_id) VALUES (?, ?)'''
        dataconn.executeInsertDeleteQuery(MainApp.conn, query, (MainApp.username, self.idx))

        MainApp.sm.get_screen('detailcarscreen').idx = self.idx
        if self.ids['heart_icon'].text_color == MainApp.red_color:
            MainApp.sm.get_screen('detailcarscreen').ids['heart_icon'].text_color = MainApp.red_color
        else:
            MainApp.sm.get_screen('detailcarscreen').ids['heart_icon'].text_color = MainApp.black_color
        MainApp.sm.transition.direction = 'left'
        MainApp.sm.current = 'detailcarscreen'

    def insertValueToLikeTable(self):
        query = '''INSERT INTO Like(username, car_id) VALUES (?, ?)'''
        dataconn.executeInsertQuery(MainApp.conn, query, (MainApp.username, self.idx))

    def heartIcon(self):
        if self.ids['heart_icon'].text_color != MainApp.black_color:
            if MainApp.sm.current == 'profile':
                MainApp.sm.get_screen('profile').changeHeartColor(self.idx, "#000000")
            MainApp.sm.get_screen('listcarscreen').changeHeartColor(self.idx, "#000000")
            query = ''' DELETE FROM Like WHERE username = ? AND car_id = ?'''
            dataconn.executeInsertDeleteQuery(MainApp.conn, query, (MainApp.username, self.idx))
        else:
            if MainApp.sm.current == 'profile':
                MainApp.sm.get_screen('profile').changeHeartColor(self.idx, "#EB144C")
            MainApp.sm.get_screen('listcarscreen').changeHeartColor(self.idx, "#EB144C")
            query = '''INSERT INTO Like(username, car_id) VALUES (?, ?)'''
            dataconn.executeInsertDeleteQuery(MainApp.conn, query, (MainApp.username, self.idx))
        try:
            if MainApp.sm.get_screen('profile').ids['box'].children[0].ids['heart_icon'].text_color == MainApp.red_color:
                MainApp.sm.get_screen('profile').ids['box'].children[0].Like()
            else:
                MainApp.sm.get_screen('profile').ids['box'].children[0].History()
        except:
            pass

class ListCarScreen(MDScreen):
    flag = True
    begin = 0
    logo_index = None
    logo_name = None

    def on_pre_enter(self):
        if self.flag:
            Window.size = [300, 600]
            self.list_logos()
            self.list_items()

    def list_items(self):
        if self.logo_index == None:
            query = "SELECT * FROM Car_data LIMIT 20 OFFSET " + str(self.begin)
            data = dataconn.executeSelectQuery(MainApp.conn, query)
        else:
            query = """SELECT * FROM Car_data WHERE instr(Tieu_de, ?) > 0 LIMIT 20 OFFSET """ + str(self.begin)
            data = dataconn.Filter_hang_xe(MainApp.conn, query, self.ids['listlogo'].children[self.logo_index].ids['lb_name'].text)
        query = "SELECT car_id FROM Like WHERE username = '%s'"
        like_car_id = dataconn.executeSelectQueryOneContion(MainApp.conn, query, MainApp.username)

        index_in_data = 0
        for i in data:
            car_index = int(i[16])
            color = "#000000"
            for k in like_car_id:
                if car_index == k[0]:
                    color = "#EB144C"
                    break
            self.ids.listitem.data.append({ "car_image": GetLink(i[12].split()[0]),
                                            "inform_car": i[0],
                                            "price_car": i[1],
                                            "status_car": i[2],
                                            "manufacture_year_car": i[8],
                                            "km_car": i[4],
                                            "shift_stick_inform_car": i[5],
                                            "place": i[14],
                                            "day": i[15],
                                            "heart_color": color,
                                            "idx": car_index,
                                            "index_in_data": index_in_data})
            index_in_data += 1
        self.flag = False

    def update_list_item(self, *args):
        self.flag = True
        self.clearListItem()
        self.list_items()

    def leftArrowIcon(self):
        temp = self.begin - 20
        if temp < 0:
            return
        self.begin -= 20
        self.clock = Clock.schedule_once(self.update_list_item, 0.5)

    def rightArrowIcon(self):
        self.begin += 20
        self.update_list_item()
        self.clock = Clock.schedule_once(self.update_list_item, 0.5)

    def toProfileForm(self):
        MainApp.sm.transition.direction = 'left'
        MainApp.sm.current = 'profile'

    def reset(self):
        self.flag = True
        self.begin = -20
        self.clearListItem()

    def list_logos(self):
        idx = len(logo) - 1
        for i in logo:
            self.ids.listlogo.add_widget(CircularAvatarImage(avatar = logo.get(i), name = i, idx = idx, color = "#20B2AA"))
            idx -= 1

    def clearListItem(self):
        self.ids.listitem.data = []

    def logoClick(self, idx):
        if self.logo_index != None:
            self.ids['listlogo'].children[self.logo_index].ids['line'].md_bg_color = MainApp.black_color
        self.ids['listlogo'].children[idx].ids['line'].md_bg_color = MainApp.red_color
        self.flag = True
        self.begin = 0
        self.logo_index = idx
        self.clock = Clock.schedule_once(self.update_list_item, 0.5) 

    def homeIcon(self):
        self.logo_index = None
        self.begin = 0
        self.clock = Clock.schedule_once(self.update_list_item, 0.5)

    def clearAll(self):
        self.clearListItem()
        self.ids.listlogo.clear_widgets()
        self.begin = 0
        self.flag = True

    def changeHeartColor(self, index, color):
        for i in self.ids.listitem.data:
            if i['idx'] == index:    
                i['heart_color'] = color
                break
        self.ids.listitem.refresh_from_data()

class DetailCarScreen(MDScreen):
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
    idx = NumericProperty()

    def on_pre_enter(self):
        Window.size = [300, 600]
        query = '''SELECT * FROM Car_data WHERE id = %d'''
        data = dataconn.executeSelectQueryOneContion(MainApp.conn, query, self.idx)
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
        self.list_image_car(data[0][12])
        self.idx = int(data[0][16])

    def list_image_car(self, str_list_link):
        list_link = str_list_link.split()
        for i in list_link:
            self.ids.list_image_car.add_widget(FitImage(source = GetLink(i),
                                                        radius = [20, ],
                                                        size_hint = [None, None],
                                                        height = 130,
                                                        width = 200))

    def changeScreen(self):
        if MainApp.toListScreen:
            MainApp.sm.transition.direction = 'right'
            MainApp.sm.current = "listcarscreen"
        else:
            MainApp.sm.transition.direction = 'right'
            MainApp.sm.current = "profile"
        self.ids.list_image_car.clear_widgets()

    def heartIcon(self):
        if self.ids['heart_icon'].text_color != MainApp.black_color:
            self.ids['heart_icon'].text_color = MainApp.black_color
            MainApp.sm.get_screen('listcarscreen').changeHeartColor(self.idx, "#000000")
            query = ''' DELETE FROM Like WHERE username = ? AND car_id = ?'''
            dataconn.executeInsertDeleteQuery(MainApp.conn, query, (MainApp.username, self.idx))
        else:
            self.ids['heart_icon'].text_color = MainApp.red_color
            MainApp.sm.get_screen('listcarscreen').changeHeartColor(self.idx, "#EB144C")
            query = '''INSERT INTO Like(username, car_id) VALUES (?, ?)'''
            dataconn.executeInsertDeleteQuery(MainApp.conn, query, (MainApp.username, self.idx))
        try:
            if MainApp.sm.get_screen('profile').ids['box'].children[0].ids['heart_icon'].text_color == MainApp.red_color:
                MainApp.sm.get_screen('profile').ids['box'].children[0].Like()
            else:
                MainApp.sm.get_screen('profile').ids['box'].children[0].History()
        except:
            pass

class ProfileScreen(MDScreen):
    profile_picture = 'assets/profile_picture.png'
    flag_profile_card = True
    flag_fit_image = True

    def on_pre_enter(self):
        if self.flag_profile_card:
            self.ids.listitem.data = []
            self.ids.box.add_widget(ProfileCard(id = 'profile_card', username = MainApp.username, gmail = MainApp.gmail))
            self.flag_profile_card = False
        if self.flag_fit_image:
            self.ids.box.add_widget(components.fit_image.Fit_Image())
            self.flag_fit_image = False

    def update_list_item(self, data):
        self.removeFitImage()
        self.ids.listitem.data = []
        query = "SELECT car_id FROM Like"
        like_car_id = dataconn.executeSelectQuery(MainApp.conn, query)

        index_in_data = 0
        for i in data:
            car_index = int(i[16])
            color = "#000000"
            for k in like_car_id:
                if car_index == k[0]:
                    color = "#EB144C"
                    break
            self.ids.listitem.data.append({   "car_image": GetLink(i[12].split()[0]),
                            "inform_car": i[0],
                            "price_car": i[1],
                            "status_car": i[2],
                            "manufacture_year_car": i[8],
                            "km_car": i[4],
                            "shift_stick_inform_car": i[5],
                            "place": i[14],
                            "day": i[15],
                            "heart_color": color,
                            "idx": car_index,
                            "index_in_data": index_in_data})
            index_in_data += 1
        self.flag = False
    
    def toFormListCar(self):
        MainApp.sm.transition.direction = 'right'
        MainApp.sm.current = 'listcarscreen'
        self.flag_fit_image = True
        self.reset()
        
    def reset(self):
        self.removeFitImage()
        self.ids.listitem.data = []
        self.ids.listitem.refresh_from_data()
        self.ids['box'].children[0].ids['heart_icon'].text_color = MainApp.black_color
        self.ids['box'].children[0].ids['history_icon'].text_color = MainApp.black_color
        
    def removeFitImage(self):
        if len(self.ids.box.children) == 2:
            self.ids.box.remove_widget(self.ids.box.children[0])

    def clearAll(self):
        self.ids.box.clear_widgets()
        self.ids.listitem.data = []
        self.flag_profile_card = True
        self.flag_fit_image = True
    
    def changeHeartColor(self, index, color):
        for i in self.ids.listitem.data:
            if i['idx'] == index:    
                i['heart_color'] = color
                break
        self.ids.listitem.refresh_from_data()

class PredictPriceScreen(MDScreen):
    fuel = None
    shift_stick = None
    currenBox = None

    def changeFuelColor(self):
        for i in self.ids.fuel.children:
            if i.text == self.fuel:
                i.background_color = get_color_from_hex('#FFC300')
            else:
                i.background_color = get_color_from_hex('#DCDCDC')
    
    def changeShiftStickColor(self):
        for i in self.ids.shift_stick.children:
            if i.text == self.shift_stick:
                i.background_color = get_color_from_hex('#FFC300')
            else:
                i.background_color = get_color_from_hex('#DCDCDC')

    def toSelectScreen(self):
        MainApp.sm.get_screen('selectscreen').text = self.currenBox
        if self.currenBox == 'Hãng xe':
            MainApp.sm.get_screen('selectscreen').diction = logo
        else:
            MainApp.sm.get_screen('selectscreen').diction = type
        MainApp.sm.transition.direction = 'right'
        MainApp.sm.current = 'selectscreen'

    def changeLogoType(self, text):
        if self.currenBox == 'Hãng xe':
            self.ids['logo_field'].text = text
        else:
            self.ids['type_field'].text = text

    def reset(self):
        for i in self.ids.fuel.children:
            i.background_color = get_color_from_hex('#DCDCDC')
        for i in self.ids.shift_stick.children:
            i.background_color = get_color_from_hex('#DCDCDC')
        self.ids['logo_field'].text = ''
        self.ids['type_field'].text = ''
        self.ids['manufacture_year'].text = ''
        self.ids['seat'].text = ''
        self.ids['km'].text = ''

    def openPredictDialog(self):
        price = predictPrice(self.ids['logo_field'].text, self.ids['type_field'].text, self.fuel, self.shift_stick, self.ids['manufacture_year'].text, self.ids['seat'].text, self.ids['km'].text)
        popup = Popup(  content = Label(text = str(price) + ' triệu'),
                        auto_dismiss = True,
                        size_hint=(None, None), 
                        size=(300, 300),
                        title = 'Xe của bạn được định giá: ')
        popup.open()

class CustomListItem(OneLineAvatarListItem):
    image = StringProperty()

    def changeTextField(self, text):
        MainApp.sm.get_screen('selectscreen').ids['search_field'].text = text
        if MainApp.sm.get_screen('selectscreen').text == 'Hãng xe':
            MainApp.sm.get_screen('predictpricescreen').ids['logo_field'].text = text
        else:
            MainApp.sm.get_screen('predictpricescreen').ids['type_field'].text = text

    def toPredictScreen(self, text):
        MainApp.sm.transition.direction = 'left'
        MainApp.sm.current = 'predictpricescreen'
        MainApp.sm.get_screen('predictpricescreen').changeLogoType(text)
        MainApp.sm.get_screen('selectscreen').reset()

class CircularAvatarImage(MDCard):
    avatar = StringProperty()
    name = StringProperty()
    idx = NumericProperty()
    color = StringProperty("#FFFFFF")

    def changeLineColor(self):
        MainApp.sm.get_screen('listcarscreen').logoClick(self.idx)

class ProfileCard(MDCard):
    id = StringProperty()
    username = StringProperty()
    gmail = StringProperty()

    def toFormListCar(self):
        MainApp.sm.transition.direction = 'right'
        MainApp.sm.get_screen("profile").toFormListCar()

    def toFormLogin(self):
        MainApp.sm.transition.direction = 'left'
        MainApp.sm.current = 'login'
        MainApp.sm.get_screen('listcarscreen').clearAll()
        MainApp.sm.get_screen('profile').clearAll()
    
    def likeIcon(self):
        self.clock = Clock.schedule_once(self.Like, 0.5)

    def historyIcon(self):
        self.clock = Clock.schedule_once(self.History, 0.5)

    def toFormLoginIcon(self):
        MyApp.showLogoutDialog()

    def Like(self, *args):
        query = "SELECT * FROM Car_data WHERE id in (SELECT car_id FROM Like where username = '%s')"
        data = dataconn.executeSelectQueryOneContion(MainApp.conn, query, MainApp.username)
        MainApp.sm.get_screen("profile").update_list_item(data)
        self.ids['heart_icon'].text_color = get_color_from_hex('#EB144C')
        self.ids['history_icon'].text_color = get_color_from_hex('#000000')

    def History(self, *args):
        query = "SELECT * FROM Car_data WHERE id in (SELECT car_id FROM History where username = '%s')"
        data = dataconn.executeSelectQueryOneContion(MainApp.conn, query, MainApp.username)
        MainApp.sm.get_screen("profile").update_list_item(data)
        self.ids['heart_icon'].text_color = get_color_from_hex('#000000')
        self.ids['history_icon'].text_color = get_color_from_hex('#EB144C')

    def clearHistory(self):
        query = "DELETE FROM History"
        dataconn.executeInsertDeleteQuery(MainApp.conn, query, ())
        self.History()

class Recycleviewlist(RecycleView):
    id = StringProperty()

    def __init__(self, data):
        super(Recycleviewlist, self).__init__()
        self.data = data

class SelectScreen(MDScreen):
    text = StringProperty()
    diction = {}

    def on_pre_enter(self):
        for i in self.diction:
             self.ids.recycle_view.data.append({'text': i, 
                                                'ImageLeftWidget': self.diction.get(i),
                                                'viewclass': 'CustomListItem',
                                                'image': self.diction.get(i)})
    def searchText(self, text):         
        self.ids.recycle_view.data = []
        for i in self.diction:
            if text.title() in i:
                self.ids.recycle_view.data.append({     'text': i, 
                                                        'ImageLeftWidget': self.diction.get(i),
                                                        'viewclass': 'CustomListItem',
                                                        'image': self.diction.get(i)})

    def reset(self):
        self.ids['search_field'].text = ''
        self.ids['recycle_view'].data = []

def predictPrice(logo, type, fuel, shift_stick, manufacture_year, seat, km):
    return 100

def GetLink(link):
    try:
        link = "".join(c for c in link if c != '[' and c != ',' and c != "'" and c != ']')
        return link
    except:
        return ""

def messageBox(title, content):
    pop = Popup(title=title,
                content=Label(text=content),
                size_hint=(None, None), size=(400, 400))
    pop.open()

class MainApp(MDApp):
    sm = ScreenManager()
    users = pd.read_csv('assets/login.csv')
    df = pd.DataFrame(users)
    toListScreen = None
    conn = dataconn.create_connection("assets/database.db")
    username = "Le Minh"
    gmail = "khanhprolazay@gmail.com"
    black_color = get_color_from_hex("#000000")
    red_color = get_color_from_hex("#EB144C")
    dialog = None

    def build(self):
        Window.size = (300, 600)
        self.load_all_kivy_file()
        self.theme_cls.primary_palette = "Blue"
        #self.sm.add_widget(PredictPriceScreen(name = 'predictpricescreen'))
        self.sm.add_widget(LoginForm(name='login'))
        self.sm.add_widget(ListCarScreen(name='listcarscreen'))
        self.sm.add_widget(RegisterForm(name='register'))
        self.sm.add_widget(DetailCarScreen(name = 'detailcarscreen'))
        self.sm.add_widget(ProfileScreen(name = 'profile'))
        self.sm.add_widget(SelectScreen(name = 'selectscreen'))
        self.sm.add_widget(PredictPriceScreen(name = 'predictpricescreen'))
        return self.sm

    def load_all_kivy_file(self):
        Builder.load_file('components/car_card.kv')
        Builder.load_file('components/circular_avatar_image.kv')
        Builder.load_file('components/fit_image.kv')
        Builder.load_file('components/profile_card.kv')
        Builder.load_file('screen_manager/login_screen.kv')
        Builder.load_file('screen_manager/detail_car_screen.kv')
        Builder.load_file('screen_manager/profile_screen.kv')
        Builder.load_file('screen_manager/predict_price_screen.kv')
        Builder.load_file('screen_manager/list_car_screen.kv')
        Builder.load_file('screen_manager/select_screen.kv')

    def toFormLogin(self):
        self.sm.transition.direction = 'left'
        self.sm.current = 'login'
        self.sm.get_screen('listcarscreen').clearAll()
        self.sm.get_screen('profile').clearAll()

if __name__ == '__main__':
    MyApp = MainApp()
    MyApp.run()
    MyApp.conn.close()