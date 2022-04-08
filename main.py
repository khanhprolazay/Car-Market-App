from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.label import Label
import pandas as pd
from screen_manager.screen_simple_data import ScreenSimpleData


Builder.load_file('screen_manager/screen_simple_data.kv')
Builder.load_file('components/car_card.kv')
Builder.load_file('screen_manager/login_screen.kv')


class LoginForm(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def validate(self):
        if self.checkLogin(self.email.text, self.password.text):
            sm.current = "screensimpledata"
            self.reset()
        else:
            messageBox('Warning!', 'Incorrect Username or Password')

    def createBtn(self):
        self.reset()
        sm.current = "register"

    def reset(self):
        self.email.text = ""
        self.password.text = ""

    def checkLogin(self, email, password):
        index_list = df.index.tolist()
        i = 0
        check = False
        while i <= len(index_list) - 1:
            if (email == df.loc[i].at['Email']) and (password == df.loc[i].at['Password']):
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
            if self.email.text not in users['Email'].unique():
                if self.password.text == self.confPass.text:
                    user.to_csv('login.csv', mode='a', header=False, index=False)
                    messageBox('Message', 'Register Done!')
                    sm.current = 'login'
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


class MenuForm(Screen):
    # username = ObjectProperty(None)
    # email = ObjectProperty(None)
    # current = ""
    #
    # def on_enter(self, *args):
    #     username = self.get_user(self.current)
    #     # self.username.text = "Hello: " + username
    #     print(self.current)
    #
    # def get_user(self, email):
    #     index_list = df.index.tolist()
    #     for i in range(0, len(index_list)):
    #         if email == df.loc[i].at['Email']:
    #             name = df.loc[i].at['Name']
    #             return name
    pass




Window.size = (375, 667)
sm = ScreenManager()
users = pd.read_csv('data/login.csv')
df = pd.DataFrame(users)

class MainApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        #self.theme_cls.theme_style = "Dark"
        sm.add_widget(LoginForm(name='login'))
        sm.add_widget(RegisterForm(name='register'))
        sm.add_widget(ScreenSimpleData(name='screensimpledata'))
        return sm

def messageBox(title, content):
    pop = Popup(title=title,
                content=Label(text=content),
                size_hint=(None, None), size=(400, 400))
    pop.open()


if __name__ == '__main__':
    MainApp().run()
