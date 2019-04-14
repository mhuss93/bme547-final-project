# BME547 Final Project
# Katrina Barth, Minhaj Hussain, and Iakov Rachinsky
# GUI Modules

from tkinter import *  # Brings in higher level tools
from tkinter import ttk  # Themed packages


def start_window():
    root = Tk()
    root.title("Image Processor")

    welcome_message = ttk.Label(root, text="Welcome to the image processor.")
    welcome_message.grid(column=0, row=0, columnspan = 3)

    open_file_label = ttk.Label(root, text="Select image file(s) for processing:")
    open_file_label.grid(column=0, row=1, sticky=W)

    open_file_address = StringVar()
    open_file_box = ttk.Entry(root, textvariable=open_file_address)
    open_file_box.grid(column=1, row=1)

    processing_options_label = ttk.Label(root, text="Select image processing steps:")
    processing_options_label.grid(column=0, row=2, sticky=W)

    process_1var = StringVar()
    process_1var.set('+')
    process_1 = ttk.Checkbutton(root, text="Histogram Equalization", \
        variable=process_1var, onvalue='+', offvalue='-')
    process_1.grid(column=0, row=3, sticky=W)

    process_2var = StringVar()
    process_2var.set('-')
    process_2 = ttk.Checkbutton(root, text="Contrast Stretching", \
        variable=process_2var, onvalue='+', offvalue='-')
    process_2.grid(column=0, row=4, sticky=W)

    process_3var = StringVar()
    process_3var.set('-')
    process_3 = ttk.Checkbutton(root, text="Log Compression", \
        variable=process_3var, onvalue='+', offvalue='-')
    process_3.grid(column=0, row=5, sticky=W)

    process_4var = StringVar()
    process_4var.set('-')
    process_4 = ttk.Checkbutton(root, text="Reverse Video", \
        variable=process_4var, onvalue='+', offvalue='-')
    process_4.grid(column=0, row=6, sticky=W)

    def image_process():
        check1 = process_1var.get()
        if check1 == '+':
            print("Histogram Equalization")
        check2 = process_2var.get()
        if check2 == '+':
            print("Contrast Stretching")
        check3 = process_3var.get()
        if check3 == '+':
            print("Log Compression")
        check4 = process_4var.get()
        if check4 == '+':
            print("Reverse Video")
        pass


    process_btn = ttk.Button(root, text="Process my image(s)", command=image_process)
    process_btn.grid(column=0, row=7, columnspan=2)

    root.mainloop()
    return


if __name__=='__main__':
    start_window()