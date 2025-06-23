import Utilidades as uti
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk 


def ventana_jugar():
    
    def generar_columna(tree):
        datos = []
        for i in range(0,9):
            datos.append( (i, i+i) )
        print(datos)
        for row in datos:
            tree.insert('', tk.END, values=row)
            #tree.bind('<Double 1>', activar_edicion)


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
        # Busca el archivo de partidas y lo obtiene
        partidas = uti.buscar_archivo("kakuro2025_partidas")
        # Toma la partida seleccionada
        partida = partidas[0]

        tam = tam_casilla
        # Recorre las claves para ir colocandolas
        for clave in partida["claves"]:
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
                btn_act[4].append( (clave["tipo_de_clave"],nuevo_i,nuevo_j) )
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

    # Funcion que coloca un numero en la casilla
    # Recibe el número a colocar y el id de la casilla que se quiere marcar
    def marcar_casilla(num,id):
        if id == "":
            return None
        tablero[id][0].config(text=num)
        tablero[id][2] = num
        if num == "":
            tablero[id][2] = "0"

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


            

    celda_actual = [""]
    tam_casilla = 50
    tam_borde = 2
    tam_juego = (tam_casilla + tam_borde) * 9 + tam_borde
    ventana = tk.Tk()
    ventana.geometry(str(tam_juego + 10)+"x"+str(tam_juego + 10))

    frame_juego = tk.Frame(ventana,bg=uti.col_borde)
    frame_juego.place(x=20, y=20, width=tam_juego, height=tam_juego)

    frame_numeros = tk.Frame(ventana,bg="#090909")
    frame_numeros.place(x=20, y=20 + tam_juego+ tam_casilla, width=tam_juego, height=tam_casilla * 2 + tam_borde * 3)

    frame_usuario = tk.Frame(ventana,bg="#090909")
    frame_usuario.place(x=20 + tam_juego + tam_casilla, y=20, width=tam_juego, height=tam_casilla)

    tablero={}

    
    generar_tabla(frame_juego)
    generar_interfaz()
    print(tablero)


    ventana.mainloop() 

def ventana_principal():
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
        command= lambda: uti.abrir_ventana(ventana,lambda: ventana_jugar())
    )
    btn_jugar.grid(row=0,column=0,columnspan=2, padx=5,pady=5)
    
    btn_configurar = tk.Button(
        frame_opc_derecha,
        text="Configurar",
        font=("Arial",12),
        bg="#f0f0f0",
        fg="#090909",
        command= lambda: uti.abrir_ventana(ventana,lambda: ventana_jugar())
    )
    btn_configurar.grid(row=1,column=0,columnspan=2, padx=5,pady=5)
    
    btn_ayuda = tk.Button(
        frame_opc_abajo,
        text="Ayuda",
        font=("Arial",12),
        bg="#f0f0f0",
        fg="#090909",
        command= lambda: uti.abrir_ventana(ventana,lambda: ventana_jugar())
    )
    btn_ayuda.grid(row=0,column=0,columnspan=1, padx=5,pady=5)

    btn_acerca_de = tk.Button(
        frame_opc_abajo,
        text="Acerca De",
        font=("Arial",12),
        bg="#f0f0f0",
        fg="#090909",
        command= lambda: uti.abrir_ventana(ventana,lambda: ventana_jugar())
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

ventana_principal()