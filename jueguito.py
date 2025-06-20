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

    def generar_tabla(frame):
        for i in range(0,9):
            for j in range(0,9):
                tam = tam_casilla
                pos_x = (tam + 2) * j
                pos_y = (tam + 2) * i
                frame_actual = tk.Frame(frame)
                btn_act = tk.Button(
                    frame,
                    text=str(i)+str(j),
                    font=("Arial",12),
                    bg=uti.col_celda,
                    fg= uti.col_texto,
                    command= ""
                )
                if i == j:
                    frame_actual.config(bg="#677083")
                    btn_act.config(bg="#677083",state="disabled")
                

                #frame_actual.place(x=pos_x,y=pos_y,width=15,height=15)
                btn_act.bind('<Button 1>', lambda event, x=i,y=j: seleccionar_casilla( (str(x)+str(y)),celda_actual ))
                btn_act.place(x=pos_x,y=pos_y,width=tam,height=tam)
                tablero[(str(i)+str(j))] = [btn_act,str(i)+str(j)]

    def generar_interfaz():
        pass

    celda_actual = [""]
    tam_casilla = 45
    tam_juego = (tam_casilla + 2) * 9
    ventana = tk.Tk()
    ventana.geometry(str(tam_juego + 10)+"x"+str(tam_juego + 10))
    frame_juego = tk.Frame(ventana,bg="#090909")
    #frame_juego.grid(row=0, column=0, columnspan=1, padx= 0, pady= 0)
    frame_juego.place(x=0, y=0, width=tam_juego, height=tam_juego)
    tablero={}
    generar_tabla(frame_juego)
    generar_interfaz()
    print(tablero)
    

    # Define column headings
    
    #tree.heading('Placa', text='Placa')
    #tree.heading('Marca', text='Marca')
    #tree.heading('Modelo', text='Modelo')
    # Insert datos
    #generar_tabla()


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