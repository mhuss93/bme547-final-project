# BME547 Final Project
# Katrina Barth, Minhaj Hussain, and Iakov Rachinsky
# GUI Modules

from tkinter import *  # Brings in higher level tools
from tkinter import ttk  # Themed packages
from tkinter import filedialog
from PIL import ImageTk, Image
from pathlib import Path
import io
import base64
import io
import json
import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from matplotlib.pyplot import imread, imshow, show, subplot, title
from matplotlib.pyplot import get_cmap, hist
import requests
from flask import Flask, jsonify, request
import os

# Global variables
url = 'http://vcm-8935.vm.duke.edu:5000'
#url = 'http://127.0.0.1:5000'
multi_file = 0
userID = ''
mockDB = {}


def main_window():
    """
    Opens the main window of the GUI. From this window,
    the user enters their ID, a file or folder from where
    they want to upload images, the image processing
    method they wish to apply, and a button to submit the
    new images or view images already in the database.

    :params: nothing
    :returns: nothing
    """
    root = Tk()
    root.title("Image Processor")
    root.grid_rowconfigure(10, weight=3)
    # Title message
    welcome_msg = ttk.Label(root, text="Welcome to the image processor!",
                            font=(20))
    welcome_msg.grid(column=0, row=0, columnspan=4, pady=15)

    # Asking for user ID
    def post_userID():
        """
        Function tied to button to create a new user or recognize
        an existing user in the database.

        :params: nothing
        :returns: nothing
        """
        global userID
        userID = userID_box.get()
        mockDB["user_id"] = userID
        requests.post(url + "/api/register_user", json=mockDB)
        pass
    userID_lbl = ttk.Label(root, text="Enter User ID:")
    userID_lbl.grid(column=0, row=1, padx=5, pady=5, sticky=E)
    userID = StringVar()
    userID_box = ttk.Entry(root, textvariable=userID)
    userID_box.config(width=50)
    userID_box.grid(column=1, row=1, padx=5, pady=5, columnspan=2)
    userID_btn = ttk.Button(root, text="Enter ID", command=post_userID)
    userID_btn.grid(column=3, row=1, padx=5, pady=5)

    # Labels, boxes, and buttons for image file selection
    def ask_file():
        """
        Clear file adress box and open file dialog window to
        choose image for upload.

        :params: nothing
        :returns: nothing
        """
        open_file_box.delete(0, END)
        open_folder_box.delete(0, END)
        file_adrs = filedialog.askopenfilename()
        open_file_box.insert(0, file_adrs)
        pass
    open_file_lbl = ttk.Label(root,
                              text="Select ONE image file for processing:")
    open_file_lbl.grid(column=0, row=2, pady=5, padx=10)
    file_adrs = StringVar()
    open_file_box = ttk.Entry(root, textvariable=file_adrs)
    open_file_box.config(width=50)
    open_file_box.grid(column=1, row=2, padx=5, columnspan=2)
    browse_btn = ttk.Button(root, text='Browse', command=ask_file)
    browse_btn.grid(column=3, row=2)

    # Opening folder of files
    def ask_folder():
        """
        Clear folder adress box and open folder dialog window to
        choose images for upload.

        :params: nothing
        :returns: nothing
        """
        open_file_box.delete(0, END)
        open_folder_box.delete(0, END)
        folder_adrs = filedialog.askdirectory()
        open_folder_box.insert(0, folder_adrs)
        global multi_file
        multi_file = 1
        pass
    lbl = "OR select folder of images for processing:"
    open_folder_lbl = ttk.Label(root, text=lbl)
    open_folder_lbl.grid(column=0, row=3, pady=5, padx=10)
    folder_adrs = StringVar()
    open_folder_box = ttk.Entry(root, textvariable=folder_adrs)
    open_folder_box.config(width=50)
    open_folder_box.grid(column=1, row=3, padx=5, columnspan=2)
    browse_btn2 = ttk.Button(root, text='Browse', command=ask_folder)
    browse_btn2.grid(column=3, row=3)
    # Frame and radio buttons to choose image processing method
    proc_frm = ttk.Frame(root, borderwidth=1, relief=GROOVE)
    proc_frm.grid(column=0, row=5, pady=5, ipady=5)
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
                             value='Contrast')
    proc_2.grid(column=0, row=2, sticky=W, padx=20)
    proc_3 = ttk.Radiobutton(proc_frm, text="Log Compression",
                             variable=proc_choice,
                             value='Log')
    proc_3.grid(column=0, row=3, sticky=W, padx=20)
    proc_4 = ttk.Radiobutton(proc_frm, text="Reverse Video",
                             variable=proc_choice,
                             value='Reverse')
    proc_4.grid(column=0, row=4, sticky=W, padx=20)

    # Function for pulling file name out of file path
    def get_file_name(img_path):
        """
        Extract the file name out of the file path.

        :param img_path: file path to image
        :type img_path: string
        :return file_name: name of the image file
        :type file_name: string
        """
        file_adrs_str = img_path
        file_name = ""
        fas = file_adrs_str
        for x in range(len(file_adrs_str)):
            if file_adrs_str[x] == '.':
                for n in range(len(file_adrs_str)):
                    if fas[x-n-1] != '/' and fas[x-n-1] != '\\':
                        file_name = file_name + file_adrs_str[x-n-1]
                    else:
                        break
        file_name = file_name[::-1]
        return file_name

    def get_file_type(img_path):
        """
        Extract the file type out of the file path.

        :param img_path: file path to image
        :type img_path: string
        :return file_name: file type of the image file
        :type file_name: string
        """
        file_adrs_str = img_path
        file_type = ""
        for x in range(len(file_adrs_str)):
            if file_adrs_str[x] == '.':
                for n in range(len(file_adrs_str)-x-1):
                    file_type = file_type + file_adrs_str[x+n+1]
        return file_type

    # Button to send image to server for processing and open up next window
    def img_proc():
        """
        Saving image information into a local dictionary, encoding
        the image file, and sending both to the server for
        processing. The next window is then opened.

        :params: nothing
        :returns: nothing
        """
        if multi_file == 0:
            proc = proc_choice.get()
            img_path = open_file_box.get()
            with open(img_path, "rb") as img_file:
                b64_bytes = base64.b64encode(img_file.read())
            b64_string = str(b64_bytes, encoding='utf-8')
            file_name = get_file_name(img_path)
            file_type = get_file_type(img_path)
            mockDB["filename"] = file_name
            mockDB["extension"] = file_type
            mockDB["method"] = proc
            mockDB["original_image"] = b64_string
            post_adrs = url + "/api/upload_user_image"
            requests.post(post_adrs, json=mockDB)
            window2()
        else:
            files = []
            folder_path = open_folder_box.get()
            for r, d, f in os.walk(folder_path):
                for file in f:
                    files.append(os.path.join(r, file))
            for f in files:
                proc = proc_choice.get()
                img_path = f
                with open(img_path, "rb") as img_file:
                    b64_bytes = base64.b64encode(img_file.read())
                b64_string = str(b64_bytes, encoding='utf-8')
                file_name = get_file_name(img_path)
                file_type = get_file_type(img_path)
                mockDB["filename"] = file_name
                mockDB["extension"] = file_type
                mockDB["method"] = proc
                mockDB["original_image"] = b64_string
                post_adrs = url + "/api/upload_user_image"
                requests.post(post_adrs, json=mockDB)
            window2()
            pass
    proc_btn = ttk.Button(root, text="Process my image(s)",
                          command=img_proc)
    proc_btn.grid(column=1, row=5, columnspan=3, pady=10)
    look_ahead = ttk.Button(root, text="OR see previously uploaded images",
                            command=window2)
    look_ahead.grid(column=1, row=6, columnspan=3, pady=5, sticky=N)
    root.mainloop()
    return


def window2():
    """
    Window showing the original and processed images. There is a
    drop down menu to display other pairs of image files, and
    metadata is shown for each pair. The save file type is selected
    and the processed image file can be saved.

    :params: nothing
    :returns: nothing
    """
    window2 = Toplevel()
    window2.title("Processed Image Viewer")
    # In-window global variables
    img1_array = np.empty([2, 2])
    img2_array = np.empty([2, 2])
    # Get of file names and extensions
    userID_dic = {
                  "user_id": userID
                  }
    post_adrs = url + "/api/user_metadata"
    r = requests.post(post_adrs, json=userID_dic)
    meta_dic = r.json()

    file_names = meta_dic["filenames"]
    extensions = meta_dic["extension"]
    proc_file_names = meta_dic["proc_filenames"]
    proc_extensions = meta_dic["proc_extensions"]
    methods = meta_dic["proc_types"]
    proc_time_list = meta_dic["proc_times"]
    processedAt_list = meta_dic["proc_processedAt"]
    proc_data = list(zip(proc_file_names, proc_extensions, methods,
                         proc_time_list, processedAt_list))
    # Drop down menu to select file to view
    drop_lbl = ttk.Label(window2, text='Select Image to View:')
    drop_lbl.grid(column=0, row=0, columnspan=2, pady=5, sticky=E)

    def method_list_to_string(method_list):
        """
        Convert a list of image processing methods applied to an image into
        a single string.
        
        :param method_list: List of methods.
        :type method_list: list
        :return: String of methods separated by whitespace.
        :rtype: str
        """
        return ''.join(method_list)

    variable = StringVar(window2)
    variable.set(file_names[0])

    variable_method = StringVar(window2)
    variable_method.set(method_list_to_string(methods[0]))

    variable_ext = StringVar(window2)
    variable_ext.set(extensions[0])

    def get_method_options(filename, extension):
        """
        Get list of valid methods given filename and extension.
        
        :param filename: Filename.
        :type filename: str
        :param extension: Extension.
        :type extension: str
        :return: Processing methods that have been applied to the image.
        :rtype: list
        """
        options = [i[2] for i in proc_data
                   if (i[0] == filename and i[1] == extension)]
        return options

    def get_ext_options(filename):
        """
        Get list of valid extensions given filename.
        
        :param filename: Filename.
        :type filename: str
        :return: Extensions of previously uploaded files sharing the filename.
        :rtype: list
        """
        options = [i[1] for i in zip(file_names, extensions)
                   if i[0] == filename]
        return options

    method_options = get_method_options(file_names[0], extensions[0])
    method_options = [method_list_to_string(i) for i in method_options]
    drop_menu_method = OptionMenu(window2, variable_method, *method_options)
    drop_menu_method.grid(column=4, row=0, pady=5, padx=10)

    def update_method_options(extension):
        """
        Update the dropdown method list given the selected
        filename and extension.
        
        :param extension: Extension.
        :type extension: str
        """
        menu = drop_menu_method["menu"]
        menu.delete(0, "end")
        options = get_method_options(variable.get(), extension)
        options = [method_list_to_string(i) for i in options]
        for string in options:
            menu.add_command(
                label=string, 
                command=lambda value=string: variable_method.set(value)
            )
        variable_method.set(options[0])

    ext_options = get_ext_options(file_names[0])
    drop_menu_ext = OptionMenu(window2, variable_ext, *ext_options,
                               command=update_method_options)
    drop_menu_ext.grid(column=3, row=0, pady=5, padx=10)

    def update_ext_options(filename):
        """
        Update the dropdown extension list given the selected filename.
        
        :param filename: Filename.
        :type extension: str
        """
        menu = drop_menu_ext["menu"]
        menu.delete(0, "end")
        options = get_ext_options(variable.get())
        for string in options:
            menu.add_command(
                label=string, 
                command=lambda value=string: variable_ext.set(value)
            )
        variable_ext.set(options[0])
        update_method_options(variable_ext.get())

    unique_filenames = list(set(file_names))
    drop_menu = OptionMenu(window2, variable, *unique_filenames,
                           command=update_ext_options)
    drop_menu.grid(column=2, row=0, pady=5, padx=10)


    # Frame for metadata
    data_frm = ttk.Frame(window2, borderwidth=1, relief=GROOVE,
                         width=250, height=95)
    data_frm.grid(column=5, row=2, columnspan=2, pady=5, padx=5, sticky=N)
    data_frm.grid_propagate(0)
    time = StringVar()
    time_proc = StringVar()
    size_var = StringVar()
    time.set("Time of upload: ")
    time_proc.set("Time for processing: ")
    size_var.set("Image Size (pixels): ")
    timestamp_lbl = ttk.Label(data_frm, textvariable=time)
    timestamp_lbl.grid(column=0, row=0, pady=5, sticky=W)
    proctime_lbl = ttk.Label(data_frm, textvariable=time_proc)
    proctime_lbl.grid(column=0, row=1, pady=5, sticky=W)
    size_lbl = ttk.Label(data_frm, textvariable=size_var)
    size_lbl.grid(column=0, row=2, pady=5, sticky=W)
    # Frame and Label for Original Image
    img1_lbl = ttk.Label(window2, text="Original Image",
                         font='Arial 10 bold')
    img1_lbl.grid(column=0, row=1, columnspan=4, pady=5)
    img1_frm = ttk.Frame(window2, borderwidth=1,
                         width=380, height=380)
    img1_frm.grid(column=0, row=2, columnspan=4, rowspan=2, pady=5,
                  padx=5, ipady=5)
    img1_frm.grid_propagate(0)
    # Frame and Label for Processed Image
    img2_lbl = ttk.Label(window2, text="Processed Image",
                         font='Arial 10 bold')
    img2_lbl.grid(column=4, row=1, pady=5)
    img2_frm = ttk.Frame(window2, borderwidth=1,
                         width=380, height=380)
    img2_frm.grid(column=4, row=2, rowspan=2, pady=5, padx=5, ipady=5)
    img2_frm.grid_propagate(0)

    def get_up_img(dic):
        """
        Requests an already uploaded image from the server and decodes
        this image for use in the gui.

        :param dic: A dictionary of the file the user wants to get
        from the server
        :type dic: Dictionary (JSON format)
        :return img1_array: Array of RGB values for the original image
        :type img1_array: Array
        """
        dic_short = {
                     "user_id": userID,
                     "filename": dic['filename'],
                     "extension": dic['extension']
                     }
        r = requests.post(url + "/api/get_uploaded_image",
                          json=dic_short)
        img_dict = r.json()
        b64_string = img_dict['image']
        img_bytes = base64.b64decode(b64_string)
        img_buf = io.BytesIO(img_bytes)
        img1_array = mpimg.imread(img_buf,
                                  format=dic_short['extension'])
        return img1_array
    if 'filename' in mockDB:
        img1_array = get_up_img(mockDB)
    else:
        feed_dict = {
            'user_id': userID,
            'filename': file_names[0],
            'extension': extensions[0],
            'method': methods[0]
        }
        img1_array = get_up_img(feed_dict)
    img1_obj = Image.fromarray(img1_array)
    size = (375, 375)
    img1_obj.thumbnail(size)
    img1 = ImageTk.PhotoImage(img1_obj)
    img1_space = ttk.Label(img1_frm, image=img1)
    img1_space.grid(column=0, row=0)

    def get_proc_img(dic):
        """
        Requests the processed image from the server and decodes
        this image for use in the gui.

        :param dic: A dictionary of the file the user wants to get
        from the server
        :type dic: Dictionary (JSON format)
        :return img2_array: Array of RGB values for the processed image
        :type img2_array: Array
        """
        dic_short = {
                     "user_id": userID,
                     "filename": dic['filename'],
                     "extension": dic['extension'],
                     "method": dic['method']
                     }
        r = requests.post(url + "/api/get_processed_image",
                          json=dic_short)
        img_dict = r.json()
        b64_string = img_dict['img']
        img_bytes = base64.b64decode(b64_string)
        img_buf = io.BytesIO(img_bytes)
        img2_array = mpimg.imread(img_buf,
                                  format=dic_short['extension'])
        return img2_array

    if 'filename' in mockDB:
        img2_array = get_proc_img(mockDB)
    else:
        feed_dict = {
            'user_id': userID,
            'filename': file_names[0],
            'extension': extensions[0],
            'method': methods[0]
        }
        img2_array = get_proc_img(feed_dict)
    img2_obj = Image.fromarray(img2_array)
    size = (375, 375)
    img2_obj.thumbnail(size)
    img2 = ImageTk.PhotoImage(img2_obj)
    img2_space = ttk.Label(img2_frm, image=img2)
    img2_space.grid(column=0, row=0)

    # Refresh button
    def refresh_img():
        """
        Replaces the image and metadata displays in the GUI with
        the newly selected files.

        :params: none
        :returns: none
        """
        global img1_array
        global img2_array
  
        """
        for i in range(len(file_names)):
            if file_names[i] == variable.get():
                file_name = file_names[i]
                extension = extensions[i]
                method = methods[i]
                proc_time = proc_time_list[i]
                procAt = processedAt_list[i]
        """
        file_name = variable.get()
        extension = variable_ext.get()
        method = variable_method.get().split()
        proc_time = [i[3] for i in proc_data
                           if (i[0] == file_name and
                               i[1] == extension and
                               i[2] == method)][0]
        procAt = [i[4] for i in proc_data
                           if (i[0] == file_name and
                               i[1] == extension and
                               i[2] == method)][0]

        dic1 = {
               "user_id": userID,
               "filename": file_name,
               "extension": extension,
                }
        dic2 = {
                "user_id": userID,
                "filename": file_name,
                "extension": extension,
                "method": method
                }
        img1_array = get_up_img(dic1)
        img1_obj = Image.fromarray(img1_array)
        size = (375, 375)
        img1_obj.thumbnail(size)
        img1 = ImageTk.PhotoImage(img1_obj)
        img1_space.configure(image=img1)
        img1_space.image = img1
        img2_array = get_proc_img(dic2)
        img2_obj = Image.fromarray(img2_array)
        size = (375, 375)
        img2_obj.thumbnail(size)
        img2 = ImageTk.PhotoImage(img2_obj)
        img2_space.configure(image=img2)
        img2_space.image = img2
        size_val = np.shape(img2_array)
        size_x = size_val[0]
        size_y = size_val[1]
        time.set("Time for Processing: " + str(proc_time))
        time_proc.set("Time of Upload: " + str(procAt))
        dimensions = str(size_x) + " x " + str(size_y)
        size_var.set("Image Size (pixels): " + dimensions)
        pass
    refresh_img()
    refresh_btn = ttk.Button(window2, text='Refresh Image',
                             command=refresh_img)
    refresh_btn.grid(column=5, row=0, pady=5, sticky=W)
    # Button to open histogram window
    window2.grid_rowconfigure(3, weight=1)
    histo_btn = ttk.Button(window2,
                           text='Show Color Histograms',
                           command=lambda: plt_histo(img1_array, img2_array))
    histo_btn.grid(column=5, row=3, pady=10, columnspan=2, sticky=N)
    # Choose the save file type, with JPEG as default
    file_type = StringVar()
    file_type_lbl = ttk.Label(window2,
                              text="Select save file type:")
    file_type_lbl.grid(column=0, row=4, sticky=E, pady=5, padx=5)
    jpg_box = ttk.Radiobutton(window2, text='JPEG',
                              variable=file_type, value='.jpg')
    jpg_box.grid(column=1, row=4, padx=15, sticky=W)
    png_box = ttk.Radiobutton(window2, text='PNG',
                              variable=file_type, value='.png')
    png_box.grid(column=2, row=4, padx=15, sticky=W)
    tiff_box = ttk.Radiobutton(window2, text='TIFF',
                               variable=file_type, value='.tiff')
    tiff_box.grid(column=3, row=4, padx=15, sticky=W)
    file_type.set('.jpg')

    # Choosing a save location for the processed image
    def ask_file():
        """
        Opens file dialog to get file save location from the user.

        :params: none
        :returns: none
        """
        save_file_adrs = filedialog.asksaveasfilename()
        save_file_box.insert(0, save_file_adrs)
        window2.lift()
        pass

    # Saving the file
    def save_file():
        """
        Saves the image file on the computer at the specified location.

        :params: none
        :returns: none
        """
        file_path = save_file_adrs.get() + file_type.get()
        img2_obj.save(file_path)
        pass
    save_file_lbl = ttk.Label(window2, text="Save processed image as:")
    save_file_lbl.grid(column=0, row=5, sticky=E, pady=5, padx=5)
    save_file_adrs = StringVar()
    save_file_box = ttk.Entry(window2, textvariable=save_file_adrs)
    save_file_box.grid(column=1, row=5, columnspan=4, padx=5)
    save_file_box.config(width=105)
    browse_btn = ttk.Button(window2, text='Browse', command=ask_file)
    browse_btn.grid(column=5, row=5, sticky=W)
    save_btn = ttk.Button(window2, text="Save Processed Image",
                          command=save_file)
    save_btn.grid(column=6, row=5, pady=5, padx=5)
    # Close window button
    close_btn = ttk.Button(window2, text="Close Processed Image Viewer",
                           command=window2.destroy)
    close_btn.grid(column=0, row=6, columnspan=7, pady=10)
    window2.mainloop()
    return


def plt_histo(img1_array, img2_array):
    """
    Makes matplot lib histograms of the RGB values of the original
    and processed images.

    :param img1_array: Array of RGB values for original image
    :type img1_array: Array
    :param img2_array: Array of RGB values for processed image
    :type img2_array: Array
    """
    # Generate arrays of color values from image files
    img1_shape = img1_array.shape
    img2_shape = img2_array.shape
    r1 = []
    g1 = []
    b1 = []
    r2 = []
    g2 = []
    b2 = []
    for i in range(img1_shape[0]):
        for j in range(img1_shape[1]):
            r1.append(img1_array[i, j, 0])
            g1.append(img1_array[i, j, 1])
            b1.append(img1_array[i, j, 2])
    for i in range(img2_shape[0]):
        for j in range(img2_shape[1]):
            r2.append(img2_array[i, j, 0])
            g2.append(img2_array[i, j, 1])
            b2.append(img2_array[i, j, 2])
    # Plot Histogram for original image
    plt.figure(1)
    plt.suptitle('Original Image')
    subplot(311)
    hist(r1, 256, range=(0, 256), color='red')
    title('Red')
    subplot(312)
    hist(g1, 256, range=(0, 256), color='green')
    title('Green')
    subplot(313)
    hist(b1, 256, range=(0, 256), color='blue')
    title('Blue')
    plt.tight_layout()
    plt.subplots_adjust(top=0.88, right=0.93)
    plt.subplots_adjust(top=0.88)
    # Plot Histogram for processed image
    plt.figure(2)
    plt.suptitle('Processed Image')
    subplot(311)
    hist(r2, 256, range=(0, 256), color='red')
    title('Red')
    subplot(312)
    hist(g2, 256, range=(0, 256), color='green')
    title('Green')
    subplot(313)
    hist(b2, 256, range=(0, 256), color='blue')
    title('Blue')
    plt.tight_layout()
    plt.subplots_adjust(top=0.88, right=0.93)
    plt.show()
    return


if __name__ == '__main__':
    main_window()
