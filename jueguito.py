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

    def generar_tabla():
        datos = []
        for auto in autos:
            datos.append( ( auto, autos[auto]["marca"], autos[auto]["modelo"]) )

        for row in datos:
            tree.insert('', tk.END, values=row)
            tree.bind('<Double 1>', activar_edicion)


    ventana = tk.Tk()
    frame_juego = tk.Frame(ventana)
    frame_juego.grid(row=0, column=0, columnspan=6, padx= 0, pady= 0)
    tree0 = ttk.Treeview(frame_juego, columns=("0",), show='')
    generar_columna(tree0)
    tree0.grid(row=0, column=0, columnspan=2, padx= 1, pady= 0)

    tree1 = ttk.Treeview(frame_juego, columns=("0",), show='')
    generar_columna(tree1)
    tree1.grid(row=0, column=2, columnspan=2, padx= 0, pady= 0)

    tree2 = ttk.Treeview(frame_juego, columns=("0",), show='')
    generar_columna(tree2)
    tree2.grid(row=0, column=4, columnspan=2, padx= 0, pady= 0)

    

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
    frame_opc_derecha.grid(row=0, column=2, columnspan=1, padx= 5, pady= 5)
    frame_opc_abajo = tk.Frame(ventana)
    frame_opc_abajo.grid(row=1, column=0, columnspan=3, padx= 5, pady= 5)

    rut_img = uti.obtener_ruta()+"/Recursos/logo.png"
    #img = 

    btn_jugar = tk.Button(
        frame_opc_derecha,
        text="Jugar",
        font=("Arial",12),
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
        frame_opc_derecha,
        text="Configurar",
        font=("Arial",12),
        bg="#f0f0f0",
        fg="#090909",
        command= lambda: uti.abrir_ventana(ventana,lambda: ventana_jugar())
    )
    btn_ayuda.grid(row=3,column=0,columnspan=1, padx=5,pady=5)

    btn_acerca_de = tk.Button(
        frame_opc_derecha,
        text="Configurar",
        font=("Arial",12),
        bg="#f0f0f0",
        fg="#090909",
        command= lambda: uti.abrir_ventana(ventana,lambda: ventana_jugar())
    )
    btn_acerca_de.grid(row=3,column=1,columnspan=1, padx=5,pady=5)

    btn_salir = tk.Button(
        frame_opc_abajo,
        text="Configurar",
        font=("Arial",12),
        bg="#f0f0f0",
        fg="#090909",
        command= lambda: uti.abrir_ventana(ventana,lambda: ventana_jugar())
    )
    btn_salir.grid(row=0,column=0,columnspan=1, padx=5,pady=5)


    ventana.mainloop()

ventana_principal()