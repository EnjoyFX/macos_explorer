import tkinter as tk
from tkinter import filedialog, messagebox
import os
import subprocess

APP_TITLE = "File Visibility Toggler for MacOS"
APP_VERSION = "1.0.1"


def toggle_visibility(file_path):
    file_name = os.path.basename(file_path)
    parent_dir = os.path.dirname(file_path)

    if file_name.startswith('.'):
        # File or folder is currently hidden, make it visible
        new_name = file_name[1:]
        new_path = os.path.join(parent_dir, new_name)
        try:
            os.rename(file_path, new_path)
            # Remove hidden flag:
            subprocess.run(["chflags", "nohidden", new_path])
            return new_path, 'visible'
        except Exception as e:
            print(f'Issue in toggle_visibility catched: {e}')
            return None, None
    else:
        # File or folder is currently visible, make it hidden
        new_name = '.' + file_name
        new_path = os.path.join(parent_dir, new_name)
        try:
            os.rename(file_path, new_path)
            # Add hidden flag:
            subprocess.run(["chflags", "hidden", new_path])
            return new_path, 'hidden'
        except Exception as e:
            print(f'Issue in toggle_visibility catched: {e}')
            return None, None


def txt_selector(visible_count, hidden_count, subj='file(s)'):
    txt = "No changes done"
    if visible_count == 0 and hidden_count:
        txt = f"{hidden_count} {subj} became HIDDEN."
    elif hidden_count == 0 and visible_count:
        txt = f"{visible_count} {subj} became VISIBLE"
    else:
        if visible_count and hidden_count:
            txt = (f"{visible_count} {subj} became VISIBLE,\n"
                   f"{hidden_count} {subj} became HIDDEN.")
    return txt


def select_files():
    files = filedialog.askopenfilenames()
    visible_count, hidden_count = 0, 0
    for file in files:
        result, status = toggle_visibility(file)
        if status == 'visible':
            visible_count += 1
        elif status == 'hidden':
            hidden_count += 1
    if (visible_count + hidden_count) > 0:
        messagebox.showinfo("Success",
                                txt_selector(visible_count, hidden_count))


def select_folder():
    folder = filedialog.askdirectory()
    visible_count, hidden_count = 0, 0
    if folder:
        for root, dirs, files in os.walk(folder):
            for name in files + dirs:
                result, status = toggle_visibility(os.path.join(root, name))
                if status == 'visible':
                    visible_count += 1
                elif status == 'hidden':
                    hidden_count += 1
    if (visible_count + hidden_count) > 0:
        messagebox.showinfo("Success",
                            txt_selector(visible_count,
                                         hidden_count,
                                         subj='file(s)/folder(s)'))


def center_window(window, width=300, height=200):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')


# Create the main window
root = tk.Tk()
root.title(f"{APP_TITLE} v{APP_VERSION}")

# Center the window
center_window(root, 340, 150)

# Create buttons for selecting files and folders
btn_select_files = tk.Button(root,
                             text="Select File(s)",
                             command=select_files)
btn_select_files.pack(pady=10)

btn_select_folder = tk.Button(root,
                              text="Select Folder(s)",
                              command=select_folder)
btn_select_folder.pack(pady=10)

# Create exit button
btn_exit = tk.Button(root,
                     text="Exit",
                     command=root.quit)
btn_exit.pack(pady=10)

# Run the application
root.mainloop()
