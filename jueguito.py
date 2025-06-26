import Utilidades as uti
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk 
import collections 
import time
import threading as th

# Busca una partida en el archivo de partidas
# Recibe la dificultad y el numero
# Devuelve el diccionario correspondiente a la partida
def buscar_partida(dif,num):
    partidas = uti.buscar_archivo("kakuro2025_partidas")
    for partida in partidas:
        if partida["nivel_de_dificultad"] == dif and partida["partida"] == num:
            return partida

def ventana_jugar(nombre):
    # Funcion para hacer el contador de tiempo
    def temporizador(tiempo_partida):
        time.sleep(1)
        tiempo_partida[0] += contar_al_tiempo
        tiempo_partida[1].config(text=time.strftime("%H:%M:%S",time.gmtime(tiempo_partida[0])))
        if estado_partida:
            temporizador(tiempo_partida)

    def seleccionar_casilla(id,celda_actual):
        #deseleccionar la actual
        celda_actual [0] 
        if celda_actual[0] != "":
            tablero[celda_actual[0]][0].config(bg=uti.col_celda)               
        tablero[id][0].config(bg= uti.col_celda_selec)
        celda_actual[0] = id
    
    def cargar_partida():
        pass

    # Carga las claves de la partida seleccionada
    # Recibe el frame qe contiene la cuadrícula del juego
    def cargar_claves(frame):
        tam = tam_casilla
        # Recorre las claves para ir colocandolas
        for clave in partida_actual["claves"]:
            # Obtiene la posición de la fila y columna de la clave
            i = clave["fila"] - 1
            j = clave["columna"] - 1
            # Calcula la posición en pixeles respecto al inicio del frame
            pos_x = ((tam + 2) * j + 2) 
            pos_y = ((tam + 2) * i + 2)
            #Crea la linea (solo si aun no ha sido marcado como clave)
            if not tablero[(str(i)+str(j))][3]:
                linea = tk.Canvas(frame,bg=uti.col_celda_desact,)
                linea.create_line(0,0,tam,tam,width=2,fill=uti.col_celda,)
                linea.place(x=pos_x,y=pos_y,height=tam,width=tam)
                tablero[(str(i)+str(j))][3] = True
            # Ajusta el funcionamiento dependiendo de si es fila o columna
            inc_i = 0
            inc_j = 0
            if clave["tipo_de_clave"] == "C":
                pos_x += tam // 6
                pos_y += ((2 * tam) // 3) - 1
                inc_i = 1
            else: 
                pos_x += ((2 * tam) // 3) - 1
                pos_y += tam // 6
                inc_j = 1
            # Agrega el label de la clave
            lbl_clave = tk.Label(frame,text=str(clave["clave"]),bg=uti.col_celda_desact,fg=uti.col_celda)
            lbl_clave.place(x=pos_x,y=pos_y,height=tam//3,width=tam//3)
            # Activa las casillas de la clave
            for k in range(1,clave["casillas"]+1):
                nuevo_i = i + (k * inc_i)
                nuevo_j = j + (k * inc_j)
                btn_act = tablero[(str(nuevo_i)+str(nuevo_j))]
                btn_act[4].append( (clave["tipo_de_clave"],i+1,j+1) )
                btn_act[0].bind('<Button 1>', lambda event, x=nuevo_i,y=nuevo_j: seleccionar_casilla( (str(x)+str(y)),celda_actual ))
                btn_act[0].config(bg=uti.col_celda, state="normal")
        

    def generar_tabla(frame):
        for i in range(0,9):
            for j in range(0,9):
                tam = tam_casilla
                pos_x = (tam + 2) * j + 2
                pos_y = (tam + 2) * i + 2
                btn_act = tk.Button(
                    frame,
                    text="",
                    font=("Arial",12),
                    bg=uti.col_celda,
                    fg= uti.col_texto,
                    relief="flat",
                    command= ""
                )
                btn_act.config(bg=uti.col_celda_desact,state="disabled")
                

                btn_act.place(x=pos_x,y=pos_y,width=tam,height=tam)
                # tablero[00] = [[0]objeto_del_boton, [1]id, [2]valor_actual, 
                # [3]es_clave?(Si/No), [4]lista de las casillas de las a las que pertenece (las guarda como duplas) ("C",0,3)]
                tablero[(str(i)+str(j))] = [btn_act, str(i)+str(j), 0, False, []]
        cargar_claves(frame)

    # Valida la última jugada
    # Recibe el identificador de la casilla que se modificó
    # Devuelve un booleano que indica si es válida, y un mensaje de error en caso de que no
    def validar_jugada(id):
        for claves_celda in tablero[id][4]:
            for claves in partida_actual["claves"]:
                if claves["tipo_de_clave"] == claves_celda[0] and claves["fila"] == claves_celda[1] and claves["columna"] == claves_celda[2]:
                    i = claves["fila"] - 1
                    j = claves["columna"] - 1
                    inc_i = 0
                    inc_j = 0
                    total = 0
                    mensaje = ""
                    if claves["tipo_de_clave"] == "C":
                        inc_i = 1
                        mensaje = "columna"
                    else: 
                        inc_j = 1
                        mensaje = "fila"
                    nums_usados = []
                    for k in range(1,claves["casillas"]+1):
                        nuevo_i = i + (k * inc_i)
                        nuevo_j = j + (k * inc_j)
                        nuevo_num = int( tablero[(str(nuevo_i)+str(nuevo_j))][2] )
                        if nuevo_num in nums_usados and nuevo_num != 0:
                            return False, "Ya se ha usado el valor "+ str(nuevo_num) +" en la " + mensaje
                        nums_usados.append(nuevo_num)
                        total += nuevo_num
                    if total > claves["clave"]:
                        mensaje = "Se ha excedido el valor de la clave " + str(claves["clave"]) + "en la " + mensaje + ". La suma da " + str(total)
                        return False, mensaje
        return True, "Super bien todo"


                    
                    
                    
        

    # Funcion que coloca un numero en la casilla
    # Recibe el número a colocar y el id de la casilla que se quiere marcar
    def marcar_casilla(num,id):
        # Si no hay casilla seleccionada se sale del proceso
        if id == "":
            return None
        # Guarda el movimiento en la pila
        pila_movimientos.append((id,tablero[id][2],num))
        # Cambia el valor actual de la casilla por el nuevo
        tablero[id][0].config(text=num)
        tablero[id][2] = num
        # Si la opción era limpiar, marca con cero
        if num == "":
            tablero[id][2] = "0"
        # Valida la jugada y si no es posible, envia un mensaje de alerta
        es_valida, mensaje = validar_jugada(id)
        if not es_valida:
            print(mensaje)

    def iniciar_juego():
        pass

    def deshacer_jugada():
        pass

    def rehacer_jugada():
        pass

    def borrar_juego():
        pass

    def guardar_juego():
        pass

    def terminar_juego():
        pass

    def cargar_juego():
        pass

    def records():
        pass

    # Esta funcion genera la interfaz que tiene que ver con el usuario
    def generar_interfaz_usuario():
        label_nombre = tk.Label(frame_usuario,text=nombre,bg=uti.col_celda_desact,fg=uti.col_celda,font=("Arial",14))
        label_nombre.place(x=tam_borde,y=tam_borde,width=(tam_juego/2)-tam_borde,height=tam_casilla-(tam_borde*2))
        
        label_tiempo = tk.Label(frame_usuario,text=time.strftime("%H:%M:%S",time.gmtime(tiempo_partida[0])),
                                bg=uti.col_celda_desact,fg=uti.col_celda,font=("Arial",16))
        label_tiempo.place(x=tam_borde+(tam_juego/2),y=tam_borde,width=(tam_juego/2)-tam_borde*2,height=tam_casilla-(tam_borde*2))
        tiempo_partida.append(label_tiempo)
        pass

    #nombre

    # Esta función genera la interfaz
    def generar_interfaz():
        tam = tam_casilla
        pos_y = 2

        # Genera los numeros para marcar en las casillas
        for i in range(0,9):
            pos_x = (tam + 2) * i + 2
            btn_act = tk.Button(
                    frame_numeros,
                    text= str(i+1),
                    font=("Arial",12),
                    bg=uti.col_celda,
                    fg= uti.col_texto,
                    relief="flat",
                    command= lambda num=i+1: marcar_casilla(num, celda_actual[0])
            )
            btn_act.place(x=pos_x,y=pos_y, width=tam, height=tam)
        # Botón para Limpiar las casillas
        btn_limpiar = tk.Button(
                frame_numeros,
                text= "Limpiar",
                font=("Arial",12),
                bg=uti.col_celda,
                fg= uti.col_texto,
                relief="flat",
                command= lambda: marcar_casilla("", celda_actual[0])
        )
        btn_limpiar.place(x=2, y=pos_y + tam_casilla + tam_borde, width=tam_juego - 4, height=tam)
        generar_interfaz_usuario()

    # Guarda duplas (idcasilla,num anterior, nuevo num)
    pila_movimientos = collections.deque()
    es_temporizador = False

    contar_al_tiempo = 1
    if es_temporizador:
        contar_al_tiempo = -1

    estado_partida = True
    tiempo_partida = [0]
    partida_actual = buscar_partida("FACIL",1)
    celda_actual = [""]
    tam_casilla = 50
    tam_borde = 2
    tam_juego = (tam_casilla + tam_borde) * 9 + tam_borde
    ventana = tk.Tk()
    ventana.geometry(str((tam_juego * 2) + 40 + tam_casilla)+"x"+str(tam_juego + (tam_casilla * 3) + 40))

    frame_juego = tk.Frame(ventana,bg=uti.col_borde)
    frame_juego.place(x=20, y=20, width=tam_juego, height=tam_juego)

    frame_numeros = tk.Frame(ventana,bg=uti.col_borde)
    frame_numeros.place(x=20, y=20 + tam_juego+ tam_casilla, width=tam_juego, height=tam_casilla * 2 + tam_borde * 3)

    frame_usuario = tk.Frame(ventana,bg=uti.col_borde)
    frame_usuario.place(x=20 + tam_juego + tam_casilla, y=20, width=tam_juego, height=tam_casilla)

    tablero={}

    
    generar_tabla(frame_juego)
    generar_interfaz()
    print(tablero)

    t1 = th.Thread(target=lambda:temporizador(tiempo_partida))
    t1.start()
    ventana.mainloop() 

def ventana_principal(nombre):
    # La ventana
    ventana = tk.Tk()
    ventana.title("Kakuro")

    # Frames para ordenar la ventana
    frame_logo = tk.Frame(ventana)
    frame_logo.grid(row=0, column=0, columnspan=2, padx= 5, pady= 5)
    frame_opc_derecha = tk.Frame(ventana)
    frame_opc_derecha.grid(row=0, column=2, columnspan=2, padx= 5, pady= 5)
    frame_opc_abajo = tk.Frame(ventana)
    frame_opc_abajo.grid(row=1, column=0, columnspan=4, padx= 5, pady= 5)
    espacio = uti.espacio(ventana)
    espacio.grid(row=0, column=4, columnspan=1, padx= 5, pady= 5)


    ruta_img = uti.obtener_ruta()+"/Recursos/logo.png"
    img = tk.PhotoImage(file=ruta_img)
    label_img =tk.Label(frame_logo,image=img)
    label_img.grid(row=0,column=0,columnspan=1, padx=5,pady=5)

    btn_jugar = tk.Button(
        frame_opc_derecha,
        text="Jugar",
        font=("Arial",18),
        bg="#f0f0f0",
        fg="#090909",
        command= lambda: uti.abrir_ventana(ventana,lambda: ventana_jugar(nombre))
    )
    btn_jugar.grid(row=0,column=0,columnspan=2, padx=5,pady=5)
    
    btn_configurar = tk.Button(
        frame_opc_derecha,
        text="Configurar",
        font=("Arial",12),
        bg="#f0f0f0",
        fg="#090909",
        command= lambda: uti.abrir_ventana(ventana,lambda: ventana_jugar(nombre))
    )
    btn_configurar.grid(row=1,column=0,columnspan=2, padx=5,pady=5)
    
    btn_ayuda = tk.Button(
        frame_opc_abajo,
        text="Ayuda",
        font=("Arial",12),
        bg="#f0f0f0",
        fg="#090909",
        command= lambda: uti.abrir_ventana(ventana,lambda: ventana_jugar(nombre))
    )
    btn_ayuda.grid(row=0,column=0,columnspan=1, padx=5,pady=5)

    btn_acerca_de = tk.Button(
        frame_opc_abajo,
        text="Acerca De",
        font=("Arial",12),
        bg="#f0f0f0",
        fg="#090909",
        command= lambda: uti.abrir_ventana(ventana,lambda: ventana_jugar(nombre))
    )
    btn_acerca_de.grid(row=0,column=1,columnspan=1, padx=5,pady=5)

    btn_salir = tk.Button(
        frame_opc_derecha,
        text="Salir",
        font=("Arial",12),
        bg="#f0f0f0",
        fg="#090909",
        command= lambda: ventana.destroy()
    )
    btn_salir.grid(row=2,column=0,columnspan=2, padx=5,pady=5)


    ventana.mainloop()

# Es la ventana inicial, pide el nombre al usuario y lo valida antes de empezar
def ventana_usuario():
    def validar_nombre():
        if nombre.get().strip() == "":
            mb.showinfo("Error", "Nombre no adecuado")
            return None

        uti.abrir_ventana(ventana,lambda: ventana_principal(nombre.get()))
        

    ventana = tk.Tk()
    frame = tk.Frame(ventana)
    frame.grid(row=0,column=0,columnspan=1, padx=5,pady=5)
    frame_opc = tk.Frame(ventana)
    frame_opc.grid(row=0,column=1,columnspan=1, padx=5,pady=5)


    ruta_img = uti.obtener_ruta()+"/Recursos/logo.png"
    img = tk.PhotoImage(file=ruta_img)
    label_img =tk.Label(frame,image=img)
    label_img.grid(row=0,column=0,rowspan=1, padx=5,pady=5)

    label = tk.Label(frame_opc,text="Ingrese su nombre de usuario:")
    label.grid(row=0,column=0,columnspan=3, padx=5,pady=5)

    nombre = tk.StringVar(ventana, value=str(""))
    entry_nombre = tk.Entry(frame_opc)
    entry_nombre.config(textvariable= nombre)
    entry_nombre.grid(row=1,column=0,columnspan=2, padx=5,pady=5)

    btn_ingresar = tk.Button(
        frame_opc,
        text="Ingresar",
        font=("Arial",14),
        bg=uti.col_celda_selec,
        fg=uti.col_borde,
        relief="flat",
        command= validar_nombre
    )
    btn_ingresar.grid(row=1,column=2,columnspan=1, padx=5,pady=5)

    btn_salir = tk.Button(
        frame_opc,
        text="Salir",
        font=("Arial",12),
        bg=uti.col_celda_desact,
        fg=uti.col_celda,
        relief="flat",
        command= lambda: ventana.destroy()
    )
    btn_salir.grid(row=2,column=0,columnspan=3, padx=5,pady=5)

    ventana.mainloop()


#ventana_principal()
ventana_usuario()