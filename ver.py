from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty, StringProperty
import calendar
from datetime import datetime


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


class DatePickerApp(App):
    def build(self):
        return MyScreen()

    def open_date_picker(self, target_input):
        # Pasamos el TextInput que activó el DatePicker
        date_picker = DatePicker(target_input=target_input)
        date_picker.bind(on_dismiss=self.on_date_selected)
        date_picker.open()

    def on_date_selected(self, instance):
        pass  # Ya no necesitamos manejar la fecha seleccionada aquí


class MyScreen(BoxLayout):
    pass


if __name__ == "__main__":
    DatePickerApp().run()
