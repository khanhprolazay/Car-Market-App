from kaki.app import App
from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.core.window import Window
import os


class Live(App, MDApp):
    CLASSES = {
        "UI": "hotreload"
    }

    KV_FILES = {
        os.path.join(os.getcwd(), 'hot_reload/layout.kv')
    }

    AUTORELOADER_PATHS = [
            (".", {"recursive": True}),     
    ]

    def build_app(self, first = False):
        return Factory.UI()

Window.size = [300, 600]
Live().run()