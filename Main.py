#-------------------------------------------------------Module Imports--------------------------------------------------------------
import tkinter as tk
from tkinter import filedialog, Toplevel, ttk, Scale
from PIL import Image, ImageTk, ImageFilter, ImageEnhance

#----------------------------------------------------------GUI Setup--------------------------------------------------------------
# Initialize the main application window
root = tk.Tk()
root.title("Image Processing Tool")
root.geometry("1090x610")
root.resizable(False, False)

# Load the application icon
icon_image_path = r"C:\Users\pc world\OneDrive\Desktop\Programming project 1\Photos\ImgProcessingIcon.png"
icon_image = Image.open(icon_image_path)
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(False, icon_photo)

#----------------------------------------------------------Constants & Image Variables--------------------------------------------------------------
# Constants for preview size
PREVIEW_WIDTH = 150
PREVIEW_HEIGHT = 150

# Image variables for storing and manipulating images
uploaded_photo = None  # Image after uploading
original_image = None  # Original image (before any processing)
current_image = None   # Image currently being processed


#---------------------------------------------Image Uploading/Displaying/Saving/Resetting---------------------------------------------------

# Define function to upload an image
def upload_image():
    global uploaded_photo, original_image, current_image
    file_path = filedialog.askopenfilename()
    if file_path:
        original_image = Image.open(file_path)
        current_image = original_image.copy()

        # Resize image to fit within constraints
        max_width, max_height = 850, 550
        aspect_ratio = original_image.width / original_image.height
        if original_image.width > original_image.height:
            new_width, new_height = max_width, int(max_width / aspect_ratio)
        else:
            new_width, new_height = int(max_height * aspect_ratio), max_height

        resized_image = current_image.resize((new_width, new_height), Image.LANCZOS)
        uploaded_photo = ImageTk.PhotoImage(resized_image)
        output_label.config(image=uploaded_photo)
        output_label.image = uploaded_photo

# Define function to save the processed image
def save_image():
    global current_image
    if current_image:
        # Open file dialog to choose save location and file format
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"),
                                                           ("JPEG files", "*.jpg"),
                                                           ("All files", ".")])
        if file_path:
            # Save the current edited image to the selected file path
            current_image.save(file_path)
            print("Image saved successfully.")

# Define function to show the original image
def show_original_image(event):
    if original_image:
        original_width, original_height = original_image.size

        original_window = Toplevel(root)
        original_window.title("Original Image")
        original_window.geometry(f"{original_width}x{original_height}")

        original_photo = ImageTk.PhotoImage(original_image)
        original_label = tk.Label(original_window, image=original_photo)
        original_label.image = original_photo
        original_label.pack()

# Define function to display the image preview
def display_image_preview():
    if original_image:
        preview_image = original_image.copy()
        preview_image.thumbnail((PREVIEW_WIDTH, PREVIEW_HEIGHT), Image.LANCZOS)

        preview_photo = ImageTk.PhotoImage(preview_image)
        image_preview_label.config(image=preview_photo)
        image_preview_label.image = preview_photo

# Define function to reset the image
def reset_image():
    global current_image, uploaded_photo, original_image
    if original_image:
        # Reset the current_image to the original image
        current_image = original_image.copy()

        # Resize the image to fit within constraints
        max_width, max_height = 850, 550
        aspect_ratio = original_image.width / original_image.height
        if original_image.width > original_image.height:
            new_width, new_height = max_width, int(max_width / aspect_ratio)
        else:
            new_width, new_height = int(max_height * aspect_ratio), max_height

        resized_image = current_image.resize((new_width, new_height), Image.LANCZOS)

        # Update the UI with the reset image
        uploaded_photo = ImageTk.PhotoImage(resized_image)
        output_label.config(image=uploaded_photo)
        output_label.image = uploaded_photo





#---------------------------------------------Image Effect Adjustment Windows---------------------------------------------------
# Define function for the blur adjustment window
blur_window_open = False

def open_blur_window():
    global blur_window_open
    if blur_window_open:
        return  # Prevent opening another blur window if one is already open

    blur_window = Toplevel(root)
    blur_window.title("Adjust Blur Intensity")
    blur_window.geometry("300x150")

    blur_window_open = True

    blur_slider = ttk.Scale(blur_window, from_=1, to=100, orient='horizontal')
    blur_slider.pack(pady=30, padx=20, fill='x')
    value_label = tk.Label(blur_window, text="Intensity: 1")
    value_label.pack(pady=10)

    def update_blur(event):
        global current_image, uploaded_photo
        if current_image:
            # Map the 1-100 range to the Gaussian blur's intensity (scaled to 0-10)
            intensity = int(blur_slider.get()) / 10
            blurred_image = current_image.filter(ImageFilter.GaussianBlur(radius=intensity))

            current_image = blurred_image
            updated_photo = ImageTk.PhotoImage(blurred_image)
            output_label.config(image=updated_photo)
            output_label.image = updated_photo
            value_label.config(text=f"Intensity: {int(blur_slider.get())}")

    blur_slider.bind("<Motion>", update_blur)

    def on_closing():
        global blur_window_open
        blur_window_open = False
        blur_window.destroy()

    blur_window.protocol("WM_DELETE_WINDOW", on_closing)


edge_window = None

def open_edge_detection_window():
    global edge_window
    if edge_window is not None and edge_window.winfo_exists():
        edge_window.focus()
        return
    
    edge_window = Toplevel(root)
    edge_window.title("Adjust Edge Detection Intensity")
    edge_window.geometry("300x150")

    edge_slider = ttk.Scale(edge_window, from_=1, to=100, orient='horizontal')
    edge_slider.pack(pady=30, padx=20, fill='x')
    value_label = tk.Label(edge_window, text="Intensity: 1")
    value_label.pack(pady=10)

    def update_edge_detection(event):
        global current_image, uploaded_photo
        if current_image:
            # Scale intensity for edge detection (1-100 scaled appropriately)
            intensity = int(edge_slider.get() / 10)
            edge_image = current_image
            for _ in range(intensity):
                edge_image = edge_image.filter(ImageFilter.FIND_EDGES)
            current_image = edge_image
            edge_photo = ImageTk.PhotoImage(edge_image)
            output_label.config(image=edge_photo)
            output_label.image = edge_photo
            value_label.config(text=f"Intensity: {int(edge_slider.get())}")

    edge_slider.bind("<Motion>", update_edge_detection)


grayscale_window = None

def open_grayscale_window():
    global grayscale_window
    if grayscale_window is None or not grayscale_window.winfo_exists():
        grayscale_window = Toplevel(root)
        grayscale_window.title("Adjust Grayscale Intensity")
        grayscale_window.geometry("300x150")

        grayscale_slider = ttk.Scale(grayscale_window, from_=1, to=100, orient='horizontal')
        grayscale_slider.pack(pady=30, padx=20, fill='x')

        value_label = tk.Label(grayscale_window, text="Intensity: 1")
        value_label.pack(pady=10)

        original_image = current_image.copy() if current_image else None

        def update_grayscale(event):
            global current_image, uploaded_photo
            if original_image:
                intensity = int(grayscale_slider.get())
                
                # Convert the original image to grayscale
                gray_image = original_image.convert("L").convert("RGB")

                if intensity > 0:
                    blend_factor = intensity / 100.0
                    blended_image = Image.blend(current_image, gray_image, blend_factor)
                else:
                    blended_image = current_image

                current_image = blended_image
                updated_photo = ImageTk.PhotoImage(blended_image)
                output_label.config(image=updated_photo)
                output_label.image = updated_photo
                value_label.config(text=f"Intensity: {intensity}")
        
        grayscale_slider.bind("<Motion>", update_grayscale)
        grayscale_slider.set(1)
        update_grayscale(None)



#---------------------------------------------------------------user interface---------------------------------------------------------------------

# Constants for icon size
ICON_SIZE = (40, 40)

# Function to load and resize an image for buttons
def load_icon(image_path):
    image = Image.open(image_path)
    image = image.resize(ICON_SIZE, Image.LANCZOS)
    return ImageTk.PhotoImage(image)

# Load icons for upload, check, and download buttons
upload_icon = load_icon(r"C:\Users\pc world\OneDrive\Desktop\Programming project 1\Photos\upload.png")
upload_check_icon = load_icon(r"C:\Users\pc world\OneDrive\Desktop\Programming project 1\Photos\check.png")
upload_download_icon = load_icon(r"C:\Users\pc world\OneDrive\Desktop\Programming project 1\Photos\download.png")
reset_icon = load_icon(r"C:\Users\pc world\OneDrive\Desktop\Programming project 1\Photos\reset.png")

# Configure grid layout for the root window
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=4)
root.grid_rowconfigure(0, weight=1)

# Left side: Controls Frame
left_frame = tk.Frame(root, bg="lightgray", bd=2, relief="groove")
left_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

# Buttons for applying image filters
grayscale_button = tk.Button(left_frame, text="Grayscale", command=open_grayscale_window)
blur_button = tk.Button(left_frame, text="Blur", command=open_blur_window)
edge_button = tk.Button(left_frame, text="Edge Detection", command=open_edge_detection_window)

# Pack the buttons with some padding
grayscale_button.pack(pady=5)
blur_button.pack(pady=5)
edge_button.pack(pady=5)

# Image preview area for original image
image_preview_frame = tk.Frame(left_frame, bg="black", width=PREVIEW_WIDTH, height=PREVIEW_HEIGHT, bd=2, relief="groove")
image_preview_frame.pack(side="bottom", pady=10, padx=10)
image_preview_frame.pack_propagate(0)

# Label to show the preview image
image_preview_label = tk.Label(image_preview_frame, bg="black")
image_preview_label.pack(fill="both", expand=True)
image_preview_label.bind("<Button-1>", show_original_image)

# Right side: Processed image output area
right_frame = tk.Frame(root, bg="lightblue", bd=2, relief="groove")
right_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

# Label for displaying the processed image
output_label = tk.Label(right_frame, text="Processed Image (placeholder)", bg="lightblue")
output_label.pack(fill="both", expand=True, padx=0, pady=(5, 0))

# Icon buttons frame at the bottom of the right frame
icon_frame = tk.Frame(right_frame, bg="lightblue")
icon_frame.pack(side="bottom", pady=(0, 10), padx=10)

# Upload button to load image
upload_button = tk.Button(icon_frame, image=upload_icon, command=upload_image, bg="lightblue", borderwidth=0)
upload_button.grid(row=0, column=0, padx=20)

# Check button to display image preview
check_button = tk.Button(icon_frame, image=upload_check_icon, command=display_image_preview, bg="lightblue", borderwidth=0)
check_button.grid(row=0, column=1, padx=20)

# Download button to save image
download_button = tk.Button(icon_frame, image=upload_download_icon, command=save_image, bg="lightblue", borderwidth=0)
download_button.grid(row=0, column=2, padx=20)

# Reset button to reset the image
reset_button = tk.Button(icon_frame, image=reset_icon, command=reset_image, bg="lightblue", borderwidth=0)
reset_button.grid(row=0, column=3, padx=20)


# Start the Tkinter main loop
root.mainloop()
