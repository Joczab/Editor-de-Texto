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
global right_click_text_menu, ruta
import re
import ply.lex as lex
from ply import yacc

# Lista de palabras clave de Python
palabras_clave = ['import', 'def', 'from', 'global', 'if', 'else','elif','match','while','int','for']

# Patrones para números e identificadores
patron_numero = r'^\d+(\.\d+)?$'
patron_identificador = r'^\w+$'

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
    for tok in lexer:
        print(tok)

def analisis_sintactico():
    global ruta
    mensaje.set('Abrir fichero')
    ruta = FileDialog.askopenfilename(initialdir='.', filetypes=(("Archivos de Texto", "*.txt"), 
                                                                 ("Archivos .py", "*.py"), 
                                                                 ("Todos los Archivos", "*.*")), 
                                      title="Abrir un fichero.")
    with open(ruta, 'r', encoding='utf-8') as archivo:
        texto_prueba = archivo.read()
    print(analizar_texto(texto_prueba))

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
        elif re.match(patron_identificador, token):
            clasificacion_tokens['IDENTIFICADOR'].append(token)
        else:
            clasificacion_tokens['SIMBOLO'].append(token)
    
    # Retornar el diccionario con los tokens clasificados
    return mostrar_resultados_ordenados(clasificacion_tokens)

# Para mostrar los resultados de manera ordenada
def mostrar_resultados_ordenados(clasificacion_tokens):
    for categoria in sorted(clasificacion_tokens):
        print(f"{categoria}:")
        for token in sorted(clasificacion_tokens[categoria]):
            print(f" - {token}")

'''def analizar_lexico(texto):
    tokens_clasificados = []
    # Dividir el texto en tokens
    tokens = re.findall(r'\w+|[^\w\s]', texto, re.UNICODE)
    
    for token in tokens:
        if token in palabras_clave:
            tokens_clasificados.append((token, 'PALABRA CLAVE'))
        elif re.match(patron_numero, token):
            tokens_clasificados.append((token, 'NUMERO'))
        elif re.match(patron_identificador, token):
            tokens_clasificados.append((token, 'IDENTIFICADOR'))
        else:
            tokens_clasificados.append((token, 'SIMBOLO'))
    
    # Ordenar los tokens clasificados por su clasificación
    tokens_clasificados.sort(key=lambda x: x[1])
    
    return tokens_clasificados'''

def copy():
    texto.event_generate('<<Copy>>')


def cut():
    texto.event_generate('<<Cut>>')


def paste():
    texto.event_generate('<<Paste>>')


def undo():
    texto.event_generate('<<Undo>>')


def redo():
    texto.event_generate('<<Redo>>')


def select_all(event=None):
    texto.tag_add('sel', '1.0', 'end')
    return "break"


def changeBg():
    (tripple, hexstr) = askcolor()
    if hexstr:
        texto.config(background=hexstr)


def changeFg():
    (triple, hexstr) = askcolor()
    if hexstr:
        texto.config(fg=hexstr)


def bold():
    F_font = ('bold', 30)
    text.font = F_font


def right_click_menu(event):
    # mostra il menù partendo dalla posizione definita con .post()
    right_click_text_menu.post(event.x_root, event.y_root)


def right_click_menu_destroy(widget):
    
    # semplicemente toglie il menù apparentemente senza perdite di memoria
    right_click_text_menu.unpost()


def nuevo():
    global ruta
    mensaje.set("Nuevo fichero")
    ruta = ""
    texto.delete(1.0, "end")
    root.title("Editor de Texto en python")


def anilisis_lexico():
    
    global ruta
    mensaje.set('Abrir fichero')
    ruta = FileDialog.askopenfilename(initialdir='.', filetypes=(("Archivos de Texto", "*.txt"), 
                                                                 ("Archivos .py", "*.py"), 
                                                                 ("Todos los Archivos", "*.*")), 
                                      title="Abrir un fichero.")
    
    with open(ruta, 'r', encoding='utf-8') as archivo:
        texto_prueba = archivo.read()
    print(analizar_lexico(texto_prueba))
    
   
    
def abrir():
    # Indicamos que la ruta es respecto a la variable global
    # Debemos de forzar esta lectura global porque los comandos
    # sólo son conscientes de las variables externas que son widgets
    global ruta

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
        fichero = open(ruta, 'r')
        contenido = fichero.read()
        texto.delete(1.0, 'end')  # Nos aseguramos de que esté vacío
        texto.insert('insert', contenido)  # Le insertamos el contenido
        fichero.close()  # Cerramos el fichero
        root.title(nombre_archivo + " -- Editor de texto en Python")  # Cambiamos el título
        mensaje.set('Editor de Texto en python')

def guardar():
    global ruta
    mensaje.set("Guardar fichero")
    if ruta == "":
        guardar_como()
    else:
        contenido = texto.get(1.0, 'end-1c')
        fichero = open(ruta, 'w+')
        fichero.write(contenido)
        fichero.close()
        mensaje.set("Fichero guardado correctamente")

def guardar_como():
    global ruta
    mensaje.set("Guardar fichero como")

    fichero = FileDialog.asksaveasfile(title="Guardar fichero", mode="w", defaultextension="txt", 
                                       filetypes=[("Archivos de Texto", "*.txt"),
                                                  ("Archivos .py", "*.py"), 
                                                  ("Todos los Archivos", "*.*")])

    if fichero is not None:
        ruta = fichero.name
        contenido = texto.get(1.0, 'end-1c')
        fichero = open(ruta, 'w+')
        fichero.write(contenido)
        fichero.close()
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
    ruta = ""
    root = tk.Tk()
    root.title("Editor de Texto")
    w = 700
    h = 600
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    menubarra = Menu(root, background='#FFFFFF')
    # Crea un menu desplegable y lo agrega al menu barra
    menuarchivo = Menu(menubarra, tearoff=0, background='#FFFFFF')
    menuarchivo.add_command(label="Abrir", command=abrir)
    menuarchivo.add_command(label="Guardar", command=guardar)
    menuarchivo.add_command(label="Guardar Como", command=guardar_como)
    menuarchivo.add_command(label="Analisis Lexico", command=anilisis_lexico)
    menuarchivo.add_command(label="Analisis Sintactico", command=analisis_sintactico)
    menuarchivo.add_separator()
    menuarchivo.add_command(label="Salir", command=root.quit)
    menubarra.add_cascade(label="Archivo", menu=menuarchivo)

    # Crea dos menus desplegables mas
    menueditar = Menu(menubarra, tearoff=0, background='#FFFFFF')
    menueditar.add_command(label="Cortar", accelerator="Ctrl+X", command=cut)  # , command=hola)
    menueditar.add_command(label="Copiar", accelerator="Ctrl+C", command=copy)  # , command=hola)
    menueditar.add_command(label="Pegar", accelerator="Ctrl+V", command=paste)  # , command=hola)
    menueditar.add_command(label="Atras", accelerator="Ctrl+U", command=undo)
    menueditar.add_command(label="Adelante", accelerator="Ctrl+Y", command=redo)
    menueditar.add_command(label="Seleccionar todo", accelerator="Ctrl+A", command=select_all)
    menubarra.add_cascade(label="Editar", menu=menueditar)
    formatmenu = Menu(menubarra, tearoff=0,  background='#FFFFFF')
    formatmenu.add_command(label="Cambiar Fondo", command=changeBg)
    formatmenu.add_command(label="Color de Fuente", command=changeFg)
    menueditar.add_separator()
    menueditar.add_cascade(label="Formato", menu=formatmenu)
    menuayuda = Menu(menubarra, tearoff=0,  background='#FFFFFF')
    menuayuda.add_command(label="Acerca de...", command=acercade)
    menubarra.add_cascade(label="Ayuda", menu=menuayuda)
    text = tk.Text(root)

    right_click_text_menu = Menu(text, tearoff=0,  background='#FFFFFF')
    right_click_text_menu.add_command(label=' Cortar ', command=lambda: texto.event_generate('<<Cut>>'))
    right_click_text_menu.add_command(label=' Copiar ', command=lambda: texto.event_generate('<<Copy>>'))
    right_click_text_menu.add_command(label=' Pegar ', command=lambda: texto.event_generate('<<Paste>>'))
    right_click_text_menu.add_command(label=' Seleccionar Todo ', command=select_all)

    S = tk.Scrollbar(root)
    texto = tk.Text(root)
    S.config(command=texto.yview)
    S.pack(side=tk.RIGHT, fill=Y)
    texto.config(font=("Verdana", 12), bd=0, padx=1, pady=1, yscrollcommand=S.set, undo=1)
    texto.pack(expand=True, fill="both")
    texto.bind('<Button-3>', right_click_menu)
    texto.bind('<Button-1>', lambda event: right_click_menu_destroy(right_click_text_menu))
    mensaje = tk.StringVar()
    mensaje.set("Editor de texto en python")
    monitor = tk.Label(root, textvar=mensaje, justify='left')
    monitor.pack(side="left")
    root.config(menu=menubarra)
    root.mainloop()
    