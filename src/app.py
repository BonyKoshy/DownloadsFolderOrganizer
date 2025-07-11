import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# File categories
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Music": [".mp3", ".wav", ".aac"],
    "Archives": [".zip", ".rar", ".tar", ".gz"],
    "Code": [".py", ".js", ".html", ".css", ".java"],
    "Others": []
}

moved_files_log = []
dark_mode = False

def organize_files(folder_path, progress_bar, status_label, delete_empty):
    global moved_files_log
    moved_files_log.clear()

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    total_files = len(files)

    if total_files == 0:
        messagebox.showinfo("Info", "No files to organize!")
        return

    progress_bar["maximum"] = total_files
    progress_bar["value"] = 0

    for index, file in enumerate(files):
        file_path = os.path.join(folder_path, file)
        file_ext = os.path.splitext(file)[-1].lower()
        destination_folder = "Others"

        for category, extensions in FILE_CATEGORIES.items():
            if file_ext in extensions:
                destination_folder = category
                break

        category_path = os.path.join(folder_path, destination_folder)
        if not os.path.exists(category_path):
            os.makedirs(category_path)

        new_file_path = os.path.join(category_path, file)
        shutil.move(file_path, new_file_path)
        moved_files_log.append((new_file_path, file_path))

        progress_bar["value"] += 1
        root.update_idletasks()

    with open(os.path.join(folder_path, "organizer_log.txt"), "w") as log:
        for new_path, old_path in moved_files_log:
            log.write(f"{old_path} -> {new_path}\n")

    if delete_empty:
        delete_empty_folders(folder_path)

    status_label.config(text="Files organized successfully!")
    messagebox.showinfo("Success", "Files have been organized successfully!")

def delete_empty_folders(folder_path):
    for root_dir, dirs, files in os.walk(folder_path, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root_dir, dir_name)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)

def undo_last_action(status_label):
    if not moved_files_log:
        messagebox.showinfo("Info", "No actions to undo!")
        return

    for new_path, old_path in reversed(moved_files_log):
        shutil.move(new_path, old_path)

    moved_files_log.clear()
    status_label.config(text="Undo completed! Files restored.")
    messagebox.showinfo("Success", "Undo completed! Files restored to original locations.")

def browse_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        entry_folder_path.delete(0, tk.END)
        entry_folder_path.insert(0, folder_selected)

def toggle_dark_mode():
    global dark_mode
    dark_mode = not dark_mode
    bg_color = "#333" if dark_mode else "#f4f4f4"
    fg_color = "white" if dark_mode else "black"

    root.configure(bg=bg_color)
    frame.configure(bg=bg_color)
    status_label.configure(bg=bg_color, fg=fg_color)
    delete_empty_check.configure(bg=bg_color, fg=fg_color)

    btn_browse.configure(bg="#007BFF" if not dark_mode else "#555", fg="white")
    btn_organize.configure(bg="#28a745" if not dark_mode else "#666", fg="white")
    btn_undo.configure(bg="#dc3545" if not dark_mode else "#777", fg="white")
    btn_toggle_dark.configure(bg="#FFC107" if not dark_mode else "#888", fg="black")

# GUI Setup
root = tk.Tk()
root.title("Enhanced File Organizer")
root.geometry("500x350")
root.resizable(False, False)
root.configure(bg="#f4f4f4")

frame = tk.Frame(root, bg="#f4f4f4")
frame.pack(pady=20)

entry_folder_path = tk.Entry(frame, width=50)
entry_folder_path.pack(side=tk.LEFT, padx=5)

btn_browse = tk.Button(frame, text="Browse", command=browse_folder, bg="#007BFF", fg="white", padx=10)
btn_browse.pack(side=tk.LEFT)

progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
progress_bar.pack(pady=10)

status_label = tk.Label(root, text="", bg="#f4f4f4", fg="green")
status_label.pack()

delete_empty_var = tk.BooleanVar()
delete_empty_check = tk.Checkbutton(root, text="Delete Empty Folders", variable=delete_empty_var, bg="#f4f4f4")
delete_empty_check.pack()

btn_organize = tk.Button(root, text="Organize Files", command=lambda: organize_files(entry_folder_path.get(), progress_bar, status_label, delete_empty_var.get()), width=20, height=2, bg="#28a745", fg="white")
btn_organize.pack(pady=5)

btn_undo = tk.Button(root, text="Undo Last Action", command=lambda: undo_last_action(status_label), width=20, height=2, bg="#dc3545", fg="white")
btn_undo.pack(pady=5)

btn_toggle_dark = tk.Button(root, text="Toggle Dark Mode", command=toggle_dark_mode, width=20, height=2, bg="#FFC107", fg="black")
btn_toggle_dark.pack(pady=5)

root.mainloop()
