import tkinter as tk
from tkinter import ttk, scrolledtext, Spinbox, Checkbutton, IntVar, Radiobutton
from time import sleep
# Create instance
win = tk.Tk()

# Add a title
win.title("Python GUI")

# Create a notebook
tab_control = ttk.Notebook(win)

# Create tabs
tab1 = ttk.Frame(tab_control)
tab_control.add(tab1, text='Tab 1')

tab2 = ttk.Frame(tab_control)
tab_control.add(tab2, text='Tab 2')

tab3 = ttk.Frame(tab_control)
tab_control.add(tab3, text='Tab 3')

tab_control.pack(expand=1, fill='both')

# Tab 1 contents
mighty = ttk.LabelFrame(tab1, text=' Mighty Python ')
mighty.grid(column=0, row=0, padx=8, pady=4)

a_label = ttk.Label(mighty, text="Enter a name:")
a_label.grid(column=0, row=0, sticky='W')

def click_me():
    action.configure(text='Hello ' + name.get() + ' ' + number_chosen.get())

name = tk.StringVar()
name_entered = ttk.Entry(mighty, width=12, textvariable=name)
name_entered.grid(column=0, row=1, sticky='W')

action = ttk.Button(mighty, text="Click Me!", command=click_me)
action.grid(column=2, row=1)

ttk.Label(mighty, text="Choose a number:").grid(column=1, row=0)
number = tk.StringVar()
number_chosen = ttk.Combobox(mighty, width=12, textvariable=number, state='readonly')
number_chosen['values'] = (1, 2, 4, 42, 100)
number_chosen.grid(column=1, row=1)
number_chosen.current(0)

chVarDis = tk.IntVar()
check1 = tk.Checkbutton(mighty, text="Disabled", variable=chVarDis, state='disabled')
check1.select()
check1.grid(column=0, row=4, sticky=tk.W)

chVarUn = tk.IntVar()
check2 = tk.Checkbutton(mighty, text="UnChecked", variable=chVarUn)
check2.deselect()
check2.grid(column=1, row=4, sticky=tk.W)

chVarEn = tk.IntVar()
check3 = tk.Checkbutton(mighty, text="Enabled", variable=chVarEn)
check3.deselect()
check3.grid(column=2, row=4, sticky=tk.W)

def _spin():
    value = spin.get()
    print(value)
    scr.insert(tk.INSERT, value + '\n')

spin = Spinbox(mighty, values=(1, 2, 4, 42, 100), width=5, bd=8, command=_spin)
spin.grid(column=0, row=2)

def _spin2():
    value = spin2.get()
    print(value)
    scr.insert(tk.INSERT, value + '\n')

spin2 = Spinbox(mighty, values=(0, 50, 100), width=5, bd=20, command=_spin2)
spin2.grid(column=1, row=2)

def checkCallback(*ignoredArgs):
    if chVarUn.get():
        check3.configure(state='disabled')
    else:
        check3.configure(state='normal')
    if chVarEn.get():
        check2.configure(state='disabled')
    else:
        check2.configure(state='normal')

chVarUn.trace('w', lambda *args: checkCallback())
chVarEn.trace('w', lambda *args: checkCallback())

scrol_w = 30
scrol_h = 3
scr = scrolledtext.ScrolledText(mighty, width=scrol_w, height=scrol_h, wrap=tk.WORD)
scr.grid(column=0, row=5, columnspan=3)

colors = ["Blue", "Gold", "Red"]

def radCall():
    radSel = radVar.get()
    if radSel == 0:
        win.configure(background=colors[0])
    elif radSel == 1:
        win.configure(background=colors[1])
    elif radSel == 2:
        win.configure(background=colors[2])

radVar = tk.IntVar()
radVar.set(99)

for col in range(3):
    curRad = tk.Radiobutton(mighty, text=colors[col], variable=radVar,
                            value=col, command=radCall)
    curRad.grid(column=col, row=6, sticky=tk.W)

buttons_frame = ttk.LabelFrame(mighty, text=' Labels in a Frame ')
buttons_frame.grid(column=0, row=7)

ttk.Label(buttons_frame, text="Label1").grid(column=0, row=0, sticky=tk.W)
ttk.Label(buttons_frame, text="Label2").grid(column=1, row=0, sticky=tk.W)
ttk.Label(buttons_frame, text="Label3").grid(column=2, row=0, sticky=tk.W)

# Tab 2 contents
mighty2 = ttk.LabelFrame(tab2, text=' Another Frame ')
mighty2.grid(column=0, row=0, padx=8, pady=4)

chVarDis2 = tk.IntVar()
check1_tab2 = tk.Checkbutton(mighty2, text="Disabled", variable=chVarDis2, state='disabled')
check1_tab2.select()
check1_tab2.grid(column=0, row=0, sticky=tk.W)

chVarUn2 = tk.IntVar()
check2_tab2 = tk.Checkbutton(mighty2, text="UnChecked", variable=chVarUn2)
check2_tab2.deselect()
check2_tab2.grid(column=1, row=0, sticky=tk.W)

chVarEn2 = tk.IntVar()
check3_tab2 = tk.Checkbutton(mighty2, text="Enabled", variable=chVarEn2)
check3_tab2.deselect()
check3_tab2.grid(column=2, row=0, sticky=tk.W)

# Progress bar and buttons for Tab 2
progress_frame = ttk.LabelFrame(tab2, text=' ProgressBar  ')
progress_frame.grid(column=0, row=1, sticky='WE', padx=8, pady=4)

progress_bar = ttk.Progressbar(progress_frame, orient='horizontal', length=286, mode='determinate')
progress_bar.grid(column=0, row=0, pady=2, columnspan=4)

def run_progressbar():
    progress_bar["maximum"] = 100
    for i in range(101):
        sleep(0.05)
        progress_bar["value"] = i
        progress_bar.update()
    progress_bar["value"] = 0

def start_progressbar():
    progress_bar.start()

def stop_progressbar():
    progress_bar.stop()

def progressbar_stop_after(wait_ms=1000):
    win.after(wait_ms, progress_bar.stop)

ttk.Button(progress_frame, text="Run Progressbar", command=run_progressbar).grid(column=0, row=1, sticky='W')
ttk.Button(progress_frame, text="Start Progressbar", command=start_progressbar).grid(column=0, row=2, sticky='W')
ttk.Button(progress_frame, text="Stop immediately", command=stop_progressbar).grid(column=0, row=3, sticky='W')
ttk.Button(progress_frame, text="Stop after second", command=lambda: progressbar_stop_after(1000)).grid(column=0, row=4, sticky='W')

for child in progress_frame.winfo_children():
    child.grid_configure(padx=2, pady=2)

for child in mighty2.winfo_children():
    child.grid_configure(padx=8, pady=2)

# Tab 3 contents
tab3_frame = tk.Frame(tab3, bg='blue')
tab3_frame.pack()

for orange_color in range(2):
    canvas = tk.Canvas(tab3_frame, width=150, height=80, highlightthickness=0, bg='orange')
    canvas.grid(row=orange_color, column=orange_color)

win.mainloop()
