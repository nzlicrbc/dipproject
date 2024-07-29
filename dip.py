import tkinter as tk
from tkinter import filedialog, messagebox
from rembg import remove
from PIL import Image, ImageTk, ImageOps
import cv2
import numpy as np
import io

# Function to remove background
def remove_background():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    try:
        input_image = Image.open(file_path)
        output_image = remove(input_image)
        display_images(input_image, output_image)
    except Exception as e:
        print(f"Error in remove_background: {e}")

# Function to crop image
def crop_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    try:
        image = Image.open(file_path)
        cropped_image = image.crop((50, 50, 200, 200))  # Example crop box
        display_images(image, cropped_image)
    except Exception as e:
        print(f"Error in crop_image: {e}")

# Function to convert image to grayscale
def grayscale_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    try:
        image = Image.open(file_path)
        grayscale_image = ImageOps.grayscale(image)
        display_images(image, grayscale_image)
    except Exception as e:
        print(f"Error in grayscale_image: {e}")

# Function to rotate image
def rotate_image():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    try:
        image = Image.open(file_path)
        rotated_image = image.rotate(90)  # Rotate 90 degrees
        display_images(image, rotated_image)
    except Exception as e:
        print(f"Error in rotate_image: {e}")

# Function to compare images
def compare_images():
    file_path1 = filedialog.askopenfilename(title="Select First Image")
    if not file_path1:
        return
    file_path2 = filedialog.askopenfilename(title="Select Second Image")
    if not file_path2:
        return
    try:
        img1 = Image.open(file_path1)
        img2 = Image.open(file_path2)
        display_images(img1, img2)

        img1_np = np.array(img1)
        img2_np = np.array(img2)
        if img1_np.shape == img2_np.shape:
            difference = cv2.subtract(img1_np, img2_np)
            b, g, r = cv2.split(difference)
            if cv2.countNonZero(b) == 0 and cv2.countNonZero(g) == 0 and cv2.countNonZero(r) == 0:
                messagebox.showinfo("Result", "The images are the same")
            else:
                messagebox.showinfo("Result", "The images are different")
        else:
            messagebox.showinfo("Result", "The images have different dimensions")
    except Exception as e:
        print(f"Error in compare_images: {e}")

# Function to display selected and output images
def display_images(selected_image, output_image):
    selected_image.thumbnail((150, 150))
    output_image.thumbnail((150, 150))

    selected_image_bytes = io.BytesIO()
    output_image_bytes = io.BytesIO()
    selected_image.save(selected_image_bytes, format="PNG")
    output_image.save(output_image_bytes, format="PNG")

    selected_photo = ImageTk.PhotoImage(data=selected_image_bytes.getvalue())
    output_photo = ImageTk.PhotoImage(data=output_image_bytes.getvalue())

    selected_image_label.config(image=selected_photo)
    output_image_label.config(image=output_photo)

    selected_image_label.image = selected_photo
    output_image_label.image = output_photo

    selected_image_label.grid(row=1, column=0, padx=10, pady=5)
    output_image_label.grid(row=1, column=1, columnspan=2, padx=10, pady=5)

# UI setup
root = tk.Tk()
root.title("Image Processing Application")

remove_bg_button = tk.Button(root, text="Remove Background", command=remove_background)
crop_button = tk.Button(root, text="Crop Image", command=crop_image)
grayscale_button = tk.Button(root, text="Convert to Grayscale", command=grayscale_image)
rotate_button = tk.Button(root, text="Rotate Image", command=rotate_image)
compare_button = tk.Button(root, text="Compare Images", command=compare_images)

remove_bg_button.grid(row=0, column=0, padx=10, pady=10)
crop_button.grid(row=0, column=1, padx=10, pady=10)
grayscale_button.grid(row=0, column=2, padx=10, pady=10)
rotate_button.grid(row=0, column=3, padx=10, pady=10)
compare_button.grid(row=0, column=4, padx=10, pady=10)

selected_image_label = tk.Label(root)
output_image_label = tk.Label(root)

root.mainloop()