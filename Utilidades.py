

import json
import os
import webbrowser
import tkinter as tk


########## Funciones generales


##############Funciones para archivos

# Recibe la ventana actual (para cerrarla) y recibe la función (cómo objeto) que abre la ventana a la que se quiere ir
def abrir_ventana(ventana,funcion):
    ventana.destroy() 
    funcion() 

def obtener_ruta():
    return os.path.split(__file__)[0]


# devuelve un diccionario con toda la información del json de la configuración
# recibe el nombre del archivo json (sin la extensión)
def buscar_archivo(nombre):
    ruta = obtener_ruta()
    f = open(ruta+"/Archivos/"+nombre+".json", "r")
    archivo = f.read()
    f.close()
    return json.loads(archivo)

def guardar_archivo(nombre, datos):
    # Guardar
        ruta = obtener_ruta()
        f = open(ruta+"/Archivos/"+nombre+".json", "w")
        f.write(json.dumps(datos))
        f.close()






# Recibe un string y mide su tamaño 
# Ademas recibe el tamaño minimo y maximo
def validar_tam_string(string, min, max):
    return len(string) >= min and len(string) <= max

# Recibe un int y mide su tamaño 
# Ademas recibe el tamaño minimo y maximo
def validar_tam_int(num, min, max):
    return num > (10**(min-1))+1 and num <  (10**(max))

# Valida que sea un entero positivo 
# Se espera recibir un numero entero y positivo
def validar_int_positivo(num):
    try:
        num= int(num)
    except: 
        return False
    if (num < 1):
        return False        
    return True



# Abre el manual de usuario 
# Recibe el nombre del módulo para saber cual manual abrir
def ayuda(nombre):
    
    ruta = os.path.split(__file__)[0]
    ruta += "\Manuales\pc_manual_de_usuario_"+nombre+".pdf"
    webbrowser.open(ruta)



# Funcion que devuelve un Label con una imagen vacía de 10px
# Recibe el frame/ventana en el que se desplegará
def espacio(frame):
    ruta_img = obtener_ruta()+"/Recursos/void.png"
    img = tk.PhotoImage(file=ruta_img)
    return tk.Label(frame,image=img)



#Constantes
col_texto = "#090909"
col_celda = "#f0f0f0"
col_celda_selec = "#c7ccf0"
col_celda_desact ="#677083"
col_borde= "#3E3E3E"

