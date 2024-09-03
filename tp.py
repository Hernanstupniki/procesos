import tkinter as tk
import random
import threading
import time

# Configuración de la memoria
MEMORIA_TOTAL = 1000  # Memoria total disponible
MEMORIA_USADA = 0  # Memoria actualmente en uso

# Lista de procesos
procesos = []
procesos_listos = []
procesos_bloqueados = []
procesos_swap = []
procesos_terminados = []
proceso_ejecucion = None

# Clase para representar un proceso
class Proceso:
    def __init__(self, id, memoria):
        self.id = id
        self.memoria = memoria
        self.estado = 'Listo'

    def __str__(self):
        return f"Proceso {self.id}: {self.estado} (Memoria: {self.memoria})"

# Función para crear procesos aleatorios
def crear_procesos():
    global MEMORIA_USADA
    while True:
        if len(procesos) < 10:  # Máximo 10 procesos simultáneos
            memoria_necesaria = random.randint(50, 200)
            agregar_proceso(memoria_necesaria)
        time.sleep(2)

# Función para agregar un proceso manualmente o aleatoriamente
def agregar_proceso(memoria_necesaria):
    global MEMORIA_USADA
    proceso = Proceso(len(procesos) + 1, memoria_necesaria)
    
    # Probabilidad de que un proceso sea bloqueado (ajustar según sea necesario)
    probabilidad_bloqueo = 0.3  # 30% de probabilidad de bloqueo
    
    if random.random() < probabilidad_bloqueo:
        proceso.estado = 'Bloqueado'
        procesos_bloqueados.append(proceso)
    else:
        if MEMORIA_USADA + memoria_necesaria <= MEMORIA_TOTAL:
            procesos_listos.append(proceso)
            MEMORIA_USADA += memoria_necesaria
            proceso.estado = 'Listo'
        else:
            proceso.estado = 'Swap'
            procesos_swap.append(proceso)
    
    procesos.append(proceso)
    actualizar_interfaz()

# Función para revisar procesos en Swap y moverlos a Listos si hay suficiente memoria
def revisar_swap():
    global MEMORIA_USADA
    while True:
        for proceso in procesos_swap[:]:
            if MEMORIA_USADA + proceso.memoria <= MEMORIA_TOTAL:
                procesos_swap.remove(proceso)
                procesos_listos.append(proceso)
                proceso.estado = 'Listo'
                MEMORIA_USADA += proceso.memoria
        time.sleep(1)

# Función para simular la ejecución de procesos
def ejecutar_procesos():
    global MEMORIA_USADA, proceso_ejecucion
    while True:
        if procesos_listos:
            proceso_ejecucion = procesos_listos.pop(0)
            proceso_ejecucion.estado = 'Ejecutando'
            actualizar_interfaz()
            time.sleep(3)  # Simula el tiempo de ejecución del proceso
            proceso_ejecucion.estado = 'Terminado'
            procesos_terminados.append(proceso_ejecucion)
            MEMORIA_USADA -= proceso_ejecucion.memoria
            proceso_ejecucion = None
        actualizar_interfaz()
        time.sleep(1)

# Función para manejar el evento de agregar un proceso manualmente
def agregar_proceso_manual():
    try:
        memoria_necesaria = int(memoria_entry.get())
        if memoria_necesaria > 0:
            agregar_proceso(memoria_necesaria)
        else:
            tk.messagebox.showerror("Error", "La memoria debe ser un número positivo.")
    except ValueError:
        tk.messagebox.showerror("Error", "Ingrese un valor numérico válido para la memoria.")

# Actualiza la interfaz gráfica
def actualizar_interfaz():
    memoria_label.config(text=f"Memoria Usada: {MEMORIA_USADA}/{MEMORIA_TOTAL}")
    listos_listbox.delete(0, tk.END)
    for p in procesos_listos:
        listos_listbox.insert(tk.END, str(p))
    bloqueados_listbox.delete(0, tk.END)
    for p in procesos_bloqueados:
        bloqueados_listbox.insert(tk.END, str(p))
    swap_listbox.delete(0, tk.END)
    for p in procesos_swap:
        swap_listbox.insert(tk.END, str(p))
    terminados_listbox.delete(0, tk.END)
    for p in procesos_terminados:
        terminados_listbox.insert(tk.END, str(p))
    ejecucion_label.config(text=f"Proceso en Ejecución: {proceso_ejecucion if proceso_ejecucion else 'Ninguno'}")

# Configuración de la interfaz gráfica con Tkinter
ventana = tk.Tk()
ventana.title("Simulador de Gestión de Procesos y Memoria")

memoria_label = tk.Label(ventana, text=f"Memoria Usada: {MEMORIA_USADA}/{MEMORIA_TOTAL}")
memoria_label.pack()

# Sección para agregar procesos manualmente
frame_agregar = tk.Frame(ventana)
frame_agregar.pack(pady=10)

memoria_label_entry = tk.Label(frame_agregar, text="Memoria del Proceso:")
memoria_label_entry.pack(side=tk.LEFT)

memoria_entry = tk.Entry(frame_agregar, width=10)
memoria_entry.pack(side=tk.LEFT)

agregar_boton = tk.Button(frame_agregar, text="Agregar Proceso", command=agregar_proceso_manual)
agregar_boton.pack(side=tk.LEFT)

# Listbox para los procesos en diferentes estados
listos_label = tk.Label(ventana, text="Procesos Listos")
listos_label.pack()
listos_listbox = tk.Listbox(ventana)
listos_listbox.pack()

ejecucion_label = tk.Label(ventana, text="Proceso en Ejecución: Ninguno")
ejecucion_label.pack()

bloqueados_label = tk.Label(ventana, text="Procesos Bloqueados")
bloqueados_label.pack()
bloqueados_listbox = tk.Listbox(ventana)
bloqueados_listbox.pack()

swap_label = tk.Label(ventana, text="Procesos en Swap")
swap_label.pack()
swap_listbox = tk.Listbox(ventana)
swap_listbox.pack()

terminados_label = tk.Label(ventana, text="Procesos Terminados")
terminados_label.pack()
terminados_listbox = tk.Listbox(ventana)
terminados_listbox.pack()

# Hilos para la simulación de creación, ejecución de procesos y revisión de Swap
creador_procesos_thread = threading.Thread(target=crear_procesos, daemon=True)
ejecutor_procesos_thread = threading.Thread(target=ejecutar_procesos, daemon=True)
revisor_swap_thread = threading.Thread(target=revisar_swap, daemon=True)

creador_procesos_thread.start()
ejecutor_procesos_thread.start()
revisor_swap_thread.start()

ventana.mainloop()
