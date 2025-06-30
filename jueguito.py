import Utilidades as uti
import tkinter as tk
from tkinter import messagebox as mb
from tkinter import ttk 
import collections 
import time
import threading as th
import random

# Busca una partida en el archivo de partidas
# Recibe la dificultad y el numero
# Devuelve el diccionario correspondiente a la partida
def buscar_partida(dif,num):
    partidas = uti.buscar_archivo("kakuro2025_partidas")
    for partida in partidas:
        if partida["nivel_de_dificultad"] == dif and partida["partida"] == num:
            return partida

def guardar_record(nombre,tiempo,dificultad,num_partida):
    encontrado = False
    records = uti.buscar_archivo("kakuro2025_records")
    for record in records:
        if record["nombre"] == nombre and record["dificultad"] == dificultad and record["num_partida"] == num_partida:
            encontrado = True 
            if record["tiempo"] > tiempo:
                record["tiempo"] = tiempo
                break
    if not encontrado:
        record = {"nombre":nombre,"tiempo":tiempo,"dificultad":dificultad,"num_partida":num_partida}
        records.append(record)
    uti.guardar_archivo("kakuro2025_records",records)

def ventana_records(nombre):
    def ordenar_la_lista(lista):
        tam = len(lista)
        for i in range(tam-1):
            for j in range(1,tam):
                if lista[i][1] > lista[j][1]:
                    de_paso = lista[j]
                    lista[j] = lista[i]
                    lista[i] = de_paso

    
    def generar_datos():
        seleccion_actual.clear()
        personales.clear()
        for record in records:
            fila = (record["nombre"],record["tiempo"],record["dificultad"],record["num_partida"])
            if fila[2] != dificultad[0] and dificultad[0] != "TODOS":
                continue
            seleccion_actual.append(fila)
            if nombre == record["nombre"]:
                personales.append(fila)
        ordenar_la_lista(seleccion_actual)
        ordenar_la_lista(personales)

    def construir_tabla():
        tablas[0].destroy() 
        tablas[0] = ttk.Treeview(frame_tree_globales, columns=columnas, show='headings', selectmode=tk.BROWSE)
        tablas[1].destroy() 
        tablas[1] = ttk.Treeview(frame_personales, columns=columnas, show='headings', selectmode=tk.BROWSE)
        for tree in tablas:
            for columna in columnas:
                tree.heading(columna, text=columna)
        tablas[0].grid(row=0, column=0, padx= 5, pady= 5)
        tablas[1].grid(row=1, column=0, columnspan=5, padx= 5, pady= 5)

    def generar_tabla():
        for row in seleccion_actual:
            tablas[0].insert('', tk.END, values=row)
        for row in personales:
            tablas[1].insert('', tk.END, values=row)
        pass

    # Vuelve a la ventana que lo llamó
    def salir():
        uti.abrir_ventana(ventana,lambda: ventana_principal(nombre))

    def cambiar_dificultades(nueva_dificultad):
        btn_todos.config(bg=uti.col_borde,fg=uti.col_celda)
        btn_facil.config(bg=uti.col_borde,fg=uti.col_celda)
        btn_medio.config(bg=uti.col_borde,fg=uti.col_celda)
        btn_dificil.config(bg=uti.col_borde,fg=uti.col_celda)
        btn_experto.config(bg=uti.col_borde,fg=uti.col_celda)
        match nueva_dificultad:
            case "TODOS":
                btn_todos.config(bg=uti.col_celda_selec,fg=uti.col_borde)
            case "FACIL":
                btn_facil.config(bg=uti.col_celda_selec,fg=uti.col_borde)
            case "MEDIO":
                btn_medio.config(bg=uti.col_celda_selec,fg=uti.col_borde)
            case "DIFICIL":
                btn_dificil.config(bg=uti.col_celda_selec,fg=uti.col_borde)
            case "EXPERTO":
                btn_experto.config(bg=uti.col_celda_selec,fg=uti.col_borde)
        dificultad[0]=nueva_dificultad
        construir_tabla()
        generar_datos()
        generar_tabla()


    #records que se muestran

    ventana = tk.Tk()
    tk.Label(ventana,fg=uti.col_borde,font=("Arial",16),text="Records Globales").grid(column=0,row=0,padx=5,pady=5)
    tk.Label(ventana,fg=uti.col_borde,font=("Arial",16),text="Records Personales").grid(column=0,row=2,padx=5,pady=5)
    frame_globales = tk.Frame(ventana)
    frame_globales.grid(column=0,row=1,padx=0,pady=0)
    frame_tree_globales = tk.Frame(frame_globales,bg=uti.col_borde)
    frame_tree_globales.grid(row=1, column=0, columnspan=5, padx= 5, pady= 5)
    frame_personales = tk.Frame(ventana,bg=uti.col_borde)
    frame_personales.grid(column=0,row=3,padx=5,pady=5)

    btn_todos = tk.Button(frame_globales,text="Todos",font=("Arial",12),bg=uti.col_celda_selec,fg=uti.col_borde)
    btn_todos.config(relief="flat",command=lambda: cambiar_dificultades("TODOS") )
    btn_todos.grid(column=0,row=0,padx=5,pady=5)
    
    btn_facil = tk.Button(frame_globales,text="Fácil",font=("Arial",12),bg=uti.col_borde,fg=uti.col_celda)
    btn_facil.config(relief="flat",command=lambda: cambiar_dificultades("FACIL") )
    btn_facil.grid(column=1,row=0,padx=5,pady=5)
    
    btn_medio = tk.Button(frame_globales,text="Medio",font=("Arial",12),bg=uti.col_borde,fg=uti.col_celda)
    btn_medio.config(relief="flat",command=lambda: cambiar_dificultades("MEDIO") )
    btn_medio.grid(column=2,row=0,padx=5,pady=5)
    
    btn_dificil = tk.Button(frame_globales,text="Difícil",font=("Arial",12),bg=uti.col_borde,fg=uti.col_celda)
    btn_dificil.config(relief="flat",command=lambda: cambiar_dificultades("DIFICIL") )
    btn_dificil.grid(column=3,row=0,padx=5,pady=5)
    
    btn_experto = tk.Button(frame_globales,text="Experto",font=("Arial",12),bg=uti.col_borde,fg=uti.col_celda)
    btn_experto.config(relief="flat",command=lambda: cambiar_dificultades("EXPERTO") )
    btn_experto.grid(column=4,row=0,padx=5,pady=5)

    btn_volver = tk.Button(ventana,text="Volver",font=("Arial",12),bg=uti.col_borde,fg=uti.col_celda)
    btn_volver.config(relief="flat",command=lambda: salir() )
    btn_volver.grid(column=0,row=4,padx=5,pady=5)

    records = uti.buscar_archivo("kakuro2025_records")
    seleccion_actual = []
    personales = []
    dificultad = ["TODOS"]
    
    columnas = ('Nombre','Tiempo','Dificultad','Número de la partida')
    tree_globales = ttk.Treeview(frame_tree_globales, columns=columnas, show='headings', selectmode=tk.BROWSE)
    tree_personales = ttk.Treeview(frame_personales, columns=columnas, show='headings', selectmode=tk.BROWSE)
    tablas = [tree_globales,tree_personales]
    construir_tabla
    generar_datos()
    generar_tabla()
    tree_globales.grid(row=0, column=0, padx= 5, pady= 5)

    tree_personales.grid(row=1, column=0, columnspan=5, padx= 5, pady= 5)



    ventana.mainloop() 

def ventana_jugar(nombre,se_debe_cargar):
    #Esta función pregunta al usuario si desea continuar después de que se agote el temporizador
    def tiempo_agotado():
        estado_partida[0] = False
        respuesta = mb.askquestion("Tiempo agotado","¿Desea continuar la partida?")
        if respuesta == 'yes':
            contar_al_tiempo[0] = 1
            tiempo_partida[2] = tiempo_partida[0]
            estado_partida[0] = True
            tiempo_partida[1].config(text=time.strftime("%H:%M:%S",time.gmtime(tiempo_partida[2])))
        else:
            uti.abrir_ventana(ventana,lambda: ventana_principal(nombre))
    # Funcion para hacer el contador de tiempo
    def temporizador(tiempo_partida):
        time.sleep(1)
        tiempo_partida[0] += 1
        tiempo_partida[2] += contar_al_tiempo[0]
        if configuracion["reloj"] != "NORELOJ":
            tiempo_partida[1].config(text=time.strftime("%H:%M:%S",time.gmtime(tiempo_partida[2])))
        if tiempo_partida[2] == 0:
            tiempo_agotado()
        if estado_partida[0]:
            temporizador(tiempo_partida)
    
    # Esta función comienza el

    # Funcion para seleccionar partida segund dificultad de la configuración
    def seleccionar_partida():
        partidas = uti.buscar_archivo("kakuro2025_partidas")
        partidas_posibles = []
        for partida in partidas:
            if partida["nivel_de_dificultad"] == configuracion["nivel"]:
                partidas_posibles.append(partida)
        num_partida = random.randint(1,len(partidas_posibles))
        for partida in partidas_posibles:
            if partida["partida"] == num_partida:
                return partida
        


    def seleccionar_casilla(id,celda_actual):
        #deseleccionar la actual
        celda_actual [0] 
        if celda_actual[0] != "":
            tablero[celda_actual[0]][0].config(bg=uti.col_celda)               
        tablero[id][0].config(bg= uti.col_celda_selec)
        celda_actual[0] = id
    
    def cargar_partida():
        for celda in partida_para_cargar["celdas_jugables"]:
            marcar_casilla(celda[1],celda[0],True)
        

    

    # Valida la última jugada
    # Recibe el identificador de la casilla que se modificó
    # Recibe la lista de claves a validar
    # Devuelve un booleano que indica si es válida, y un mensaje de error en caso de que no
    def validar_jugada(claves_para_validar, para_victoria):
        for claves_celda in claves_para_validar:
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
                        mensaje = "Se ha excedido el valor de la clave " + str(claves["clave"]) + " en la " + mensaje + ". La suma da " + str(total)
                        return False, mensaje
                    if para_victoria and total != claves["clave"]:
                        return False, "Suma no es igual a la clave"

        return True, "Super bien todo"


                    
                    
                    
    # Esta función indica si la partida fue ganada o no
    def validar_victoria():
        claves = []
        for celda in celdas_jugables:
            if celda[1] == 0:
                return False
            for clave in tablero[celda[0]][4]:
                if not clave in claves:
                    claves.append(clave)
        if validar_jugada(claves,True)[0]:
            estado_partida[0] = False
            mb.showinfo("Felicidades","Ha ganado la partida con un tiempo de: "+time.strftime("%H:%M:%S",time.gmtime(tiempo_partida[0])))
            guardar_record(nombre,tiempo_partida[0],partida_actual["nivel_de_dificultad"],partida_actual["partida"])
            uti.abrir_ventana(ventana,lambda: ventana_principal(nombre))


    # Funcion que coloca un numero en la casilla
    # Recibe el número a colocar y el id de la casilla que se quiere marcar, 
    # también un booleano que indica si es deshacer/rehacer
    def marcar_casilla(num,id,es_deshacer):
        # Si no hay casilla seleccionada se sale del proceso
        if id == "":
            return None
        # Guarda el movimiento en la pila (solo si no es un desacer/rehacer)
        if not es_deshacer:
            pila_movimientos.append((id,tablero[id][2],num))
        # Cambia el valor actual de la casilla por el nuevo
        tablero[id][0].config(text=num)
        if num == 0:
            tablero[id][0].config(text="")
        tablero[id][2] = num
        # Si la opción era limpiar, marca con cero
        if num == "":
            tablero[id][2] = "0"
        # Cambia el valor en las celdas jugables
        for celda in celdas_jugables:
            if celda[0] == id:
                celda[1] = num
                if num == "":
                    celda[1] = 0
        # Valida la jugada y si no es posible, envia un mensaje de alerta
        es_valida, mensaje = validar_jugada(tablero[id][4],False)
        if not es_valida:
            label_mensajes.config(text=mensaje)
            return None
        validar_victoria()

    def pausa():
        pass

    def deshacer_jugada():
        # (idcasilla,num anterior, nuevo num)
        # ultimo_mov = um
        if len(pila_movimientos) < 1:
            return None
        um = pila_movimientos.pop()
        marcar_casilla(um[1],um[0],True)
        pila_rehacer.append(um)
        
    def rehacer_jugada():
        # (idcasilla,num anterior, nuevo num)
        # ultimo_des = ud
        if len(pila_rehacer) < 1:
            return None
        ud = pila_rehacer.pop()
        marcar_casilla(ud[2],ud[0],True)
        pila_movimientos.append(ud)

    def borrar_juego():
        seleccion = mb.askquestion("Borrar juego","¿Está seguro de que desea borrar la partida? Perderá su progreso")
        if seleccion == 'yes':
            pila_movimientos.clear()
            pila_rehacer.clear()
            for celdas in celdas_jugables:
                marcar_casilla(0,celdas[0],True)
            label_mensajes.config(text="Aquí verá cualquier alerta")

    # Guarda los datos del juego actual a nombre de [nombre de usuario]. 
    # Esto lo hace en el archivo de partidas actuales
    def guardar_juego():
        # Validación
        seleccion = mb.askquestion("Guardar juego","¿Está seguro de que desea guardar la partida? Regresará al menú")
        if seleccion != 'yes':
            return None

        # config numpartida tiempo
        partidas = uti.buscar_archivo("kakuro2025_juego_actual")
        datos = {"configuracion": configuracion, "num_partida":partida_actual["partida"],"tiempo":tiempo_partida[0]}
        
        # casillas_jugables pilas
        undo = []
        redo = []
        while(len(pila_movimientos) > 0):
            undo.append(pila_movimientos.pop())
        while(len(pila_rehacer) > 0):
            redo.append(pila_rehacer.pop())
        datos["celdas_jugables"] = celdas_jugables
        datos["pila_movimientos"] = undo
        datos["pila_rehacer"] = redo
        partidas[nombre] = datos
        uti.guardar_archivo("kakuro2025_juego_actual",partidas)
        uti.abrir_ventana(ventana,lambda: ventana_principal(nombre))


    def terminar_juego():
        respuesta = mb.askquestion("Terminar juego","¿Desea salir de la partida?")
        if respuesta == 'yes':
            estado_partida[0] = False
            uti.abrir_ventana(ventana,lambda: ventana_principal(nombre))

    def records():
        pass

    ### FUNCIONES PARA GENERAR LA INTERFAZ ##############################################
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
                # Celda que debe ser guardada
                if not ([str(nuevo_i)+str(nuevo_j),0] in celdas_jugables or se_debe_cargar):
                    celdas_jugables.append([str(nuevo_i)+str(nuevo_j),0])
        

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

    # Esta función agrega los botones de opciones de la interfaz
    def generar_interfaz_opciones():
        tam_opc = (tam_juego-tam_borde*4)//3

        # Deshacer
        btn_deshacer = tk.Button(frame_opciones,bg=uti.col_celda,fg=uti.col_borde,font=("Arial",14),relief="flat")
        btn_deshacer.config(text="Deshacer",command=deshacer_jugada)
        btn_deshacer.place(x=tam_borde,y=tam_borde,height=tam_casilla,width=tam_opc)
 
        # Rehacer
        btn_rehacer = tk.Button(frame_opciones,bg=uti.col_celda,fg=uti.col_borde,font=("Arial",14),relief="flat")
        btn_rehacer.config(text="Rehacer",command=rehacer_jugada)
        btn_rehacer.place(x=tam_borde*2+tam_opc,y=tam_borde,height=tam_casilla,width=tam_opc)
 
        # Guardar 
        btn_guardar = tk.Button(frame_opciones,bg=uti.col_celda,fg=uti.col_borde,font=("Arial",14),relief="flat")
        btn_guardar.config(text="Guardar",command=guardar_juego)
        btn_guardar.place(x=tam_borde*3+tam_opc*2,y=tam_borde,height=tam_casilla,width=tam_opc)
 

        # Borrar 
        btn_borrar_juego = tk.Button(frame_opciones,bg=uti.col_celda,fg=uti.col_borde,font=("Arial",14),relief="flat")
        btn_borrar_juego.config(text="Borrar",command=borrar_juego)
        btn_borrar_juego.place(x=tam_borde,y=tam_borde*2+tam_casilla,height=tam_casilla,width=tam_opc)
 
        # Terminar 
        btn_terminar = tk.Button(frame_opciones,bg=uti.col_celda,fg=uti.col_borde,font=("Arial",14),relief="flat")
        btn_terminar.config(text="Terminar",command=terminar_juego)
        btn_terminar.place(x=tam_borde*2+tam_opc,y=tam_borde*2+tam_casilla,height=tam_casilla,width=tam_opc)
 
        # Records
        btn_cortis = tk.Button(frame_opciones,bg=uti.col_celda,fg=uti.col_borde,font=("Arial",14),relief="flat")
        btn_cortis.config(text="Cortis",command=pausa)
        btn_cortis.place(x=tam_borde*3+tam_opc*2,y=tam_borde*2+tam_casilla,height=tam_casilla,width=tam_opc)
        pass
    

    # Esta funcion genera la interfaz que tiene que ver con el usuario
    def generar_interfaz_usuario():
        label_nombre = tk.Label(frame_usuario,text=nombre,bg=uti.col_celda_desact,fg=uti.col_celda,font=("Arial",14))
        label_nombre.place(x=tam_borde,y=tam_borde,width=(tam_juego/2)-tam_borde,height=tam_casilla-(tam_borde*2))
        
        label_tiempo = tk.Label(frame_usuario,text=time.strftime("%H:%M:%S",time.gmtime(int(configuracion["tiempo"]))),
                                bg=uti.col_celda_desact,fg=uti.col_celda,font=("Arial",16))
        if configuracion["reloj"] == "NORELOJ":
            label_tiempo.config(text="¡Kakuro!")
        label_tiempo.place(x=tam_borde+(tam_juego/2),y=tam_borde,width=(tam_juego/2)-tam_borde*2,height=tam_casilla-(tam_borde*2))
        tiempo_partida.append(label_tiempo)

    # Esta función agrega los botones para jugar
    def generar_interfaz_botones():
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
                    command= lambda num=i+1: marcar_casilla(num, celda_actual[0],False)
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
                command= lambda: marcar_casilla("", celda_actual[0],False)
        )
        btn_limpiar.place(x=2, y=pos_y + tam_casilla + tam_borde, width=tam_juego - 4, height=tam)

    # Esta función genera la interfaz
    def generar_interfaz():
        generar_tabla(frame_juego)
        generar_interfaz_botones()
        generar_interfaz_usuario()
        generar_interfaz_opciones()
        if se_debe_cargar:
            cargar_partida()

    ########## Variables que se utilizarán ############################################################
    configuracion = uti.buscar_archivo("kakuro2025_configuracion")
    # Guarda duplas (idcasilla,num anterior, nuevo num)
    pila_movimientos = collections.deque()
    pila_rehacer = collections.deque()
    # Aquí se guardan las casillas que tienen datos
    celdas_jugables = []
    partida_actual = []
    tiempo_partida = [0]
    partida_para_cargar = {}
    # True = Corriendo | False = Pausa
    estado_partida = [True]
    celda_actual = [""]

    if se_debe_cargar:
        partida_para_cargar = uti.buscar_archivo("kakuro2025_juego_actual")[nombre]
        configuracion = partida_para_cargar["configuracion"]
        tiempo_partida[0]= partida_para_cargar["tiempo"]
        celdas_jugables = partida_para_cargar["celdas_jugables"]

        partida_actual = buscar_partida(configuracion["nivel"],int(partida_para_cargar["num_partida"]))
        # Rellena la pila de undo
        for i in range(0,len(partida_para_cargar["pila_movimientos"])):
            pila_movimientos.append(partida_para_cargar["pila_movimientos"][len(partida_para_cargar["pila_movimientos"])-1-i])
        # Rellena la pila de redo
        for i in range(0,len(partida_para_cargar["pila_rehacer"])):
            pila_rehacer.append(partida_para_cargar["pila_rehacer"][len(partida_para_cargar["pila_rehacer"])-1-i])
        
    else:
        partida_actual = seleccionar_partida()

    # Lo referente al temporizador
    num_temporizador = configuracion["tiempo"]
    es_temporizador = configuracion["reloj"] == "TEMPORIZADOR"
    contar_al_tiempo = [1]
    if es_temporizador:
        contar_al_tiempo[0] = -1

    
    # Cosas de la interfaz
    tam_casilla = 50
    tam_borde = tam_casilla // 25
    tam_juego = (tam_casilla + tam_borde) * 9 + tam_borde
    ventana = tk.Tk()
    ventana.geometry(str((tam_juego * 2) + 40 + tam_casilla)+"x"+str(tam_juego + (tam_casilla * 3) + 40))

    frame_juego = tk.Frame(ventana,bg=uti.col_borde)
    frame_juego.place(x=20, y=20, width=tam_juego, height=tam_juego)

    frame_numeros = tk.Frame(ventana,bg=uti.col_borde)
    frame_numeros.place(x=20, y=20 + tam_juego+ tam_casilla, width=tam_juego, height=tam_casilla * 2 + tam_borde * 3)

    frame_usuario = tk.Frame(ventana,bg=uti.col_borde)
    frame_usuario.place(x=20 + tam_juego + tam_casilla, y=20, width=tam_juego, height=tam_casilla+1)
    
    frame_opciones = tk.Frame(ventana,bg=uti.col_borde)
    frame_opciones.place(x=20 + tam_juego + tam_casilla, y=20 + (tam_casilla*2), width=tam_juego, height=(tam_casilla+tam_borde)*2 + tam_borde)
    
    frame_mensajes = tk.Frame(ventana,bg=uti.col_borde)
    frame_mensajes.place(x=20 + tam_juego + tam_casilla, y=20 + (tam_casilla*5)+tam_borde*2, width=tam_juego, height=tam_casilla+tam_borde*2.5 )
    label_mensajes = tk.Label(frame_mensajes,text="Aquí verá cualquier alerta",font=("Arial",12),bg=uti.col_celda_desact,fg=uti.col_celda)
    label_mensajes.place(x=tam_borde,y=tam_borde,width=tam_juego-tam_borde*2,height=tam_casilla)
    tablero={}

    # Llama a la función que genera la interfaz
    generar_interfaz()
    tiempo_partida.append(int(configuracion["tiempo"]))



    



    # Pone a funcionar el cronómetro
    thread_temporizador = th.Thread(target=lambda:temporizador(tiempo_partida))
    thread_temporizador.start()
    ventana.mainloop() 

def ventana_configuracion(nombre):
    # Valida si el tiempo puesto es correcto 
    # Retorna True si sí lo es, False si no | Retorna el tiempo en segundos (0 si es no válido)
    def validar_tiempo():
        horas = hora.get()
        minutos = minuto.get()
        segundos = segundo.get()
        try:
            horas = int(horas)
            minutos  = int(minutos)
            segundos  = int(segundos)
        except:
            return False, 0
        
        if horas > 2 or horas < 0:
            return False, 0
        if minutos > 59 or minutos < 0:
            return False, 0
        if segundos > 59 or segundos < 0:
            return False, 0
        return True, segundos + minutos*60 + horas*3600

    # Pregunta si se desea guardar la configuración (la guarda en caso de que si)
    def salir():
        guardar = mb.askquestion("Guardar configuración","¿Desea guardar la nueva configuración?")
        if guardar == 'yes':
            validez, tiempo = validar_tiempo()
            if configuracion["reloj"] == "TEMPORIZADOR" and not validez:
                mb.showerror("Error", "El formato en la hora ingresada no fue correcto")
                return None
            configuracion["tiempo"] = str(tiempo)
            if configuracion["reloj"] != "TEMPORIZADOR":
                configuracion["tiempo"] = "0"
            uti.guardar_archivo("kakuro2025_configuracion",configuracion)
        uti.abrir_ventana(ventana,lambda: ventana_principal(nombre))

    # Esta funcion carga los datos del archivo de configuraciónm
    def cargar_datos():
        cambiar_dificultad(configuracion["nivel"])
        cambiar_reloj(configuracion["reloj"])
        cambiar_tiempo(int(configuracion["tiempo"]))

    # Esta función cambia la dificultad seleccionada
    # También, recibe la nueva dificultad
    def cambiar_dificultad(dificultad):
        btn_facil.config(bg=uti.col_celda)
        btn_medio.config(bg=uti.col_celda)
        btn_dificil.config(bg=uti.col_celda)
        btn_experto.config(bg=uti.col_celda)
        match dificultad:
            case "FACIL":
                btn_facil.config(bg=uti.col_celda_selec)
            case "MEDIO":
                btn_medio.config(bg=uti.col_celda_selec)
            case "DIFICIL":
                btn_dificil.config(bg=uti.col_celda_selec)
            case "EXPERTO":
                btn_experto.config(bg=uti.col_celda_selec)
        configuracion["nivel"] = dificultad
    
    # Esta función cambia el tipo de reloj seleccionado
    # También, recibe la nueva opción seleccionada
    def cambiar_reloj(reloj):
        btn_cronometro.config(bg=uti.col_celda)
        btn_temporizador.config(bg=uti.col_celda)
        btn_no_reloj.config(bg=uti.col_celda)
        match reloj:
            case "CRONOMETRO":
                btn_cronometro.config(bg=uti.col_celda_selec)
            case "TEMPORIZADOR":
                btn_temporizador.config(bg=uti.col_celda_selec)
            case "NORELOJ":
                btn_no_reloj.config(bg=uti.col_celda_selec)
        configuracion["reloj"] = reloj
    
    # Esta función recibe el tiempo en segundos y lo coloca 
    # en los entry con su debido formato
    def cambiar_tiempo(tiempo):
        # time.strftime("%H:%M:%S",time.gmtime(tiempo))
        hora.set( time.strftime("%H",time.gmtime(tiempo)) )
        minuto.set( time.strftime("%M",time.gmtime(tiempo)) )
        segundo.set( time.strftime("%S",time.gmtime(tiempo)) )
                
    configuracion = uti.buscar_archivo("kakuro2025_configuracion")
    padding = 20
    tam_borde = 2
    tam_casilla = 50
    tam_opc = tam_casilla*(5/2)
    ventana = tk.Tk()
    ventana.title("Kakuro - Configuración")
    ventana.geometry(str(padding*2 + int(tam_opc*7) + 8 * tam_borde)+"x"+str(padding*2 + tam_casilla*7 + tam_borde*6))

    # Frames de la ventana
    frame_opciones = tk.Frame(ventana)
    frame_opciones.place(x=padding,y=padding+tam_casilla,width=tam_opc*3 + 4*tam_borde,height=tam_casilla*10 + tam_borde)

    frame_tiempo = tk.Frame(ventana,bg=uti.col_borde)
    frame_tiempo.place(x=padding + tam_opc*4 + 5*tam_borde,y=padding+tam_casilla*2 + tam_borde*3,width=tam_opc*3 + 4*tam_borde,height=tam_casilla*2 + tam_borde*3)

    frame_volver = tk.Frame(ventana,bg=uti.col_borde)
    frame_volver.place(x=padding + tam_opc*4 + 5*tam_borde,y=padding+tam_casilla*6 + tam_borde*5,width=tam_opc*3 + 4*tam_borde,height=tam_casilla + tam_borde*2)

    label_nombre = tk.Label(ventana,text="Partida de: "+nombre,font=("Arial",16))
    label_nombre.place(x=padding,y=padding,width=tam_opc*3,height=tam_casilla)

    # Para opciones de nivel de dificultad
    frame_opc_nivel_nombre= tk.Frame(frame_opciones,bg=uti.col_borde)
    frame_opc_nivel_nombre.place(x=0,y=0,width=tam_opc+tam_borde*2,height=tam_casilla)
    label_nivel = tk.Label(frame_opc_nivel_nombre,text="Nivel",font=("Arial",12),bg=uti.col_celda_desact,fg=uti.col_celda)
    label_nivel.place(x=tam_borde,y=tam_borde,width=tam_opc,height=tam_casilla-tam_borde)

    frame_opc_nivel = tk.Frame(frame_opciones,bg=uti.col_borde)
    frame_opc_nivel.place(x=0,y=tam_casilla,width=tam_opc*2 + tam_borde*3,height= tam_casilla*2 +tam_borde*3)

    
    btn_facil = tk.Button(frame_opc_nivel,text="Facil",font=("Arial",12),bg=uti.col_celda,fg=uti.col_texto)
    btn_facil.config(relief="flat",command=lambda: cambiar_dificultad("FACIL") )
    btn_facil.place(x=tam_borde,y=tam_borde,width=tam_opc,height=tam_casilla)
    
    btn_medio = tk.Button(frame_opc_nivel,text="Medio",font=("Arial",12),bg=uti.col_celda,fg=uti.col_texto)
    btn_medio.config(relief="flat",command=lambda: cambiar_dificultad("MEDIO") )
    btn_medio.place(x=tam_borde*2 + tam_opc,y=tam_borde,width=tam_opc,height=tam_casilla)
    
    btn_dificil = tk.Button(frame_opc_nivel,text="Difícil",font=("Arial",12),bg=uti.col_celda,fg=uti.col_texto)
    btn_dificil.config(relief="flat",command=lambda: cambiar_dificultad("DIFICIL") )
    btn_dificil.place(x=tam_borde,y=tam_borde*2 + tam_casilla,width=tam_opc,height=tam_casilla)
    
    btn_experto = tk.Button(frame_opc_nivel,text="Experto",font=("Arial",12),bg=uti.col_celda,fg=uti.col_texto)
    btn_experto.config(relief="flat",command=lambda: cambiar_dificultad("EXPERTO") )
    btn_experto.place(x=tam_borde*2 + tam_opc,y=tam_borde*2 + tam_casilla,width=tam_opc,height=tam_casilla)


    # Para opciones de Reloj
    frame_opc_reloj_nombre= tk.Frame(frame_opciones,bg=uti.col_borde)
    frame_opc_reloj_nombre.place(x=0,y=tam_borde*5 + tam_casilla*4,width=tam_opc+tam_borde*2,height=tam_casilla)
    label_nivel = tk.Label(frame_opc_reloj_nombre,text="Reloj",font=("Arial",12),bg=uti.col_celda_desact,fg=uti.col_celda)
    label_nivel.place(x=tam_borde,y=tam_borde,width=tam_opc,height=tam_casilla-tam_borde)
    
    frame_opc_reloj = tk.Frame(frame_opciones,bg=uti.col_borde)
    frame_opc_reloj.place(x=0,y=tam_borde*5 + tam_casilla*5,width=tam_opc*3 + tam_borde*4,height= tam_casilla +tam_borde*2)

    btn_cronometro = tk.Button(frame_opc_reloj,text="Cronómetro",font=("Arial",12),bg=uti.col_celda,fg=uti.col_texto)
    btn_cronometro.config(relief="flat",command=lambda: cambiar_reloj("CRONOMETRO") )
    btn_cronometro.place(x=tam_borde,y=tam_borde,width=tam_opc,height=tam_casilla)

    btn_temporizador = tk.Button(frame_opc_reloj,text="Temporizador",font=("Arial",12),bg=uti.col_celda,fg=uti.col_texto)
    btn_temporizador.config(relief="flat",command=lambda: cambiar_reloj("TEMPORIZADOR") )
    btn_temporizador.place(x=tam_borde*2 + tam_opc,y=tam_borde,width=tam_opc,height=tam_casilla)

    btn_no_reloj = tk.Button(frame_opc_reloj,text="Sin Reloj",font=("Arial",12),bg=uti.col_celda,fg=uti.col_texto)
    btn_no_reloj.config(relief="flat",command=lambda: cambiar_reloj("NORELOJ") )
    btn_no_reloj.place(x=tam_borde*3 + tam_opc*2,y=tam_borde,width=tam_opc,height=tam_casilla)

    # Para tiempo de Reloj
    label_hora = tk.Label(frame_tiempo,text="Hora",font=("Arial",12),bg=uti.col_celda_desact,fg=uti.col_celda)
    label_hora.place(x=tam_borde,y=tam_borde,width=tam_opc,height=tam_casilla)
    
    label_minuto = tk.Label(frame_tiempo,text="Minutos",font=("Arial",12),bg=uti.col_celda_desact,fg=uti.col_celda)
    label_minuto.place(x=tam_borde*2 + tam_opc,y=tam_borde,width=tam_opc,height=tam_casilla)
    
    label_segundo = tk.Label(frame_tiempo,text="Segundos",font=("Arial",12),bg=uti.col_celda_desact,fg=uti.col_celda)
    label_segundo.place(x=tam_borde*3 + tam_opc*2,y=tam_borde,width=tam_opc,height=tam_casilla)
    
    hora = tk.StringVar(ventana, value=str("00"))
    minuto = tk.StringVar(ventana, value=str("00"))
    segundo = tk.StringVar(ventana, value=str("00"))
    entry_hora = tk.Entry(frame_tiempo,textvariable= hora,font=("Arial",12))
    entry_hora.place(x=tam_borde,y=tam_borde*2 + tam_casilla,width=tam_opc,height=tam_casilla)
    
    entry_minuto = tk.Entry(frame_tiempo,textvariable= minuto,font=("Arial",12))
    entry_minuto.place(x=tam_borde*2 + tam_opc,y=tam_borde*2 + tam_casilla,width=tam_opc,height=tam_casilla)
    
    entry_segundo = tk.Entry(frame_tiempo,textvariable= segundo,font=("Arial",12))
    entry_segundo.place(x=tam_borde*3 + tam_opc*2,y=tam_borde*2 + tam_casilla,width=tam_opc,height=tam_casilla)

    # Botón de volver
    btn_volver = tk.Button(frame_volver,text="Volver",font=("Arial",12),bg=uti.col_celda_desact,fg=uti.col_celda)
    btn_volver.config(relief="flat",command= salir )
    btn_volver.place(x=tam_borde,y=tam_borde,width=tam_opc*3 + tam_borde*2,height=tam_casilla)



    #frame_tiempo = tk.Frame(frame_principal)
    #frame_tiempo.grid(column=1,row=0)
    


    cargar_datos()
    ventana.mainloop()
    pass

def ventana_principal(nombre):
    def buscar_guardada():
        partidas = uti.buscar_archivo("kakuro2025_juego_actual")
        if nombre in partidas:
            return True
        return False
    
    partida_guardada = buscar_guardada()
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
    num_fila = 0

    btn_jugar = tk.Button(
        frame_opc_derecha,
        text="Jugar",
        font=("Arial",18),
        bg="#f0f0f0",
        fg="#090909",
        command= lambda: uti.abrir_ventana(ventana,lambda: ventana_jugar(nombre,False))
    )
    btn_jugar.grid(row=num_fila,column=0,columnspan=2, padx=5,pady=5)
    num_fila += 1

    if partida_guardada:
        btn_continuar = tk.Button(
            frame_opc_derecha,
            text="Continuar Partida",
            font=("Arial",14),
            bg="#f0f0f0",
            fg="#090909",
            command= lambda: uti.abrir_ventana(ventana,lambda: ventana_jugar(nombre,True))
        )
        btn_continuar.grid(row=num_fila,column=0,columnspan=2, padx=5,pady=5)
        num_fila += 1

    
    btn_configurar = tk.Button(
        frame_opc_derecha,
        text="Configurar",
        font=("Arial",12),
        bg="#f0f0f0",
        fg="#090909",
        command= lambda: uti.abrir_ventana(ventana,lambda: ventana_configuracion(nombre))
    )
    btn_configurar.grid(row=num_fila,column=0,columnspan=2, padx=5,pady=5)
    num_fila += 1
    
    btn_records = tk.Button(
        frame_opc_derecha,
        text="Records",
        font=("Arial",12),
        bg="#f0f0f0",
        fg="#090909",
        command= lambda: uti.abrir_ventana(ventana,lambda: ventana_records(nombre))
    )
    btn_records.grid(row=num_fila,column=0,columnspan=2, padx=5,pady=5)
    num_fila += 1
    
    btn_ayuda = tk.Button(
        frame_opc_abajo,
        text="Ayuda",
        font=("Arial",12),
        bg="#f0f0f0",
        fg="#090909",
        command= lambda: uti.ayuda("Kakuro")
    )
    btn_ayuda.grid(row=0,column=0,columnspan=1, padx=5,pady=5)

    btn_acerca_de = tk.Button(
        frame_opc_abajo,
        text="Acerca De",
        font=("Arial",12),
        bg="#f0f0f0",
        fg="#090909",
        command= lambda: uti.acerca_de("Sobre el sistema")
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
    btn_salir.grid(row=num_fila,column=0,columnspan=2, padx=5,pady=5)


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