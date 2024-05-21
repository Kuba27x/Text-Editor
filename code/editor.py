import os
from tkinter import *
from tkinter import filedialog, colorchooser, font
from tkinter.messagebox import *
from tkinter.filedialog import *

def change_color():
    color = colorchooser.askcolor(title="Pick a color")
    text_area.config(fg=color[1])

def change_font(*args):
    text_area.config(font=(font_name.get(), size_box.get()))

def new_file():
    window.title("Untitled")
    text_area.delete(1.0, END)

def open_file():
    file = askopenfilename(defaultextension=".txt", filetypes=[("All files", "*.*"), ("Text documents", "*.txt")])
    if file == "":
        file = None
    else:
        window.title(os.path.basename(file))
        text_area.delete(1.0, END)
        file = open(file, "r")
        text_area.insert(1.0, file.read())
        file.close()

def save_file():
    file = filedialog.asksaveasfile(defaultextension=".txt", filetypes=[("All files", "*.*"), ("Text documents", "*.txt")])
    if file is None:
        return
    else:
        file.write(text_area.get(1.0, END))
        file.close()

def cut():
    text_area.event_generate("<<Cut>>")

def copy():
    text_area.event_generate("<<Copy>>")

def paste():
    text_area.event_generate("<<Paste>>")

def about():
    showinfo("About editor", "This is a basic notepad editor written in python.")

def create_new_window():
    new_window = Toplevel(window)
    new_window.title("Drawing mode")
    new_window.geometry("500x500")
    new_window.iconphoto(True, icon)

    def paint(event):
        x1, y1 = (event.x - 1), (event.y - 1)
        x2, y2 = (event.x + 1), (event.y + 1)
        canvas.create_oval(x1, y1, x2, y2, fill="black", width=0)

    canvas = Canvas(new_window, bg="white")
    canvas.pack(expand=YES, fill=BOTH)
    canvas.bind("<B1-Motion>", paint)

    menuBar = Menu(new_window)
    new_window.config(menu=menuBar)
    options = Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label="Options", menu=options)
    options.add_command(label="Background Color", command=lambda : canvas.config(bg=colorchooser.askcolor()[1]))
    options.add_command(label="Save", command=save_file)
    options.add_command(label="Clear", command=lambda: canvas.delete("all"))
    options.add_separator()
    options.add_command(label="Exit", command=new_window.destroy)
    
    message = Label(new_window, text="Press and drag the mouse to draw.", font=("Consolas", 15, "bold"))
    message.pack()

def exit_editor():
    window.destroy()

window = Tk()
window.title("Notepad editor")

icon = PhotoImage(file="img\\note.png")
window.iconphoto(True, icon)

file = None
window_width = 500
window_height = 500
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

font_name = StringVar(window)
font_name.set("Consolas")
font_size = StringVar(window)
font_size.set("16")

text_area = Text(window, font=(font_name.get(), int(font_size.get())))

scroll_bar = Scrollbar(text_area)
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
text_area.grid(sticky=N + E + S + W)
scroll_bar.pack(side=RIGHT, fill=Y)
text_area.config(yscrollcommand=scroll_bar.set)

frame = Frame(window)
frame.grid() 

color_button = Button(frame, text="Color", command=change_color)
color_button.grid(row=0, column=0)

font_box = OptionMenu(frame, font_name, *font.families(), command=change_font)
font_box.grid(row=0, column=1)

size_box = Spinbox(frame, from_=1, to=100, textvariable=font_size, command=change_font)
size_box.grid(row=0, column=2)

menu_bar = Menu(window)
window.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)   
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_editor)

edit_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Background Color", command=lambda: text_area.config(bg=colorchooser.askcolor()[1]))
edit_menu.add_command(label="Cut", command=cut)
edit_menu.add_command(label="Copy", command=copy)
edit_menu.add_command(label="Paste", command=paste)

style_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Style", menu=style_menu)
style_menu.add_command(label="Regular", command=lambda: text_area.config(font=(font_name.get(), int(font_size.get()))))
style_menu.add_command(label="Bold", command=lambda: text_area.config(font=(font_name.get(), int(font_size.get()), "bold")))
style_menu.add_command(label="Italic", command=lambda: text_area.config(font=(font_name.get(), int(font_size.get()), "italic")))
style_menu.add_command(label="Bold Italic", command=lambda: text_area.config(font=(font_name.get(), int(font_size.get()), "bold italic")))
style_menu.add_command(label="Underline", command=lambda: text_area.config(font=(font_name.get(), int(font_size.get()), "underline")))
style_menu.add_command(label="Overstrike", command=lambda: text_area.config(font=(font_name.get(), int(font_size.get()), "overstrike")))

drawing_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Drawing", menu=drawing_menu)
drawing_menu.add_command(label="Drawing Mode", command=create_new_window)

help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About", command=about)

window.mainloop()