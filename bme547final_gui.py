# BME547 Final Project
# Katrina Barth, Minhaj Hussain, and Iakov Rachinsky
# GUI Modules

from tkinter import *  # Brings in higher level tools
from tkinter import ttk  # Themed packages
from tkinter import filedialog
from PIL import ImageTk, Image


def main_window():
    root = Tk()
    root.title("Image Processor")
    root.grid_rowconfigure(9, weight=3)
    # Title message
    welcome_msg = ttk.Label(root, text="Welcome to the image processor!",
                            font=(20))
    welcome_msg.grid(column=0, row=0, columnspan=4, pady=15)

    # Labels, boxes, and buttons for image file selection
    def open_file():
        open_file_address = filedialog.askopenfilename()
        open_file_box.insert(0, open_file_address)
        pass
    open_file_lbl = ttk.Label(root,
                              text="Select image file(s) for processing:")
    open_file_lbl.grid(column=0, row=1, pady=5, padx=10)
    open_file_adrs = StringVar()
    open_file_box = ttk.Entry(root, textvariable=open_file_adrs)
    open_file_box.config(width=50)
    open_file_box.grid(column=1, row=1, padx=5, columnspan=2)
    browse_btn = ttk.Button(root, text='Browse', command=open_file)
    browse_btn.grid(column=3, row=1)
    # Frame for Image or Message Display
    img_frm = ttk.Frame(root, borderwidth=1, relief=GROOVE,
                        width=380, height=380)
    img_frm.grid(column=1, row=2, columnspan=3, rowspan=8, pady=5)
    img_frm.grid_propagate(0)
    img_frm.grid_rowconfigure(0, weight=1)  # Centering message in frame
    img_frm.grid_rowconfigure(2, weight=1)
    img_frm.grid_columnconfigure(0, weight=1)
    img_frm.grid_columnconfigure(2, weight=1)
    img_msg = ttk.Label(img_frm, text="No image file(s) selected")
    img_msg.grid(column=0, row=1, columnspan=3)
    # Frame and radio buttons to choose image processing method
    proc_frm = ttk.Frame(root, borderwidth=1, relief=GROOVE)
    proc_frm.grid(column=0, row=3, pady=5, ipady=5)
    proc_lbl = ttk.Label(proc_frm, text="Select image processing method")
    proc_lbl.grid(column=0, row=0, pady=5)
    proc_choice = StringVar()
    proc_choice.set('Hist')
    proc_1 = ttk.Radiobutton(proc_frm, text="Histogram Equalization",
                             variable=proc_choice,
                             value='Hist')
    proc_1.grid(column=0, row=1, sticky=W, padx=20)
    proc_2 = ttk.Radiobutton(proc_frm, text="Contrast Stretching",
                             variable=proc_choice,
                             value='Stretch')
    proc_2.grid(column=0, row=2, sticky=W, padx=20)
    proc_3 = ttk.Radiobutton(proc_frm, text="Log Compression",
                             variable=proc_choice,
                             value='Compress')
    proc_3.grid(column=0, row=3, sticky=W, padx=20)
    proc_4 = ttk.Radiobutton(proc_frm, text="Reverse Video",
                             variable=proc_choice,
                             value='Reverse')
    proc_4.grid(column=0, row=4, sticky=W, padx=20)

    # Button to end image to server for processing and open up next window
    def img_proc():
        proc = proc_choice.get()
        print(proc)
        window2()
    proc_btn = ttk.Button(root, text="Process my image(s)",
                          command=img_proc)
    proc_btn.grid(column=0, row=9, sticky=N, pady=10)
    root.mainloop()
    return


def window2():
    window2 = Toplevel()
    window2.title("Processed Image")
    # Button to open window displaying original and processed image
    compare_btn = ttk.Button(window2, text='Compare to Original')
    compare_btn.grid(column=3, row=1, columnspan=2, pady=5)
    # Button to open window displaying histogram of colors
    histogram_btn = ttk.Button(window2,
                               text='Histogram of Color Intensities')
    histogram_btn.grid(column=3, row=2, columnspan=2, pady=5)
    # Metadata
    timestamp_lbl = ttk.Label(window2, text="Time of Upload:")
    timestamp_lbl.grid(column=3, row=3, pady=5, columnspan=2, sticky=W)
    proctime_lbl = ttk.Label(window2, text="Time for Processing:")
    proctime_lbl.grid(column=3, row=4, pady=5, columnspan=2, sticky=W)
    size_lbl = ttk.Label(window2, text="Image Size:")
    size_lbl.grid(column=3, row=5, pady=5, columnspan=2, sticky=W)
    # Choose the save file type, with JPEG as default
    file_type = StringVar()
    file_type_lbl = ttk.Label(window2,
                              text="Select save file type:")
    file_type_lbl.grid(column=0, row=7, sticky=W, pady=5)
    jpg_box = ttk.Radiobutton(window2, text='JPEG',
                              variable=file_type, value='.jpg')
    jpg_box.grid(column=1, row=7, padx=15, sticky=W)
    png_box = ttk.Radiobutton(window2, text='PNG',
                              variable=file_type, value='.png')
    png_box.grid(column=2, row=7, padx=15, sticky=W)
    tiff_box = ttk.Radiobutton(window2, text='TIFF',
                               variable=file_type, value='.tiff')
    tiff_box.grid(column=3, row=7, padx=15, sticky=W)
    file_type.set('.jpg')
    # Choose where to save the processed image
    save_file_lbl = ttk.Label(window2, text="Select save location:")
    save_file_lbl.grid(column=0, row=8, sticky=E, pady=5)
    save_file_adrs = StringVar()
    save_file_box = ttk.Entry(window2, textvariable=save_file_adrs)
    save_file_box.grid(column=1, row=8, columnspan=2, padx=5)

    def save_file():
        save_file_adrs = filedialog.askdirectory()
        save_file_box.insert(0, save_file_adrs)
        pass
    browse_btn = ttk.Button(window2, text='Browse', command=save_file)
    browse_btn.grid(column=3, row=8, sticky=W)
    # Save image button
    save_btn = ttk.Button(window2, text="Save Processed Image")
    save_btn.grid(column=4, row=8, pady=5, padx=5)
    window2.mainloop()
    return


def compare_window():
    window3 = tk.Toplevel(window2)
    window3.title("Image Comparison")
    window3.geometry('400x300+100+100')


def histogram_window():
    window4 = Tk()
    window4.title("Histogram of Image Color")
    window4.geometry('400x300+100+100')


if __name__ == '__main__':
    main_window()
