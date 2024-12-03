import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
from PIL import Image, ImageTk
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='tkinter')

class ImageProcessingApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.image1_path = None
        self.image2_path = None

    def create_widgets(self):
        self.top_frame = tk.Frame(self, bg="#2b2b2b")
        self.top_frame.pack(fill="x", pady=10)

        self.title_label = tk.Label(self.top_frame, text="Image Processing App", bg="#2b2b2b", fg="#ffffff", font=("Helvetica", 16))
        self.title_label.pack(side="top", pady=10)

        self.buttons_frame = tk.Frame(self.top_frame, bg="#2b2b2b")
        self.buttons_frame.pack(fill="x")

        self.open_image1_button = tk.Button(self.buttons_frame, text="Изображение 1", bg="#333333", fg="#ffffff", width=20, height=2, command=self.open_image1)
        self.open_image1_button.pack(side="left", padx=10, pady=5)

        self.open_image2_button = tk.Button(self.buttons_frame, text="Изображение 2", bg="#333333", fg="#ffffff", width=20, height=2, command=self.open_image2)
        self.open_image2_button.pack(side="left", padx=10, pady=5)

        self.process_button = tk.Button(self.buttons_frame, text="Алгоритм работы", bg="#333333", fg="#ffffff", width=20, height=2, command=self.process)
        self.process_button.pack(side="left", padx=10, pady=5)

        self.save_button = tk.Button(self.buttons_frame, text="Сохранить", bg="#333333", fg="#ffffff", width=20, height=2, command=self.save_image)
        self.save_button.pack(side="left", padx=10, pady=5)

        self.image_frame = tk.Frame(self, bg="#2b2b2b")
        self.image_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.image_label = tk.Label(self.image_frame, bg="#2b2b2b")
        self.image_label.pack(expand=True)

    def open_image1(self):
        self.image1_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
        if self.image1_path:
            self.open_image1_button.config(text=os.path.basename(self.image1_path))

    def open_image2(self):
        self.image2_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg .jpeg .png .bmp")])
        if self.image2_path:
            self.open_image2_button.config(text=os.path.basename(self.image2_path))

    def process(self):
        if self.image1_path and self.image2_path:
            output_filename = os.path.basename(self.image1_path).split('.')[0] + '_output.jpg'
            output_path = os.path.join(os.getcwd(), output_filename)
            processed_image1 = self.process_image1(self.image1_path)
            processed_image2 = self.process_image2(self.image2_path)
            result_image = self.overlay_images(processed_image1, processed_image2)
            cv2.imwrite(output_path, result_image)
            self.display_image(output_path)

    def overlay_images(self, image1, image2):
        result_image = cv2.add(image1, image2)
        result_image = np.where(result_image > 255, 255, result_image).astype(np.uint8)
        return result_image

    def process_image1(self, image_path):
        image = cv2.imread(image_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        low_brightness_mask = gray_image < 25
        image[low_brightness_mask, 2] = np.clip(image[low_brightness_mask, 2] * 2, 0, 255)
        return image

    def process_image2(self, image_path):
        image = cv2.imread(image_path)
        result_image = np.zeros_like(image)
        for y in range(image.shape[0]):
            for x in range(image.shape[1]):
                r, g, b = image[y, x]
                if (r > 128) or (g > 128) or (b > 128):
                    result_image[y, x] = (255, 255, 255)
                else:
                    result_image[y, x] = (0, 0, 0)
        return result_image

    def display_image(self, image_path):
        image = Image.open(image_path)
        image.thumbnail((800, 800))
        photo = ImageTk.PhotoImage(image)
        self.image_label.config(image=photo)
        self.image_label.image = photo

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            os.rename(output_path, file_path)

root = tk.Tk()
root.title("Image Processing")
app = ImageProcessingApp(master=root)
app.mainloop()