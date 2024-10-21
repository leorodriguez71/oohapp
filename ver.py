from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

class MiWidget(BoxLayout):
    def __init__(self, **kwargs):
        super(MiWidget, self).__init__(**kwargs)

        # Crear un Label con un icono
        self.label = Label(
            text="\uE84D",  # Cambia esto por el código Unicode del icono deseado (ejemplo: "home")
            font_name="ttf/MaterialIcons-Regular.ttf",  # Ruta a tu archivo .ttf
            font_size='40sp'
        )
        
        # Crear un Button con un icono
        self.boton = Button(
            text="\uf2b9",  # Cambia esto por el código Unicode del icono deseado (ejemplo: "home")
            font_name="ttf/materialdesignicons-webfont.ttf",  # Ruta a tu archivo .ttf
            font_size='40sp',
            size_hint=(None, None),
            size=(100, 100)
        )

        self.add_widget(self.label)
        self.add_widget(self.boton)

class MiApp(App):
    def build(self):
        return MiWidget()

if __name__ == '__main__':
    MiApp().run()