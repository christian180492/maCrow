import tkinter as tk
import json
import os
import maCrow_new  # Asegúrate de que maCrow_new tiene las funciones necesarias definidas
import threading

# Añadimos la variable global is_recording
is_recording = False

def save_action():
    global is_recording
    file_name = entry.get().strip()
    if file_name and not is_recording:  # Solo proceder si el nombre de archivo no está vacío y no se está grabando
        is_recording = True
        folder_path = "acciones"
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, file_name + ".json")
        # Inicia la grabación en un hilo nuevo
        threading.Thread(target=maCrow_new.record, args=(file_path, lambda: is_recording), daemon=True).start() # Pasamos una lambda como indicador de parada
        print(f"File {file_name}.json saved successfully!")
        show_file_list()
        

def stop_recording():
    global is_recording
    if is_recording:
        is_recording = False
        print("Recording stopped by user.")

def show_file_list():
    file_list.delete(0, tk.END)
    folder_path = "acciones"
    os.makedirs(folder_path, exist_ok=True)
    files = os.listdir(folder_path)
    for file_name in files:
        file_list.insert(tk.END, file_name)

def play_action():
    try:
        selected_file = file_list.get(file_list.curselection())
        folder_path = "acciones"
        file_path = os.path.join(folder_path, selected_file)
        maCrow_new.replay(file_path)
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

button_stop = tk.Button(root, text="Stop", command=stop_recording)  # Añadimos el botón de Stop
button_stop.pack()

button_show = tk.Button(root, text="Show File List", command=show_file_list)
button_show.pack()

scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

file_list = tk.Listbox(root, yscrollcommand=scrollbar.set)
file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=file_list.yview)

root.mainloop()
