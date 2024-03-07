import tkinter as tk
import json
import os
import maCrow_new  # Asegúrate de que maCrow_new tiene la función play_action definida

def save_action():
    file_name = entry.get().strip()
    if file_name:  # Solo proceder si el nombre de archivo no está vacío
        folder_path = "acciones"
        os.makedirs(folder_path, exist_ok=True)  # Asegura que la carpeta exista
        file_path = os.path.join(folder_path, file_name + ".json")
        maCrow_new.record(file_path)
        print(f"File {file_name}.json saved successfully!")
        show_file_list()  # Actualiza la lista de archivos después de guardar

def show_file_list():
    file_list.delete(0, tk.END)  # Limpia la lista actual
    folder_path = "acciones"
    os.makedirs(folder_path, exist_ok=True)  # Asegura que la carpeta exista
    files = os.listdir(folder_path)
    for file_name in files:
        file_list.insert(tk.END, file_name)

def play_action():
    try:
        selected_file = file_list.get(file_list.curselection())  # Obtiene el archivo seleccionado
        folder_path = "acciones"
        file_path = os.path.join(folder_path, selected_file)
        maCrow_new.replay(file_path)  # Asume que esta función existe en maCrow_new
        print(f"Playing actions from {selected_file}")
    except Exception as e:
        print(f"Error: {e}")
        print("Please select a file from the list.")

root = tk.Tk()
root.title("File Saver and Viewer")

label = tk.Label(root, text="Enter file name:")
label.pack()

entry = tk.Entry(root)
entry.pack()

button_save = tk.Button(root, text="Save", command=save_action)
button_save.pack()

button_play = tk.Button(root, text="Play Action", command=play_action)
button_play.pack()

button_show = tk.Button(root, text="Show File List", command=show_file_list)
button_show.pack()

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

file_list = tk.Listbox(root, yscrollcommand=scrollbar.set)
file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=file_list.yview)

root.mainloop()

# TODO: El problema es que para cancelar la grabación hay que hacer focus en la terminal desde la que se ejecuta el script y precionar CNTRL + C y este comando mismo, también se graba.
# El hecho de que el comando CNTRL + C se grabe también, es un problema, ya que si se reproduce la grabación, el script se detendrá.
# Mi propuesta es que dentro del archivo coordinador_acciones.py tengamos un valor buleano que indique si se está grabando o no. Si se presiona grabar, estará en true y si se preciona play, estará en false.
# Además de eso poner un botón de stop que sea el que cancele la grabación cuando se está grabando y que cuando se esté reproduciendo, no haga nada ya que el valor buleano estará en false.