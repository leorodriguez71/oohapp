from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import *
from kivy.metrics import dp, sp
from kivy.core.window import Window
from kivy.graphics import *
from kivy.uix.image import Image
from kivy.utils import platform

class VulcanView(BoxLayout):
    def __init__(self, **kwargs):
        super(VulcanView, self).__init__(**kwargs)
        self.cajaVert = BoxLayout(orientation='vertical')
        self.titulos = BoxLayout(orientation='horizontal',  size_hint= (1, None), height = dp(50))
        self.sv = ScrollView(scroll_type=['bars', 'content'], bar_width='10dp')
        self.sv.scroll_timeout = 150
        self.grilla = GridLayout(cols=1, size_hint_y=None, row_default_height=dp(50), row_force_default=True)
        self.sv.add_widget(self.grilla)
        self.cajaVert.add_widget(self.titulos)
        self.cajaVert.add_widget(self.sv)
		#self.add_widget(self.sv)
        self.add_widget(self.cajaVert)
        self.grilla.bind(minimum_height=self.grilla.setter('height'))
        if platform in ('linux', 'windows', 'macosx'):
            self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
            self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self.register_event_type('on_selection')
        self.is_focusable = True

    cols = NumericProperty(1)
    row_selection = BooleanProperty(True)
    titulos_visibles = BooleanProperty(True)
    background_color = ListProperty([0,0,0,1])
    text_color = ListProperty([1,1,1,1])
    title_background_color = ListProperty([1,1,1,1])
    title_text_color = ListProperty([0,0,0,1])
    selected_text_color = ListProperty([1,0,0,1])
    selected_background_color = ListProperty([0,0,0,1])
    cols_size_hint = DictProperty({})
    _tituloCont = NumericProperty(1)
    _filaActual = NumericProperty(0)
    _columnaActual = NumericProperty(0)
    _ultimaFila = NumericProperty(-1)
    _ultimaColumna = NumericProperty(0)

    def on_titulos_visibles(self, instancia, valor):
        self.cajaVert.clear_widgets()
        if valor:
            self.cajaVert.add_widget(self.titulos)
            self.cajaVert.add_widget(self.sv)
        else:
            self.cajaVert.add_widget(self.sv)
    def on_selection(self, fila):
        pass
    def ordenarColumna(self, objeto):
        pass
    def on_row_selection(self, instance, value):
        pass
    def on_cols(self, instance, value):
        self.grilla.cols = value
        self.grilla.clear_widgets()
        self._tituloCont = 1
        self._filaActual = 0
        self._columnaActual = 0
        self._ultimaFila = -1
        self._ultimaColumna = 0
    def GetNodeGrid(self, fila, columna):
        for node in self.grilla.children:
            if node != 'T':
                if node.fila == fila and node.columna == columna:
                    return node
        return None
    def Clear(self):
        self.grilla.clear_widgets()
        self.titulos.clear_widgets()
        self._tituloCont = 1
        self._filaActual = 0
        self._columnaActual = 0
        self._ultimaFila = -1
        self._ultimaColumna = 0
    def GetRows(self):
        filas = 0
        for node in self.grilla.children:
            if node._tipo != 'T':
                if node.columna == 0:
                    filas += 1
        return filas
    def GetSelectedRow(self):
        return self._filaActual
    def GetSelectedCol(self):
        return self._columnaActual
    def GetSelection(self):
        if self.row_selection:
            return self._filaActual
        else:
            return self.GetNodelGrid(self, self._filaActual, self._columnaActual)
    def SetTextGrid(self, fila, columna, texto, adicional):
        for node in self.grilla.children:
            if node._tipo != 'T':
                if node.fila == fila and node.columna == columna:
                    node.text = texto
                    node.adicional = adicional
    def SetImageGrid(self, fila, columna, imagen, adicional):
        for node in self.grilla.children:
            if node._tipo != 'T':
                if node.fila == fila and node.columna == columna and node._tipo == 'I':
                    node.source = imagen
                    node.adicional = adicional
    def GetImageGrid(self, fila, columna):
        for node in self.grilla.children:
            if node._tipo != 'T':
                if node.fila == fila and node.columna == columna:
                    return node.source
    def GetTextGrid(self, fila, columna):
        for node in self.grilla.children:
            if node._tipo != 'T':
                if node.fila == fila and node.columna == columna:
                    return node.text
        return ""
    def GetAdicionalGrid(self, fila, columna):
        for node in self.grilla.children:
            if node._tipo != 'T':
                if node.fila == fila and node.columna == columna:
                    return node.adicional
        return ""

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        fila = self._filaActual
        if keycode[1] == 'down':
            if fila >= 0 and fila < self._ultimaFila:
                fila = fila + 1
                for node in self.grilla.children:
                    if node._tipo != 'T':
                        if node.fila == fila:
                            self._on_press_lista(node)
                            self.sv.scroll_to(node)
                            return True
        elif keycode[1] == 'up':
            if fila > 0 and self._ultimaFila > 0:
                fila = fila - 1
                for node in self.grilla.children:
                    if node._tipo != 'T':
                        if node.fila == fila:
                            self._on_press_lista(node)
                            self.sv.scroll_to(node)
                            return True
        return True


    def _on_press_lista(self, nodo):
        if nodo._tipo != 'T':
            fila = nodo.fila
            columna = nodo.columna
            self._filaActual = fila
            self._columnaActual = nodo.columna
            for node in self.grilla.children:
                if node._tipo != 'T':
                    if self.row_selection:
                        if node.fila == fila:
                            node.selected = True
                            node.color = self.selected_text_color
                            node.background_color = self.selected_background_color
                        else:
                            node.selected = False
                            node.color = self.text_color
                            node.background_color = self.background_color
                    else:
                        if node.fila == fila and node.columna == columna:
                            node.selected = True
                            node.color = self.selected_text_color
                            node.background_color = self.selected_background_color
                        else:
                            node.selected = False
                            node.color = self.text_color
                            node.background_color = self.background_color
            self.dispatch('on_selection', self._filaActual)

    def AddTitle(self, texto):
        if self._tituloCont <= self.cols:
            but = Button(text=texto, on_release=self.ordenarColumna)
            but.nroCol = self._tituloCont - 1
            but.background_normal= ''
            but.background_down = ''
            if self.cols_size_hint.get(str(but.nroCol)) != None:
                but.size_hint_x = self.cols_size_hint[str(but.nroCol)]
            but._tipo = 'T'
            self._tituloCont = self._tituloCont + 1
            but.color = self.title_text_color
            but.background_color = self.title_background_color
            #self.grilla.add_widget(but)
            self.titulos.add_widget(but)

    def AddImageGrid(self, imagen, adicional):
        if self._ultimaColumna == 0:
            self._ultimaFila = self._ultimaFila + 1
        lab = Image(source=imagen)
        lab.adicional = adicional
        lab.fila = self._ultimaFila
        lab.columna = self._ultimaColumna
        lab._tipo = 'I'
        lab.selected = False
        self.grilla.add_widget(lab)
        if self._ultimaColumna == self.cols - 1:
            self._ultimaColumna = 0
        else:
            self._ultimaColumna = self._ultimaColumna + 1


    def AddWidgetGrid(self, lab, adicional):
        if self._ultimaColumna == 0:
            self._ultimaFila = self._ultimaFila + 1
        lab.adicional = adicional
        lab.fila = self._ultimaFila
        lab.columna = self._ultimaColumna
        lab._tipo = 'W'
        if self.cols_size_hint.get(str(lab.columna)) != None:
            lab.size_hint_x = self.cols_size_hint[str(lab.columna)]
        lab.selected = False
        self.grilla.add_widget(lab)
        if self._ultimaColumna == self.cols - 1:
            self._ultimaColumna = 0
        else:
            self._ultimaColumna = self._ultimaColumna + 1


    def AddGrid(self, texto, adicional):
        if self._ultimaColumna == 0:
            self._ultimaFila = self._ultimaFila + 1
        lab = Button(text=texto)
        lab.background_normal= ''
        lab.background_down = ''
        lab.background_color= self.background_color
        lab.color = self.text_color
        lab.adicional = adicional
        lab.fila = self._ultimaFila
        lab.columna = self._ultimaColumna
        lab._tipo = 'G'
        if self.cols_size_hint.get(str(lab.columna)) != None:
            lab.size_hint_x = self.cols_size_hint[str(lab.columna)]

        lab.selected = False
        self.grilla.add_widget(lab)
        if self._ultimaColumna == self.cols - 1:
            self._ultimaColumna = 0
        else:
            self._ultimaColumna = self._ultimaColumna + 1
    def on_touch_down(self, touch):
        ret = super(VulcanView, self).on_touch_down(touch)
        if ret:
            x2, y2 = self.grilla.parent.to_local(touch.x, touch.y)
            for node in self.grilla.children:
                if node.collide_point(x2, y2):
                    self.savex = x2
                    self.savey = y2
                    self.savenode = node
            ret = True
        return ret
    def on_touch_up(self, touch):
        ret = super(VulcanView, self).on_touch_up(touch);
        if ret:
            for node in self.grilla.children:
                x2, y2 = self.grilla.parent.to_local(touch.x, touch.y)
                if node.collide_point(x2, y2):
                    if hasattr(self, 'savenode'):
                        if node == self.savenode:
                            if x2 <= self.savex + 10 and x2 >= self.savex - 10 and y2 <= self.savey + 10 and y2 >= self.savey - 10:
                                self._on_press_lista(node)
                                self.focus = True
                                if platform in ('linux', 'windows', 'macosx'):
                                    self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
                                    self._keyboard.bind(on_key_down=self._on_keyboard_down)

            ret = True
        return ret;

    def RemoveRow(self,fila):
        backTitle=[]
        backUp=[]
        ultfila = self._ultimaFila
        for tit in self.titulos.children:
            backTitle.append(tit)
        for node in self.grilla.children:
            if node.fila != fila :
                if node.fila > fila:
                    node.fila = node.fila -1
                backUp.append (node)
        self.Clear()
        for t in reversed(backTitle):
            self.titulos.add_widget(t)
        for i in reversed(backUp):
            self.grilla.add_widget(i)
        self._ultimaFila = ultfila -1
        self._filaActual = 0
    def MoveRow(self,filaOrg,filaDest):
        ultfila = self._ultimaFila
        backTitle=[]
        backUp=[]
        backUpOrg=[]
        backUpDest=[]
        for tit in self.titulos.children:
            backTitle.append(tit)
        for node in self.grilla.children:
            node.fila2 = -1
            if node.fila == filaOrg :
                node.fila2 = filaOrg
                backUpOrg.append (node)
            if node.fila == filaDest :
                node.fila2 = filaDest
                backUpDest.append (node)
            backUp.append (node)
        self.Clear()
        for t in reversed(backTitle):
            self.titulos.add_widget(t)
        indexOrg = len(backUpOrg)-1
        indexDest = len(backUpDest)-1
        for i in reversed(backUp):
            if i.fila2 == filaOrg:
                backUpDest[indexDest].fila = filaOrg
                self.grilla.add_widget(backUpDest[indexDest])
                indexDest = indexDest -1
            elif i.fila2 == filaDest:
                backUpOrg[indexOrg].fila = filaDest
                self.grilla.add_widget(backUpOrg[indexOrg])
                indexOrg = indexOrg -1
            else:
                self.grilla.add_widget(i)
        self._ultimaFila = ultfila
        self._filaActual = filaDest
