# bme547-final-project
Image Processor Final Project (Spring 2019)

## Overview of Project and GUI functionality:
In this project we develop an image processing server. A client operates the server using a GUI
that allows to choose a picture or several picture of type .JPG, .PNG, or .TIFF from their hard drive.
This picture can then be uploaded to the server where it is stored in a database as an encoded RGB array.
The client has 4 option for processing the image: Histrogram Equalization (default), Contrast Stretching, Log Compression and Reverse Video. The processed image is stored on the server in the same encoded rgb array format, and is also sent back to the user. The user can compare the original and processed image visually in the GUI, as well as plot the color histograms of both images. 

## Guite for using GUI:
1. Browse - click browse to choose an image of folder of images to be processed
2. On left side of window, click a radio button of the process you want to have performed on your image.
3. Process Image - press this button to process the image(s)

-> A second window now pops up. It displays the original and processed image.

4. Display Histograms - pressing this button will display the histrograms for both images.
