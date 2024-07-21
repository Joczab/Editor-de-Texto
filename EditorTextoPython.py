# pip install future
# pip install ntk
import os
import tkinter as tk
from idlelib import *
from tkinter import *
from tkinter import filedialog as FileDialog
from io import open
from tkinter.colorchooser import askcolor
from tkinter.font import Font, families
from tkinter import Menu
global right_click_text_menu
import re
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:  # Python 3
    import tkinter as tk
    from tkinter import ttk
import ply.lex as lex

frames = []


class CustomNotebook(ttk.Notebook):
    """A ttk Notebook with close buttons on each tab"""

    __initialized = False

    def __init__(self, *args, **kwargs):
        if not self.__initialized:
            self.__initialize_custom_style()
            self.__inititialized = True

        kwargs["style"] = "CustomNotebook"
        ttk.Notebook.__init__(self, *args, **kwargs)

        self._active = None

        self.bind("<ButtonPress-1>", self.on_close_press, True)
        self.bind("<ButtonRelease-1>", self.on_close_release)

    def on_close_press(self, event):
        """Called when the button is pressed over the close button"""

        element = self.identify(event.x, event.y)

        if "close" in element:
            index = self.index("@%d,%d" % (event.x, event.y))
            del frames[index]
            self.state(['pressed'])
            self._active = index
            return "break"

    def on_close_release(self, event):
        """Called when the button is released"""
        if not self.instate(['pressed']):
            return

        element =  self.identify(event.x, event.y)
        if "close" not in element:
            # user moved the mouse off of the close button
            return

        index = self.index("@%d,%d" % (event.x, event.y))

        if self._active == index:
            self.forget(index)
            self.event_generate("<<NotebookTabClosed>>")

        self.state(["!pressed"])
        self._active = None

    def __initialize_custom_style(self):
        style = ttk.Style()
        self.images = (
            tk.PhotoImage("img_close", data='''
                R0lGODlhCAAIAMIBAAAAADs7O4+Pj9nZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
                '''),
            tk.PhotoImage("img_closeactive", data='''
                R0lGODlhCAAIAMIEAAAAAP/SAP/bNNnZ2cbGxsbGxsbGxsbGxiH5BAEKAAQALAAA
                AAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU5kEJADs=
                '''),
            tk.PhotoImage("img_closepressed", data='''
                R0lGODlhCAAIAMIEAAAAAOUqKv9mZtnZ2Ts7Ozs7Ozs7Ozs7OyH+EUNyZWF0ZWQg
                d2l0aCBHSU1QACH5BAEKAAQALAAAAAAIAAgAAAMVGDBEA0qNJyGw7AmxmuaZhWEU
                5kEJADs=
            ''')
        )

        style.element_create("close", "image", "img_close",
                            ("active", "pressed", "!disabled", "img_closepressed"),
                            ("active", "!disabled", "img_closeactive"), border=8, sticky='')
        style.layout("CustomNotebook", [("CustomNotebook.client", {"sticky": "nswe"})])
        style.layout("CustomNotebook.Tab", [
            ("CustomNotebook.tab", {
                "sticky": "nswe",
                "children": [
                    ("CustomNotebook.padding", {
                        "side": "top",
                        "sticky": "nswe",
                        "children": [
                            ("CustomNotebook.focus", {
                                "side": "top",
                                "sticky": "nswe",
                                "children": [
                                    ("CustomNotebook.label", {"side": "left", "sticky": ''}),
                                    ("CustomNotebook.close", {"side": "left", "sticky": ''}),
                                ]
                        })
                    ]
                })
            ]
        })
    ])

# Lista de palabras clave de Python
palabras_clave = ['import', 'def', 'from', 'global', 'if', 'else','elif','match','while','int','for','return']

# Patrones para números e identificadores

patron_numero = r'^\d+(\.\d+)?$'
patron_identificador = r'^[a-zA-Z_]\w*$'

# Lista de nombres de tokens. Esta es una parte crucial que faltaba.
tokens = (
    'SUMA', 'RESTA', 'MULTIPLICACION', 'DIVISION', 'IGUAL',
    'PARENTESIS_IZQUIERDO', 'PARENTESIS_DERECHO', 'NUMBER', 'LETRA', 'DOS_PUNTOS', 'COMA'
)

# Continuación de las reglas de expresiones regulares para tokens simples
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULTIPLICACION = r'\*'
t_DIVISION = r'/'
t_IGUAL = r'='
t_PARENTESIS_IZQUIERDO = r'\('
t_PARENTESIS_DERECHO = r'\)'
t_LETRA = r'[a-zA-Z_][a-zA-Z0-9_]*'
t_DOS_PUNTOS = r':'
t_COMA = r','

# Ignorar espacios en blanco
t_ignore = ' \t'

# Definición de número
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Definición de error léxico
def t_error(t):
    print(f"Caracter no registrado '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Función para analizar el texto del editor
def analizar_texto(texto):
    lexer.input(texto)
    nueva_ventana = tk.Toplevel()
    nueva_ventana.title("Resultados del Analisis Sintactico")
    nueva_ventana.geometry("400x400")
    nueva_ventana.resizable(False, False)
    nueva_ventana.config(bg="white")
    texto_resultados = tk.Text(nueva_ventana, wrap='word')
    texto_resultados.pack(expand=True, fill='both')
    for tok in lexer:
        texto_resultados.insert('end', f"{tok}\n")  
    texto_resultados.config(state='disabled')

def analisis_sintactico():

    mensaje.set('Abrir fichero')
    ruta = FileDialog.askopenfilename(initialdir='.', filetypes=(("Archivos de Texto", "*.txt"),
                                                                 ("Archivos .py", "*.py"),
                                                                 ("Todos los Archivos", "*.*")),
                                      title="Abrir un fichero.")
    with open(ruta, 'r', encoding='utf-8') as archivo:
        texto_prueba = archivo.read()
    resultados_sintactico = analizar_texto(texto_prueba)
    return resultados_sintactico
       
def analizar_lexico(texto):
    # Inicializar un diccionario para clasificar los tokens
    clasificacion_tokens = {
        'PALABRA CLAVE': [],
        'NUMERO': [],
        'IDENTIFICADOR': [],
        'SIMBOLO': []
    }
    # Dividir el texto en tokens
    tokens = re.findall(r'\w+|[^\w\s]', texto, re.UNICODE)

    for token in tokens:
        if token in palabras_clave:
            clasificacion_tokens['PALABRA CLAVE'].append(token)
        elif re.match(patron_numero, token):
            clasificacion_tokens['NUMERO'].append(token)
        elif re.match(patron_identificador, token) and token not in palabras_clave:
            clasificacion_tokens['IDENTIFICADOR'].append(token)
        else:
            clasificacion_tokens['SIMBOLO'].append(token)

    # Retornar el diccionario con los tokens clasificados
    return mostrar_resultados_ordenados(clasificacion_tokens)


# Para mostrar los resultados de manera ordenada

def mostrar_resultados_ordenados(clasificacion_tokens):
    # crear nueva ventana
    nueva_ventana = tk.Toplevel()
    nueva_ventana.title("Resultados del Analisis Lexico")
    nueva_ventana.geometry("400x400")
    nueva_ventana.resizable(False, False)
    nueva_ventana.config(bg="white")
    
    # crear un widget de texto
    texto_resultados = tk.Text(nueva_ventana, wrap = 'word')
    texto_resultados.pack(expand=True, fill='both')
    
    for categoria in sorted(clasificacion_tokens):
        texto_resultados.insert('end', f"{categoria}:\n")
        contador_tokens = 0   
        for token in sorted(clasificacion_tokens[categoria]):
            texto_resultados.insert('end', f" - {token}\n") 
            contador_tokens += 1
        texto_resultados.insert('end', f"Total de tokens de la categoría {categoria}: {contador_tokens}\n\n")
         
        # deshabilitar la edición del widget de texto
    texto_resultados.config(state='disabled')
        
    


def copy(texto):
    texto.event_generate('<<Copy>>')


def cut(texto):
    texto.event_generate('<<Cut>>')


def paste(texto):
    texto.event_generate('<<Paste>>')


def undo(texto):
    texto.event_generate('<<Undo>>')


def redo(texto):
    texto.event_generate('<<Redo>>')


def select_all(texto,event=None):
    texto.tag_add('sel', '1.0', 'end')
    return "break"


def changeBg(texto):
    (tripple, hexstr) = askcolor()
    if hexstr:
        texto.config(background=hexstr)


def changeFg(texto):
    (triple, hexstr) = askcolor()
    if hexstr:
        texto.config(fg=hexstr)


def bold(texto):
    F_font = ('bold', 30)
    texto.font = F_font


def right_click_menu(event):
    # mostra il menù partendo dalla posizione definita con .post()
    right_click_text_menu.post(event.x_root, event.y_root)


def right_click_menu_destroy(widget):

    # semplicemente toglie il menù apparentemente senza perdite di memoria
    right_click_text_menu.unpost()

def nuevo():
    texto = tk.Text(pestana)
    frames.append(texto)
    global right_click_text_menu

    right_click_text_menu = Menu(texto, tearoff=0,  background='#FFFFFF')
    right_click_text_menu.add_command(label=' Cortar ', command=lambda: texto.event_generate('<<Cut>>'))
    right_click_text_menu.add_command(label=' Copiar ', command=lambda: texto.event_generate('<<Copy>>'))
    right_click_text_menu.add_command(label=' Pegar ', command=lambda: texto.event_generate('<<Paste>>'))
    right_click_text_menu.add_command(label=' Seleccionar Todo ', command=select_all)

    S = tk.Scrollbar(texto)
    S.config(command=texto.yview)
    pestana.pack(fill="both", expand="true")
    S.pack(side=tk.RIGHT, fill=Y)
    texto.config(font=("Verdana", 12), bd=0, padx=1, pady=1, yscrollcommand=S.set, undo=1)
    texto.bind('<Button-3>', right_click_menu)
    texto.bind('<Button-1>', lambda event: right_click_menu_destroy(right_click_text_menu))
    pestana.add(texto,text="Nuevo fichero")

    mensaje.set("Nuevo fichero")
    ruta= ""
    texto.delete(1.0, "end")
    root.title("Editor de Texto en python")


def anilisis_lexico(ruta):
    
    
    mensaje.set('Abrir fichero')
    ruta = FileDialog.askopenfilename(initialdir='.', filetypes=(("Archivos de Texto", "*.txt"), 
                                                                 ("Archivos .py", "*.py"), 
                                                                 ("Todos los Archivos", "*.*")), 
                                      title="Abrir un fichero.")
    
    with open(ruta, 'r', encoding='utf-8') as archivo:
        texto_prueba = archivo.read()
    print(analizar_lexico(texto_prueba))
    
   
    
def abrir():
    global right_click_text_menu
    # Indicamos que la ruta es respecto a la variable global
    # Debemos de forzar esta lectura global porque los comandos
    # sólo son conscientes de las variables externas que son widgets
    
    texto=tk.Text(pestana)
    frames.append(texto)
    mensaje.set('Abrir fichero')


    ruta = FileDialog.askopenfilename(
        initialdir='.',
        filetypes=(  # Es una tupla con un elemento
            ("Archivos de Texto", "*.txt"),
            ("Archivos .py", "*.py"), 
            ("Todos los Archivos", "*.*"),
        ),
        title="Abrir un fichero."
    )
    nombre_archivo = os.path.basename(ruta)
    mensaje.set('Editor de Texto en python')
    # Si la ruta es válida abrimos el contenido en lectura
    if ruta != "":
        right_click_text_menu = Menu(texto, tearoff=0, background='#FFFFFF')
        right_click_text_menu.add_command(label=' Cortar ', command=lambda: texto.event_generate('<<Cut>>'))
        right_click_text_menu.add_command(label=' Copiar ', command=lambda: texto.event_generate('<<Copy>>'))
        right_click_text_menu.add_command(label=' Pegar ', command=lambda: texto.event_generate('<<Paste>>'))
        right_click_text_menu.add_command(label=' Seleccionar Todo ', command=select_all)

        S = tk.Scrollbar(texto)
        S.config(command=texto.yview)
        pestana.pack(side="top", fill="both", expand=True)
        S.pack(side=tk.RIGHT, fill=Y)
        texto.config(font=("Verdana", 12), bd=0, padx=1, pady=1, yscrollcommand=S.set, undo=1)
        texto.bind('<Button-3>', right_click_menu)
        texto.bind('<Button-1>', lambda event: right_click_menu_destroy(right_click_text_menu))
        pestana.add(texto, text= ruta)

        fichero = open(ruta, 'r')
        contenido = fichero.read()
        texto.delete(1.0, 'end')  # Nos aseguramos de que esté vacío
        texto.insert('insert', contenido)  # Le insertamos el contenido
        fichero.close()  # Cerramos el fichero
        root.title(nombre_archivo + " -- Editor de texto en Python")  # Cambiamos el título
        mensaje.set('Editor de Texto en python')

def guardar(texto:tk.Text):
    ruta = pestana.tab(pestana.select(), "text")
    mensaje.set("Guardar fichero")
    if ruta == "Nuevo fichero":
        guardar_como(texto)
    else:
        contenido = texto.get("1.0",END)
        fichero = open(ruta, 'w+')
        fichero.write(contenido)
        fichero.close()
        mensaje.set("Fichero guardado correctamente")



def guardar_como(texto):
    ruta = pestana.tab(pestana.select(), "text")

    mensaje.set("Guardar fichero como")

    fichero = FileDialog.asksaveasfile(title="Guardar fichero", mode="w", defaultextension="txt", 
                                       filetypes=[("Archivos de Texto", "*.txt"),
                                                  ("Archivos .py", "*.py"), 
                                                  ("Todos los Archivos", "*.*")])

    if fichero is not None:
        ruta = fichero.name
        contenido = texto.get("1.0",END)
        fichero = open(ruta, 'w+')
        fichero.write(contenido)
        fichero.close()
        pestana.tab("current", text=ruta)
        mensaje.set("Fichero guardado correctamente")
    else:
        mensaje.set("Guardado cancelado")
        ruta = ""

def acercade():
    #Mensaje en barra de estado
    mensaje.set("Acerca de... Editor de Texto en Python")
    # Creo el widget
    acercade1 = tk.Toplevel(root, background='#FFFFFF')
    acercade1.resizable(False, False)
    # titulo de la ventana
    acercade1.title("Acerca de...")

    # Dimension de ventana
    w = 300
    h = 250
    # ventana centralizada
    ws = acercade1.winfo_screenwidth()
    hs = acercade1.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    acercade1.geometry('%dx%d+%d+%d' % (w, h, x, y))
    #
    # Label acerca de...
    label = tk.Label(acercade1, text="Editor de texto en Python", height=3, background='#FFFFFF')
    label.pack()
    label1 = tk.Label(acercade1, text="Editor de texto, realizado en python\n con tkinter ", height=8, background='#FFFFFF')
    label1.pack()
    # Boton salir
    button1 = tk.Button(acercade1, text="Salir", width=26, height=20, command=lambda:[acercade1.destroy(), mensaje.set("Editor de Texto en Python")])
    button1.pack(padx=10, pady=10)

    # Display untill closed manually
    acercade1.mainloop()


if __name__ == '__main__':
    root = tk.Tk()
    root.title("Editor de Texto")
    w = 700
    h = 600
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    pestana= CustomNotebook(width=200, height=200)

    menubarra = Menu(root, background='#FFFFFF')
    # Crea un menu desplegable y lo agrega al menu barra
    menuarchivo = Menu(menubarra, tearoff=0, background='#FFFFFF')
    menuarchivo.add_command(label="Nuevo", command=nuevo)
    menuarchivo.add_command(label="Abrir", command=abrir)
    menuarchivo.add_command(label="Guardar", command= lambda:guardar(frames[pestana.index("current")])  )
    menuarchivo.add_command(label="Guardar Como", command=lambda: guardar_como(frames[pestana.index("current")]))
    menuarchivo.add_command(label="Analisis Lexico", command=lambda :anilisis_lexico(frames[pestana.index("current")]))
    menuarchivo.add_command(label="Analisis Sintactico", command=analisis_sintactico)
    menuarchivo.add_separator()
    menuarchivo.add_command(label="Salir", command=root.quit)
    menubarra.add_cascade(label="Archivo", menu=menuarchivo)

    # Crea dos menus desplegables mas
    menueditar = Menu(menubarra, tearoff=0, background='#FFFFFF')
    menueditar.add_command(label="Cortar", accelerator="Ctrl+X", command=lambda: cut(frames[pestana.index("current")]))  # , command=hola)
    menueditar.add_command(label="Copiar", accelerator="Ctrl+C", command=lambda :copy(frames[pestana.index("current")]))  # , command=hola)
    menueditar.add_command(label="Pegar", accelerator="Ctrl+V", command=lambda :paste(frames[pestana.index("current")]))  # , command=hola)
    menueditar.add_command(label="Atras", accelerator="Ctrl+Z", command=lambda :undo(frames[pestana.index("current")]))
    menueditar.add_command(label="Adelante", accelerator="Ctrl+Y", command=lambda :redo(frames[pestana.index("current")]))
    menueditar.add_command(label="Seleccionar todo", accelerator="Ctrl+A", command=lambda :select_all(frames[pestana.index("current")]))
    menubarra.add_cascade(label="Editar", menu=menueditar)
    formatmenu = Menu(menubarra, tearoff=0,  background='#FFFFFF')
    formatmenu.add_command(label="Cambiar Fondo", command=lambda : changeBg(frames[pestana.index("current")]))
    formatmenu.add_command(label="Color de Fuente", command=lambda :changeFg(frames[pestana.index("current")]))
    menueditar.add_separator()
    menueditar.add_cascade(label="Formato", menu=formatmenu)
    menuayuda = Menu(menubarra, tearoff=0,  background='#FFFFFF')
    menuayuda.add_command(label="Acerca de...", command=acercade)
    menubarra.add_cascade(label="Ayuda", menu=menuayuda)
    texto = tk.Text(root)
    mensaje = tk.StringVar()
    

    
    

    nuevo()
    print(frames)

    mensaje.set("Editor de texto en python")
    monitor = tk.Label(root, textvar=mensaje, justify='left')
    monitor.pack(anchor="center")
    root.config(menu=menubarra)
    root.mainloop()
    