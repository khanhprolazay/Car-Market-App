from kivymd.uix.screen import MDScreen
from components.car_card import CarCard 
from kivy.lang import Builder
from kivy.core.window import Window
import pandas

data = pandas.read_csv('data/Car_data.csv')

def GetLink(links):
    link = links.split()[0]
    link = "".join(c for c in link if c != '[' and c != ',' and c != "'")
    return link

class ScreenSimpleData(MDScreen):
    def on_pre_enter(self):
        self.list_items()

    def list_items(self):
        Window.size = [300, 600]
        for i in range(101, 120):
            self.ids.listitem.add_widget(CarCard(   car_image = GetLink(data['Link_image'][i]),
                                                    inform_car = data['Tieu_de'][i],
                                                    price_car = data['gia'][i],
                                                    status_car = data['Tinh_trang'][i],
                                                    manufacture_year_car = data['Nam_san_xuat'][i],
                                                    km_car = data['Km_da_di'][i],
                                                    shift_stick_inform_car = data['Hop_so'][i],
                                                    place = 'Thành phố Hồ Chí Minh',
                                                    day = '4-6-2022' ))
    
    def load_all_kivy_file(self):
        Builder.load_file('screen_manager/screen_simple_data.kv')
        Builder.load_file('components/car_card.kv')