from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ColorProperty, NumericProperty, BooleanProperty, StringProperty, OptionProperty, ObjectProperty
import requests
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle 
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
class RoundedNormalButton(Button):
    pass



class CustomTextInput(FloatLayout):
    line_color = ColorProperty((0.8, 0.8, 0.8, 1))  # Color gris claro por defecto
    line_width = NumericProperty(1.5)  # Grosor de línea por defecto
    password = BooleanProperty(False)  # Propiedad para activar/desactivar modo contraseña
    text = StringProperty('')  # Propiedad para acceder al texto ingresado
    max_chars = NumericProperty(0)  # Máximo de caracteres permitidos (0 para infinito)
    input_type = OptionProperty('text', options=['text', 'numeric'])  # Tipo de entrada: texto o numérico
    max_decimals = NumericProperty(0)  # Cantidad máxima de decimales permitidos si es numérico
    error_message = StringProperty('')  # Mensaje de error
    required = BooleanProperty(False)  # Propiedad que define si el campo es obligatorio
    write_tab = BooleanProperty(False)  # Si True, no pasa al siguiente textbox
    multiline = BooleanProperty(False)  # Si True, no pasa al siguiente textbox
    on_last_field = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CustomTextInput, self).__init__(**kwargs)
        # Registrar el evento de teclado
        Window.bind(on_key_down=self.on_key_down)

    def update_line(self, focused):
        if focused:
            self.line_color = (0, 0.6, 0.8, 1)  # Cambia a turquesa al enfocar
            self.line_width = 2  # Aumenta el grosor de la línea
        else:
            self.line_color = (0.8, 0.8, 0.8, 1)  # Vuelve al color gris cuando no está enfocado
            self.line_width = 1.5  # Grosor normal

    def on_key_down(self, window, key, *args):
        if self.ids.input_field.focus:
            if key == 9:  # Cambia al siguiente textbox con Tab
                if not self.write_tab:
                    self.cambiar()
                return True  # Evitar el comportamiento por defecto
            if key == 13 or key == 271:  # Cambia al siguiente textbox con Enter
                if not self.multiline:
                    self.cambiar()
                return True  # Evitar el comportamiento por defecto
    def obtener_screen(self):
        actual = self
        while actual:
            if isinstance(actual, Screen):
                return actual
            actual = actual.parent
        return None

    def get_list_textinput(self, parent):
        for child in parent.children:
            if isinstance(child, TextInput):
                self.lista_ti.append(child)
            self.get_list_textinput( child)

    def set_next_textinput(self, actual):
        encontrado = False
        for t in reversed(self.lista_ti):
            if encontrado:
                t.focus = True
                return t
            else:
                if t == actual:
                    print('lo encontre')
                    encontrado = True
        return None
    def cambiar(self):
        pantalla = self.obtener_screen()
        actual_text = self.ids.input_field
        self.lista_ti = []
        self.get_list_textinput(pantalla)
        foco = self.set_next_textinput( actual_text)
        if foco is None:
            if self.on_last_field is not None:
                self.on_last_field()

    def validate_text(self, instance, value):
        # Si el campo es obligatorio y está vacío
        if self.required and not value:
            self.error_message = "Este campo es obligatorio."
        else:
            self.error_message = ""

        # Limitar la cantidad de caracteres si max_chars está definido
        if self.max_chars > 0 and len(value) > self.max_chars:
            self.ids.input_field.text = value[:self.max_chars]
            value = value[:self.max_chars]
            self.error_message = f"Máximo {self.max_chars} caracteres permitidos."
        else:
            self.error_message = self.error_message or ""  # Mantener el mensaje de error anterior si existe

        # Validación para entradas numéricas
        if self.input_type == 'numeric':
            # Permitir solo números y punto decimal
            if not value.replace('.', '').isdigit():
                value = ''.join([c for c in value if c.isdigit() or c == '.'])
                self.error_message = "Solo números permitidos."

            # Limitar la cantidad de decimales
            if '.' in value:
                integer_part, decimal_part = value.split('.', 1)
                if len(decimal_part) > self.max_decimals:
                    value = f"{integer_part}.{decimal_part[:self.max_decimals]}"
                    self.error_message = f"Máximo {self.max_decimals} decimales permitidos."
                else:
                    self.error_message = self.error_message or ""

            self.ids.input_field.text = value

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
    def go_mant(self):
        print('mantenimieto')



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
                 self.ids.txtUsuario.error_message = 'Usuario invalido'
        else:
            self.ids.txtUsuario.error_message = 'Usuario o password invalido'


class OohApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(Inicio(name = "Inicio"))
        sm.add_widget(Login(name = "Login"))
        sm.add_widget(Principal(name = "Principal"))

        return sm

main = OohApp()
main.run()
