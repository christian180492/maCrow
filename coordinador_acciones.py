import tkinter as tk
import json
import os
import maCrow_new  # Asegúrate de que maCrow_new tiene las funciones necesarias definidas
import threading

# Añadimos la variable global is_recording
is_recording = False

# Definición de funciones
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

def delete_action():
    try:
        selected_file = file_list.get(file_list.curselection())
        folder_path = "acciones"
        file_path = os.path.join(folder_path, selected_file)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {selected_file} deleted successfully!")
        else:
            print(f"File {selected_file} not found!")
        show_file_list()  # Actualiza la lista de archivos después de eliminar
    except Exception as e:
        print(f"Error: {e}")
        print("Please select a file from the list to delete.")

def add_to_order():
    try:
        selected_file = file_list.get(file_list.curselection())
        ordered_actions_list.insert(tk.END, selected_file)
    except Exception as e:
        print(f"Error: {e}")
        print("Please select a file from the list to add.")

def play_ordered():
    for action_file in ordered_actions_list.get(0, tk.END):
        folder_path = "acciones"
        file_path = os.path.join(folder_path, action_file)
        print(f"Playing {action_file}...")
        maCrow_new.replay(file_path)
        
def remove_from_order():
    try:
        selected_index = ordered_actions_list.curselection()
        ordered_actions_list.delete(selected_index)
    except Exception as e:
        print(f"Error removing item: {e}")

def move_up():
    try:
        selected_index = ordered_actions_list.curselection()[0]
        if selected_index > 0:
            item_to_move = ordered_actions_list.get(selected_index)
            ordered_actions_list.delete(selected_index)
            ordered_actions_list.insert(selected_index - 1, item_to_move)
            ordered_actions_list.select_set(selected_index - 1)
    except Exception as e:
        print(f"Error moving item up: {e}")

def move_down():
    try:
        selected_index = ordered_actions_list.curselection()[0]
        if selected_index < ordered_actions_list.size() - 1:
            item_to_move = ordered_actions_list.get(selected_index)
            ordered_actions_list.delete(selected_index)
            ordered_actions_list.insert(selected_index + 1, item_to_move)
            ordered_actions_list.select_set(selected_index + 1)
    except Exception as e:
        print(f"Error moving item down: {e}")


# Interfaz gráfica
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

button_delete = tk.Button(root, text="Delete Action", command=delete_action)
button_delete.pack()

ordered_actions_label = tk.Label(root, text="Ordered Actions:")
ordered_actions_label.pack()

ordered_actions_list = tk.Listbox(root, yscrollcommand=scrollbar.set)
ordered_actions_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

button_add_to_order = tk.Button(root, text="Add to Order", command=add_to_order)
button_add_to_order.pack()

button_play_ordered = tk.Button(root, text="Play Ordered", command=play_ordered)
button_play_ordered.pack()

button_remove_from_order = tk.Button(root, text="Remove from Order", command=remove_from_order)
button_remove_from_order.pack()

button_move_up = tk.Button(root, text="Move Up", command=move_up)
button_move_up.pack()

button_move_down = tk.Button(root, text="Move Down", command=move_down)
button_move_down.pack()

root.mainloop()

# TODO: Crear un mecanismo para ordenar las acciones de la manera en que guste al usuario.
