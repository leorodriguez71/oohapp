from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ColorProperty, NumericProperty, BooleanProperty, StringProperty
import requests

class RoundedNormalButton(Button):
    pass

class CustomTextInput(FloatLayout):
    line_color = ColorProperty((0.8, 0.8, 0.8, 1))  # Color gris claro por defecto
    line_width = NumericProperty(1.5)  # Grosor de línea por defecto
    password = BooleanProperty(False)  # Propiedad para activar/desactivar modo contraseña
    text = StringProperty('')  # Propiedad para acceder al texto ingresado

    def update_line(self, focused):
        if focused:
            self.line_color = (0, 0.6, 0.8, 1)  # Cambia a turquesa al enfocar
            self.line_width = 2  # Aumenta el grosor de la línea
        else:
            self.line_color = (0.8, 0.8, 0.8, 1)  # Vuelve al color gris cuando no está enfocado
            self.line_width = 1.5  # Grosor normal

    def on_text(self, instance, value):
        # Actualiza el TextInput interno cuando cambia la propiedad 'text'
        self.ids.input_field.text = value

    def on_textinput_text(self, instance, value):
        # Sincroniza la propiedad 'text' con el contenido del TextInput
        self.text = value



class Inicio(Screen):
    def go_login(self):
        self.manager.current = 'Login'

class Principal(Screen):
    def on_pre_enter(self):
        if not hasattr(self.manager, 'sec_token'):
            print('no tengo')
            self.manager.current = 'Login'
            return
        headers = {
            'Authorization': f'Token {self.manager.sec_token}',  
            'Content-Type': 'application/json',
        }
        
        params = {
            'usuario': self.manager.usuario,
        }
        url = 'http://127.0.0.1:3000/api/mant/get-list'
        response = requests.get(url, headers=headers, params=params) 
        if response.status_code == 200:
            resp = response.json()
            if resp['resultado'] == 0:
                print(resp['data'])
                self.ids.vv.Clear()
                self.ids.vv.cols = 3
                self.ids.vv.AddTitle("Codigo")
                self.ids.vv.AddTitle("Direccion")
                self.ids.vv.AddTitle("Fecha")
                for mant in resp['data']:
                    self.ids.vv.AddGrid(mant['codigo'], '')
                    self.ids.vv.AddGrid(mant['direccion'], '')
                    self.ids.vv.AddGrid(mant['fecha'], '')
        else:
            print('error')
            self.manager.current = 'Login'
            return




class Login(Screen):
    def validar_usuario(self):
        usuario = self.ids.txtUsuario.text
        password = self.ids.txtPassword.text
        data = {
            'usuario': usuario,
            'password': password,
        }
        url = 'http://127.0.0.1:3000/api/auth/login_secure'
        response = requests.post(url, json=data)
        if response.status_code == 200:
             result = response.json()
             print(result)
             if result['resultado'] == 0:
                 self.manager.usuario = usuario
                 self.manager.sec_token = result['token']
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
