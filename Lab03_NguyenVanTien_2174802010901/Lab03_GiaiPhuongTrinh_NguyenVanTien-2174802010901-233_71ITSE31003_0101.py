import tkinter as tk
from tkinter import ttk

def solve_equation():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())

        if a == 0:
            result_label.config(text="Lỗi: a không được bằng 0")
        else:
            x = -b / a
            result_label.config(text=f"Giá trị của x: {x:.2f}")
    except ValueError:
        result_label.config(text="Lỗi: Vui lòng nhập các giá trị hợp lệ")

def reset_form():
    entry_a.delete(0, tk.END)
    entry_b.delete(0, tk.END)
    result_label.config(text="")

# Tạo cửa sổ chính
root = tk.Tk()
root.title("Chương Trinh Giải Bài Toán")

# Tạo LabelFrame cho các trường nhập liệu
input_frame = ttk.LabelFrame(root, text="Nhập các giá trị")
input_frame.pack(padx=20, pady=20)

# Tạo nhãn và trường nhập liệu cho a
label_a = ttk.Label(input_frame, text="a:")
label_a.grid(row=0, column=0, padx=10, pady=10)
entry_a = ttk.Entry(input_frame)
entry_a.grid(row=0, column=1, padx=10, pady=10)

# Tạo nhãn và trường nhập liệu cho b
label_b = ttk.Label(input_frame, text="b:")
label_b.grid(row=1, column=0, padx=10, pady=10)
entry_b = ttk.Entry(input_frame)
entry_b.grid(row=1, column=1, padx=10, pady=10)

# Tạo nút "Solve"
solve_button = ttk.Button(root, text="Solve", command=solve_equation)
solve_button.pack(pady=10)

# Tạo ô hiển thị kết quả
result_label = ttk.Label(root, text="")
result_label.pack(pady=10)

# Tạo nút "Reset"
reset_button = ttk.Button(root, text="Reset", command=reset_form)
reset_button.pack(pady=10)

root.mainloop()