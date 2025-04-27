import cv2
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import os
from datetime import datetime

class WebcamApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Advanced Webcam Capture")
        
        # Initialize webcam
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self.show_error("Could not open webcam!")
            return

        # Default save location
        self.save_dir = os.path.expanduser("~")  # Default to user's home directory
        self.img_format = ".jpg"  # Default format
        
        # GUI Elements
        self.create_widgets()
        
        # Start webcam preview
        self.running = True
        self.update_preview()

    def create_widgets(self):
        # Preview frame
        self.label = ttk.Label(self.window)
        self.label.pack(pady=10)
        
        # Control buttons frame
        btn_frame = ttk.Frame(self.window)
        btn_frame.pack(pady=10)
        
        # Capture buttons
        ttk.Button(btn_frame, text="Quick Save", command=self.quick_save).grid(row=0, column=0, padx=5)
        ttk.Button(btn_frame, text="Save As...", command=self.save_as).grid(row=0, column=1, padx=5)
        
        # Format selection
        format_frame = ttk.LabelFrame(self.window, text="Image Format")
        format_frame.pack(pady=5)
        self.format_var = tk.StringVar(value=".jpg")
        ttk.Radiobutton(format_frame, text="JPG", variable=self.format_var, value=".jpg").pack(side=tk.LEFT)
        ttk.Radiobutton(format_frame, text="PNG", variable=self.format_var, value=".png").pack(side=tk.LEFT)
        ttk.Radiobutton(format_frame, text="BMP", variable=self.format_var, value=".bmp").pack(side=tk.LEFT)
        
        # Directory selection
        dir_frame = ttk.Frame(self.window)
        dir_frame.pack(pady=5)
        ttk.Button(dir_frame, text="Change Save Location", command=self.change_dir).pack(side=tk.LEFT)
        self.dir_label = ttk.Label(dir_frame, text=f"Save to: {self.save_dir}")
        self.dir_label.pack(side=tk.LEFT, padx=5)
        
        # Exit button
        ttk.Button(self.window, text="Exit", command=self.close_app).pack(pady=10)

    def update_preview(self):
        if not self.running:
            return
            
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)
        
        self.window.after(15, self.update_preview)

    def quick_save(self):
        """Save with timestamp filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"webcam_{timestamp}{self.format_var.get()}"
        self.save_image(filename)
        messagebox.showinfo("Saved", f"Image saved as:\n{filename}")

    def save_as(self):
        """Save with custom filename"""
        filetypes = [
            ("JPEG files", "*.jpg"),
            ("PNG files", "*.png"),
            ("BMP files", "*.bmp"),
            ("All files", "*.*")
        ]
        filename = filedialog.asksaveasfilename(
            initialdir=self.save_dir,
            filetypes=filetypes,
            defaultextension=self.format_var.get()
        )
        if filename:
            self.save_image(filename)

    def save_image(self, filename):
        """Core save function"""
        ret, frame = self.cap.read()
        if ret:
            full_path = os.path.join(self.save_dir, filename)
            cv2.imwrite(full_path, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def change_dir(self):
        """Change save directory"""
        new_dir = filedialog.askdirectory(initialdir=self.save_dir)
        if new_dir:
            self.save_dir = new_dir
            self.dir_label.config(text=f"Save to: {self.save_dir}")

    def close_app(self):
        self.running = False
        self.cap.release()
        self.window.destroy()

    def show_error(self, message):
        messagebox.showerror("Error", message)
        self.window.destroy()

# Run the application
root = tk.Tk()
app = WebcamApp(root)
root.protocol("WM_DELETE_WINDOW", app.close_app)
root.mainloop()