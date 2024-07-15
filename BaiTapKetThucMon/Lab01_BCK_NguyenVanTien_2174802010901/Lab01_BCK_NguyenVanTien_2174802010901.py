import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import math

# Hàm xử lý các phép toán cơ bản
def calculate():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operator = combo_operator.get()

        if operator == '+':
            result = num1 + num2
        elif operator == '-':
            result = num1 - num2
        elif operator == '*':
            result = num1 * num2
        elif operator == '/':
            if num2 == 0:
                raise ValueError("Không thể chia cho 0")
            result = num1 / num2
        else:
            raise ValueError("Phép toán không hợp lệ")

        entry_result.config(state='normal')
        entry_result.delete(0, tk.END)
        entry_result.insert(0, str(result))
        entry_result.config(state='readonly')

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Hàm giải phương trình bậc 1
def solve_linear_equation():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())

        if a == 0:
            if b == 0:
                result = "Vô số nghiệm"
            else:
                result = "Vô nghiệm"
        else:
            result = -b / a

        entry_linear_result.config(state='normal')
        entry_linear_result.delete(0, tk.END)
        entry_linear_result.insert(0, str(result))
        entry_linear_result.config(state='readonly')

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Hàm giải phương trình bậc 2
def solve_quadratic_equation():
    try:
        a = float(entry_a_quad.get())
        b = float(entry_b_quad.get())
        c = float(entry_c_quad.get())

        if a == 0:
            raise ValueError("a không thể bằng 0 trong phương trình bậc 2")

        delta = b**2 - 4*a*c
        if delta < 0:
            result = "Vô nghiệm"
        elif delta == 0:
            result = -b / (2*a)
        else:
            win1 = (-b + math.sqrt(delta)) / (2*a)
            win2 = (-b - math.sqrt(delta)) / (2*a)
            result = f"Nghiệm 1: {win1}, Nghiệm 2: {win2}"

        entry_quadratic_result.config(state='normal')
        entry_quadratic_result.delete(0, tk.END)
        entry_quadratic_result.insert(0, str(result))
        entry_quadratic_result.config(state='readonly')

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Tạo cửa sổ chính
win = tk.Tk()
win.title("Chương Trình Giải Bài Toán")
win.geometry("1000x700")

# Tạo Notebook (tabs)
notebook = ttk.Notebook(win)
notebook.pack(expand=True, fill='both')

# Tab 1: Phép toán cơ bản
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='Phép Toán Cơ Bản')

# Widgets cho Tab 1
lbl_num1 = ttk.Label(tab1, text="Số thứ nhất:")
lbl_num1.pack(pady=5)
entry_num1 = ttk.Entry(tab1)
entry_num1.pack(pady=5)

lbl_operator = ttk.Label(tab1, text="Phép toán:")
lbl_operator.pack(pady=5)
combo_operator = ttk.Combobox(tab1, values=["+", "-", "*", "/"])
combo_operator.pack(pady=5)

lbl_num2 = ttk.Label(tab1, text="Số thứ hai:")
lbl_num2.pack(pady=5)
entry_num2 = ttk.Entry(tab1)
entry_num2.pack(pady=5)

btn_calculate = ttk.Button(tab1, text="Tính Toán", command=calculate)
btn_calculate.pack(pady=5)

lbl_result = ttk.Label(tab1, text="Kết quả:")
lbl_result.pack(pady=5)
entry_result = ttk.Entry(tab1, state='readonly')
entry_result.pack(pady=5)

# Tab 2: Phương trình
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text='Phương Trình')

# Tạo Frames cho phương trình bậc 1 và bậc 2
frame_linear = ttk.Frame(tab2)
frame_linear.pack(side='left', expand=True, fill='both', padx=20, pady=20)

frame_quadratic = ttk.Frame(tab2)
frame_quadratic.pack(side='right', expand=True, fill='both', padx=20, pady=20)

# Widgets cho phương trình bậc 1
lbl_linear_eq = ttk.Label(frame_linear, text="Phương trình bậc 1 (ax + b = 0):")
lbl_linear_eq.pack(pady=5)

lbl_a = ttk.Label(frame_linear, text="a:")
lbl_a.pack(pady=5)
entry_a = ttk.Entry(frame_linear)
entry_a.pack(pady=5)

lbl_b = ttk.Label(frame_linear, text="b:")
lbl_b.pack(pady=5)
entry_b = ttk.Entry(frame_linear)
entry_b.pack(pady=5)

btn_solve_linear = ttk.Button(frame_linear, text="Giải Phương Trình Bậc 1", command=solve_linear_equation)
btn_solve_linear.pack(pady=5)

lbl_linear_result = ttk.Label(frame_linear, text="Kết quả:")
lbl_linear_result.pack(pady=5)
entry_linear_result = ttk.Entry(frame_linear, state='readonly')
entry_linear_result.pack(pady=5)

# Widgets cho phương trình bậc 2
lbl_quadratic_eq = ttk.Label(frame_quadratic, text="Phương trình bậc 2 (ax^2 + bx + c = 0):")
lbl_quadratic_eq.pack(pady=5)

lbl_a_quad = ttk.Label(frame_quadratic, text="a:")
lbl_a_quad.pack(pady=5)
entry_a_quad = ttk.Entry(frame_quadratic)
entry_a_quad.pack(pady=5)

lbl_b_quad = ttk.Label(frame_quadratic, text="b:")
lbl_b_quad.pack(pady=5)
entry_b_quad = ttk.Entry(frame_quadratic)
entry_b_quad.pack(pady=5)

lbl_c_quad = ttk.Label(frame_quadratic, text="c:")
lbl_c_quad.pack(pady=5)
entry_c_quad = ttk.Entry(frame_quadratic)
entry_c_quad.pack(pady=5)

btn_solve_quadratic = ttk.Button(frame_quadratic, text="Giải Phương Trình Bậc 2", command=solve_quadratic_equation)
btn_solve_quadratic.pack(pady=5)

lbl_quadratic_result = ttk.Label(frame_quadratic, text="Kết quả:")
lbl_quadratic_result.pack(pady=5)
entry_quadratic_result = ttk.Entry(frame_quadratic, state='readonly')
entry_quadratic_result.pack(pady=5)

# Chạy ứng dụng
win.mainloop()