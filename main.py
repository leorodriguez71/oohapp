from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
import requests

class RoundedNormalButton(Button):
    pass

class Inicio(Screen):
    def go_login(self):
        self.manager.current = 'Login'

class Principal(Screen):
    def on_pre_enter(self):
        for mant in self.manager.lista_mant:
            self.ids.lblCarga.text = self.ids.lblCarga.text + mant['direccion']


class Login(Screen):
    def validar_usuario(self):
        usuario = self.ids.txtUsuario.text
        password = self.ids.txtPassword.text
        data = {
            'usuario': usuario,
            'password': password,
        }
        url = 'http://127.0.0.1:3000/api/auth/login'
        response = requests.get(url, params=data)
        if response.status_code == 200:
             result = response.json()
             if result['resultado'] == 0:
                 lista = result['data']
                 self.manager.lista_mant = lista
                 self.manager.current = 'Principal'
             else:
                 print('afueeeeraaaa')
        else:
            print('error comm')


class OohApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Inicio(name = "Inicio"))
        sm.add_widget(Login(name = "Login"))
        sm.add_widget(Principal(name = "Principal"))

        return sm

main = OohApp()
main.run()
