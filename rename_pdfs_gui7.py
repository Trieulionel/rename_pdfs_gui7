import os
import tkinter as tk
from tkinter import filedialog, messagebox

# ---------------------- Chức năng chính ----------------------
def choose_folder():
    folder_selected = filedialog.askdirectory(title="※ PDFフォルダを選択してください")
    if folder_selected:
        folder_path_var.set(folder_selected)
        list_pdfs(folder_selected)

def list_pdfs(folder_path):
    listbox.delete(0, tk.END)
    if not os.path.isdir(folder_path):
        return
    pdf_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")])
    for f in pdf_files:
        listbox.insert(tk.END, f)
    update_selected_count()  # Cập nhật số lượng file được chọn

def rename_pdfs():
    folder_path = folder_path_var.get()
    part1 = part1_var.get().strip()
    start_number = int(start_var.get())
    digits = 6
    part3 = part3_var.get().strip()
    part4 = part4_var.get().strip()

    if not os.path.isdir(folder_path):
        messagebox.showerror("エラー", "有効なフォルダを選択してください！")
        return

    selected_indices = listbox.curselection()
    if not selected_indices:
        messagebox.showinfo("通知", "少なくとも1つのPDFファイルを選択してください。")
        return

    for offset, idx in enumerate(selected_indices):
        filename = listbox.get(idx)
        old_path = os.path.join(folder_path, filename)
        number_str = str(start_number + offset).zfill(digits)
        new_name = f"{part1}-{number_str}-{part3}-{part4}.pdf"
        new_path = os.path.join(folder_path, new_name)

        if os.path.exists(new_path):
            messagebox.showerror("エラー", f"{new_name} は既に存在します！")
            return

        os.rename(old_path, new_path)
        listbox.delete(idx)
        listbox.insert(idx, new_name)  # giữ nguyên vị trí

    start_var.set(str(start_number + len(selected_indices)))
    listbox.selection_clear(0, tk.END)
    update_selected_count()
    output_label.config(text=f"※ {len(selected_indices)} 個のPDFファイルの名前を変更しました！", fg="#1565c0")

# --- Chọn tất cả / bỏ chọn ---
def select_all():
    listbox.select_set(0, tk.END)
    update_selected_count()

def deselect_all():
    listbox.selection_clear(0, tk.END)
    update_selected_count()

def update_selected_count(event=None):
    count = len(listbox.curselection())
    selected_count_var.set(f"※ 選択中のファイル数: {count}")

# ---------------------- Giao diện ----------------------
root = tk.Tk()
root.title("※ PDF 名前変更ツール ")
root.geometry("680x720")
root.resizable(False, False)
root.configure(bg="#cce6ff")  # tông xanh nhẹ

folder_path_var = tk.StringVar()
part1_var = tk.StringVar(value="3301")
start_var = tk.StringVar(value="100011")
part3_var = tk.StringVar(value="A0")
part4_var = tk.StringVar(value="N0")
selected_count_var = tk.StringVar(value="※ 選択中のファイル数: 0")

# --- Chọn folder ---
tk.Label(root, text="※ PDFフォルダを選択:", bg="#cce6ff", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10,0))
folder_frame = tk.Frame(root, bg="#cce6ff")
folder_frame.pack(fill="x", padx=10)
folder_entry = tk.Entry(folder_frame, textvariable=folder_path_var, font=("Arial",10))
folder_entry.pack(side="left", fill="x", expand=True, pady=5)
tk.Button(folder_frame, text="※ 選択...", bg="#4da6ff", fg="white", font=("Arial",10,"bold"), command=choose_folder).pack(side="right", padx=5, pady=5)

# --- Chọn tất cả / bỏ chọn ---
button_frame = tk.Frame(root, bg="#cce6ff")
button_frame.pack(fill="x", padx=10)
tk.Button(button_frame, text="※ すべて選択", bg="#4da6ff", fg="white", font=("Arial",10,"bold"), command=select_all).pack(side="left", fill="x", expand=True, padx=5)
tk.Button(button_frame, text="※ 選択解除", bg="#4da6ff", fg="white", font=("Arial",10,"bold"), command=deselect_all).pack(side="left", fill="x", expand=True, padx=5)

# --- Listbox ---
tk.Label(root, text="※ PDFファイル一覧（複数選択可）:", bg="#cce6ff", font=("Arial",10,"bold")).pack(anchor="w", padx=10, pady=(10,0))
list_frame = tk.Frame(root)
list_frame.pack(fill="both", padx=10)
scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side="right", fill="y")
listbox = tk.Listbox(list_frame, selectmode=tk.MULTIPLE, height=10, yscrollcommand=scrollbar.set, bg="#e6f2ff", font=("Arial",10))
listbox.pack(side="left", fill="both", expand=True)
scrollbar.config(command=listbox.yview)
listbox.bind('<<ListboxSelect>>', update_selected_count)

# --- Số lượng file chọn ---
selected_count_label = tk.Label(root, textvariable=selected_count_var, bg="#cce6ff", font=("Arial",10,"bold"))
selected_count_label.pack(anchor="w", padx=10, pady=(5,5))

# --- Cấu hình tên file ---
input_frame = tk.LabelFrame(root, text="※ 名前フォーマット設定", bg="#cce6ff", font=("Arial",10,"bold"), padx=10, pady=10)
input_frame.pack(fill="x", padx=10, pady=(5,10))
for label_text, var in [("※ パート1（例: 3301）:", part1_var),
                        ("※ 開始番号（例: 100011）:", start_var),
                        ("※ パート3（例: A0）:", part3_var),
                        ("※ パート4（例: N0）:", part4_var)]:
    tk.Label(input_frame, text=label_text, bg="#cce6ff", font=("Arial",10)).pack(anchor="w", pady=2)
    tk.Entry(input_frame, textvariable=var, font=("Arial",10)).pack(fill="x", pady=2)

# --- Nút thực thi ---
tk.Button(root, text="※ 選択したPDFのみ名前を変更", bg="#3399ff", fg="white", font=("Arial",12,"bold"), command=rename_pdfs).pack(fill="x", padx=10, pady=10)

# --- Nhãn kết quả ---
output_label = tk.Label(root, text="", bg="#cce6ff", font=("Arial",11,"bold"))
output_label.pack(pady=(0,10))

root.mainloop()
