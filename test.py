from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from screen_manager.screen_simple_data import ScreenSimpleData

Builder.load_file('screen_manager/screen_simple_data.kv')
Builder.load_file('components/car_card.kv')

class CarMarketApp(MDApp):
    def build(self):
        Window.size = [300, 600]
        screen_manager = ScreenManager()
        screen_manager.add_widget(ScreenSimpleData())
        return screen_manager

if __name__ == '__main__':
    CarMarketApp().run()