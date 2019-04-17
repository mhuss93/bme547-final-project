# BME547 Final Project
# Katrina Barth, Minhaj Hussain, and Iakov Rachinsky
# GUI Modules

from tkinter import *  # Brings in higher level tools
from tkinter import ttk  # Themed packages
from tkinter import filedialog
from PIL import ImageTk, Image


def start_window():
    root = Tk()
    root.title("Image Processor")
    # Title message for main GUI window
    welcome_message = ttk.Label(root, text="Welcome to the image processor.")
    welcome_message.grid(column=0, row=0, columnspan=3, pady=5)
    # Labels, boxes, and buttons for choosing an image file
    open_file_label = ttk.Label(root,
                                text="Select image file(s) for processing:")
    open_file_label.grid(column=0, row=1, sticky=W, pady=5)
    open_file_address = StringVar()
    open_file_box = ttk.Entry(root, textvariable=open_file_address)
    open_file_box.grid(column=1, row=1, padx=5)

    def open_file():
        open_file_address = filedialog.askopenfilename()
        open_file_box.insert(0, open_file_address)
        pass
    browse_button = ttk.Button(root, text='Browse', command=open_file)
    browse_button.grid(column=3, row=1)
    # Checkboxes to choose image processing methods
    processing_label = ttk.Label(root, text="Select image processing steps:")
    processing_label.grid(column=0, row=2, sticky=W, pady=5)
    process_1var = StringVar()
    process_1var.set('+')
    process_1 = ttk.Checkbutton(root, text="Histogram Equalization",
                                variable=process_1var,
                                onvalue='+', offvalue='-')
    process_1.grid(column=0, row=3, sticky=W)
    process_2var = StringVar()
    process_2var.set('-')
    process_2 = ttk.Checkbutton(root, text="Contrast Stretching",
                                variable=process_2var,
                                onvalue='+', offvalue='-')
    process_2.grid(column=0, row=4, sticky=W)
    process_3var = StringVar()
    process_3var.set('-')
    process_3 = ttk.Checkbutton(root, text="Log Compression",
                                variable=process_3var,
                                onvalue='+', offvalue='-')
    process_3.grid(column=0, row=5, sticky=W)
    process_4var = StringVar()
    process_4var.set('-')
    process_4 = ttk.Checkbutton(root, text="Reverse Video",
                                variable=process_4var,
                                onvalue='+', offvalue='-')
    process_4.grid(column=0, row=6, sticky=W)

    def image_process():
        print("File Location: {}".format(open_file_address.get()))
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
        processed_window()
    # Button to process image and open up next window
    process_btn = ttk.Button(root, text="Process my image(s)",
                             command=image_process)
    process_btn.grid(column=0, row=7, columnspan=3, pady=5)
    root.mainloop()
    return


def processed_window():
    window2 = Tk()
    window2.title("Processed Image")
    # Area where processed image from server will display
    processed_image_label = ttk.Label(window2, text="Processed Image:")
    processed_image_label.grid(column=0, row=0, sticky=W, pady=5)
    # image_frame1 = ttk.Frame(window2)
    # image_frame1.grid(column=0, row=1, padx=20, pady=50, rowspan=6)
    # img_obj = Image.open("Zoey.jpg")
    # processed_image = ImageTk.PhotoImage(img_obj)
    processed_image = PhotoImage(file="met.gif")
    processed_image_space = ttk.Label(window2, image=processed_image)
    processed_image_space.grid(column=0, row=1)
    # label['image'] = processed_image
    # image.grid(column=0, row=1, pady=5, padx=5)
    # Button to open window displaying original and processed image
    compare_button = ttk.Button(window2, text='Compare to Original')
    compare_button.grid(column=3, row=1, columnspan=2, pady=5)
    # Button to open window displaying histogram of colors
    histogram_button = ttk.Button(window2,
                                  text='Histogram of Color Intensities')
    histogram_button.grid(column=3, row=2, columnspan=2, pady=5)
    # Metadata
    timestamp_label = ttk.Label(window2, text="Time of Upload:")
    timestamp_label.grid(column=3, row=3, pady=5, columnspan=2, sticky=W)
    proctime_label = ttk.Label(window2, text="Time for Processing:")
    proctime_label.grid(column=3, row=4, pady=5, columnspan=2, sticky=W)
    size_label = ttk.Label(window2, text="Image Size:")
    size_label.grid(column=3, row=5, pady=5, columnspan=2, sticky=W)
    # Choose the save file type, with JPEG as default
    file_type = StringVar()
    file_type.set('.jpg')
    file_type_label = ttk.Label(window2,
                                text="Select save file type:")
    file_type_label.grid(column=0, row=7, sticky=W, pady=5)
    jpg_box = ttk.Radiobutton(window2, text='JPEG',
                              variable=file_type, value='.jpg')
    jpg_box.grid(column=1, row=7, padx=15, sticky=W)
    png_box = ttk.Radiobutton(window2, text='PNG',
                              variable=file_type, value='.png')
    png_box.grid(column=2, row=7, padx=15, sticky=W)
    tiff_box = ttk.Radiobutton(window2, text='TIFF',
                               variable=file_type, value='.tiff')
    tiff_box.grid(column=3, row=7, padx=15, sticky=W)
    # Choose where to save the processed image
    save_file_label = ttk.Label(window2, text="Select save location:")
    save_file_label.grid(column=0, row=8, sticky=E, pady=5)
    save_file_address = StringVar()
    save_file_box = ttk.Entry(window2, textvariable=save_file_address)
    save_file_box.grid(column=1, row=8, columnspan=2, padx=5)

    def save_file():
        save_file_address = filedialog.askdirectory()
        save_file_box.insert(0, save_file_address)
        pass
    browse_button = ttk.Button(window2, text='Browse', command=save_file)
    browse_button.grid(column=3, row=8, sticky=W)
    # Save image button
    save_button = ttk.Button(window2, text="Save Processed Image")
    save_button.grid(column=4, row=8, pady=5, padx=5)
    return


def compare_window():
    window3 = Tk()
    window3.title("Image Comparison")
    window3.geometry('400x300+100+100')


def histogram_window():
    window4 = Tk()
    window4.title("Histogram of Image Color")
    window4.geometry('400x300+100+100')


if __name__ == '__main__':
    start_window()
