from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.properties import ColorProperty, NumericProperty, BooleanProperty, StringProperty, OptionProperty, ObjectProperty, ListProperty
import requests
from kivy.uix.popup import Popup
from kivy.graphics.texture import Texture
from kivy.core.window import Window
from kivy.clock import Clock
import cv2
import calendar
from datetime import datetime
import re

class RoundedNormalButton(Button):
    pass


class DatePicker(Popup):
    selected_date = ObjectProperty(None)
    display_month_year = StringProperty()

    def __init__(self, target_input=None, **kwargs):
        super().__init__(**kwargs)
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.target_input = target_input  # Guardamos la referencia del TextInput
        self.update_month_year()  # Actualizamos el texto del mes/año
        self.create_calendar(self.current_year, self.current_month)

    def create_calendar(self, year, month):
        self.ids.calendar_container.clear_widgets()

        cal = calendar.monthcalendar(year, month)
        days_of_week = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

        for day in days_of_week:
            self.ids.calendar_container.add_widget(Label(text=day, size_hint_y=None, height='40dp'))

        for week in cal:
            for day in week:
                if day == 0:
                    self.ids.calendar_container.add_widget(Label(text=""))
                else:
                    day_button = Button(text=str(day), on_press=self.select_day)
                    self.ids.calendar_container.add_widget(day_button)

    def select_day(self, instance):
        day = instance.text
        self.selected_date = f"{self.current_year}-{self.current_month:02d}-{int(day):02d}"
        # Si hay un TextInput objetivo, se actualiza con la fecha seleccionada
        if self.target_input:
            self.target_input.text = self.selected_date
        print("salid")
        self.dismiss()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_month_year()
        self.create_calendar(self.current_year, self.current_month)

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_month_year()
        self.create_calendar(self.current_year, self.current_month)

    def update_month_year(self):
        self.display_month_year = f"{self.current_month:02d}/{self.current_year}"

class WidgetCamera(BoxLayout):
    photo_name = StringProperty("foto.jpg")  # Propiedad para el nombre de la foto
    image_texture = None

    def __init__(self, **kwargs):
        super(WidgetCamera, self).__init__(**kwargs)

    def capture_photo(self):
        # Configura la captura de video
        self.capture = cv2.VideoCapture(0)

        # Verifica si la cámara se abre correctamente
        if not self.capture.isOpened():
            print("Error: No se puede abrir la cámara.")
            return

        # Captura una imagen
        ret, frame = self.capture.read()
        if ret:
            # Convierte la imagen a formato de textura
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
            self.image_texture = texture
            self.ids.camera_image.texture = self.image_texture
            
            # Guarda la foto
            cv2.imwrite(self.photo_name, frame)

        # Libera la cámara
        self.capture.release()

    def on_kill(self):
        if self.capture and self.capture.isOpened():
            self.capture.release()



class CustomTextInput(FloatLayout):
    line_color = ColorProperty((0.8, 0.8, 0.8, 1))  # Color gris claro por defecto
    line_width = NumericProperty(1.5)  # Grosor de línea por defecto
    password = BooleanProperty(False)  # Propiedad para activar/desactivar modo contraseña
    text = StringProperty('')  # Propiedad para acceder al texto ingresado
    max_chars = NumericProperty(0)  # Máximo de caracteres permitidos (0 para infinito)
    input_type = OptionProperty('text', options=['text', 'numeric', 'date', 'note'])  # Tipo de entrada: texto o numérico
    max_decimals = NumericProperty(0)  # Cantidad máxima de decimales permitidos si es numérico
    error_message = StringProperty('')  # Mensaje de error
    required = BooleanProperty(False)  # Propiedad que define si el campo es obligatorio
    write_tab = BooleanProperty(False)  # Si True, no pasa al siguiente textbox
    multiline = BooleanProperty(False)  # Si True, no pasa al siguiente textbox
    on_last_field = ObjectProperty(None)
    hint_text = StringProperty('') 
    input_field = ObjectProperty(None)
    focus = BooleanProperty(False)
    abrir = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(CustomTextInput, self).__init__(**kwargs)
        # Registrar el evento de teclado
        self.bind(input_field=self._connect_focus)
        Window.bind(on_key_down=self.on_key_down)
        Clock.schedule_once(self.ejecutar_en_proximo_frame)

    def ejecutar_en_proximo_frame(self, dt):
        self.input_field.bind(text=self.validate_text)
        if self.input_type == 'date':
            self.input_field.bind(on_touch_down=self._on_touch_down)
        elif self.input_type == 'note':
            self.multiline = True  # Habilitar multiline
            self.input_field.multiline = True
            self.ids.input_field.height = '100dp'  # Aumentar la altura del TextInput
            self.ids.input_field.size_hint_y = None  # Deshabilitar el ajuste de tamaño automático
            self.ids.input_field.pos_hint = {'center_x': 0.5, 'center_y': 0.5}

    def _connect_focus(self, instance, value):
        """Conecta el 'focus' del TextInput interno con el CustomTextInput"""
        if self.input_field:
            self.input_field.bind(focus=self._on_focus)

    def _on_focus(self, instance, value):
        """Cuando el TextInput interno cambia de foco, actualizamos la propiedad 'focus' del CustomTextInput"""
        self.focus = value

    def _on_touch_down(self, instance, touch):
        """Controla el comportamiento cuando se hace clic en el CustomTextInput"""
        if self.collide_point(*touch.pos):
            print('abrir=',self.abrir)
            if self.abrir:
                App.get_running_app().open_date_picker(self.input_field)
                touch.grab(self)  # Agregar el toque al widget
                self.abrir = False
            else:
                self.abrir = True

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
                else:
                    return False
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
        elif self.input_type == 'date':
            if not self.validar_fecha(self.text):
                self.error_message = "Fecha invalida"

    def on_text(self, instance, value):
        # Actualiza el TextInput interno cuando cambia la propiedad 'text'
        self.ids.input_field.text = value

    def on_textinput_text(self, instance, value):
        # Sincroniza la propiedad 'text' con el contenido del TextInput
        self.text = value
    def validar_fecha(self, fecha):
        # Expresión regular para validar el formato yyyy-mm-dd
        patron = r'^\d{4}-\d{2}-\d{2}$'
        
        # Verificar si la fecha coincide con el patrón
        if not re.match(patron, fecha):
            return False
        
        # Descomponer la fecha en año, mes y día
        año, mes, dia = map(int, fecha.split('-'))
        
        # Verificar si la fecha es válida
        try:
            datetime(año, mes, dia)
            return True
        except ValueError:
            return False

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
                    self.ids.vv.AddGrid(mant['codigo'], mant['id'])
                    self.ids.vv.AddGrid(mant['direccion'], '')
                    self.ids.vv.AddGrid(mant['fecha'], '')
        else:
            self.manager.current = 'Login'
            return
    def go_mant(self):
        self.manager.mant_id = self.ids.vv.GetAdicionalGrid(self.ids.vv.GetSelectedRow(), 0)
        self.manager.current = 'Mantenimiento'

class Mantenimiento(Screen):
    def actualizar(self):
        if not hasattr(self.manager, 'sec_token'):
            self.manager.current = 'Login'
            return
        headers = {
            'Authorization': f'Token {self.manager.sec_token}',  
        }
        params = {
            'usuario': self.manager.usuario,
            'fecha': self.ids.txtFecha.text,
            'obs': self.ids.txtObs.text,
            'id': self.manager.mant_id,
        }
        files = {}
        if self.ids.picAdjunto1.image_texture is not None:
            with open(self.ids.picAdjunto1.photo_name, 'rb') as adjunto1:
                files['adjunto1'] = adjunto1
        if self.ids.picAdjunto2.image_texture is not None:
            with open(self.ids.picAdjunto2.photo_name, 'rb') as adjunto2:
                files['adjunto2'] = adjunto2
        url = 'http://127.0.0.1:3000/api/mant/update'
        response = requests.post(url, files = files, headers=headers, data = params)
        if response.status_code == 200:
            self.manager.current = 'Principal'
        else:
            print('error')

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
        sm.add_widget(Mantenimiento(name = "Mantenimiento"))

        return sm
    def open_date_picker(self, target_input):
        print('abrir')
        date_picker = DatePicker(target_input=target_input)
        date_picker.bind(on_dismiss=self.on_date_selected)
        date_picker.open()

    def on_date_selected(self, instance):
        pass  # Ya no necesitamos manejar la fecha seleccionada aquí

main = OohApp()
main.run()
