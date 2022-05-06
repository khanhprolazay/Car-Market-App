from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.screenmanager import ScreenManager

class UI(Factory.ScreenManager):
    pass

class Main(MDApp):
    def build(self):
        return UI()

if __name__ == "__main__":
    Main().run()