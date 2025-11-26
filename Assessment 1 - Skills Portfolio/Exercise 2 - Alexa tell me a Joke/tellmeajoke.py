import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import random
import os
import winsound


# Play sound when buttons are clicked
def play_click():
    winsound.PlaySound("click.wav", winsound.SND_ASYNC)

# Play special sound when punchline is revealed
def play_punchline():
    winsound.PlaySound("punchline.wav", winsound.SND_ASYNC)


# Load jokes from text file and split into setup/punchline pairs
def load_jokes():
    jokes = []
    with open("randomJokes.txt", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Split joke at question mark into setup and punchline
            if "?" in line:
                setup, punchline = line.split("?", 1)
                jokes.append((setup + "?", punchline))
    return jokes

# Store all loaded jokes in memory
jokes = load_jokes()


# Create main application window
root = tk.Tk()
root.title("ALEXA TELL ME A JOKE")
root.geometry("500x500")
# Prevent window resizing for consistent layout
root.resizable(False, False)

# Set window icon
root.iconbitmap("tell_me_a_joke.ico")

# Create drawing canvas that fills the entire window
canvas = tk.Canvas(root, width=500, height=500, highlightthickness=0, bd=0)
canvas.pack(fill="both", expand=True)


# Load static background image
bg_png = Image.open("tell_me_a_joke_bg.png").resize((500, 500))
bg_png_photo = ImageTk.PhotoImage(bg_png)


# Load animated GIF frames for special effects
gif_frames = []
gif_path = "tell_me_a_joke_bg.gif"

# Only load GIF if file exists
if os.path.exists(gif_path):
    gif = Image.open(gif_path)
    # Extract each frame from the GIF
    for frame in ImageSequence.Iterator(gif):
        frame = frame.resize((500, 500))
        gif_frames.append(ImageTk.PhotoImage(frame))

# Track animation state
gif_running = False
gif_index = 0


# Animate GIF frames continuously
def play_gif():
    global gif_running, gif_index

    # Stop if animation is disabled
    if not gif_running:
        return

    # Display current frame and advance to next
    canvas.itemconfig(background_image_id, image=gif_frames[gif_index])
    gif_index = (gif_index + 1) % len(gif_frames)

    # Schedule next frame update (80ms delay for smooth animation)
    root.after(80, play_gif)


# Switch to static background image
def show_png_background():
    global gif_running
    gif_running = False
    canvas.itemconfig(background_image_id, image=bg_png_photo)


# Switch to animated background
def show_gif_background():
    global gif_running
    gif_running = True
    play_gif()


# Create background image on canvas
background_image_id = canvas.create_image(0, 0, image=bg_png_photo, anchor="nw")


# Create text area for joke setup
setup_text_id = canvas.create_text(
    250, 145,
    text="Click the button to hear a joke!",
    fill="black",
    font=("Segoe UI", 20, "bold"),
    justify="center",
    width=380  # Text will wrap within this width
)

# Create text area for punchline (initially hidden)
punchline_text_id = canvas.create_text(
    250, 240,
    text="",
    fill="black",
    font=("Segoe UI", 16, "bold"),
    justify="center",
    width=380
)


# Store current joke being displayed
current_setup = ""
current_punchline = ""
first_click_done = False


# Display a new random joke
def new_joke():
    play_click()
    # Use static background for new jokes
    show_png_background()

    global current_setup, current_punchline
    # Pick random joke from loaded collection
    current_setup, current_punchline = random.choice(jokes)

    # Update display with new joke setup
    canvas.itemconfig(setup_text_id, text=current_setup)
    canvas.itemconfig(punchline_text_id, text="")

    # Change button text after first use
    global first_click_done
    if not first_click_done:
        first_click_done = True
        canvas.itemconfig(alexa_btn_text, text="NEXT JOKE")


# Reveal the punchline with sound and animation
def show_punchline():
    play_punchline()
    # Switch to animated background for punchline
    show_gif_background()
    canvas.itemconfig(punchline_text_id, text=current_punchline)


# Load button background image
rounded_btn_img = Image.open("button_rounded.png").resize((160, 35))
rounded_btn_photo = ImageTk.PhotoImage(rounded_btn_img)


# Create clickable button on canvas
def create_canvas_button(text, x, y, command):
    # Create button image
    img_id = canvas.create_image(x, y, image=rounded_btn_photo)
    # Create button text
    text_id = canvas.create_text(
        x, y,
        text=text,
        fill="black",
        font=("Segoe UI", 8, "bold")
    )

    # Handle click on button
    def click(event):
        command()

    # Make both image and text clickable
    canvas.tag_bind(img_id, "<Button-1>", click)
    canvas.tag_bind(text_id, "<Button-1>", click)

    return img_id, text_id


# Track if this is the first joke request
first_click_done = False

# Create main joke button (text changes after first use)
alexa_btn_img, alexa_btn_text = create_canvas_button(
    "ALEXA TELL ME A JOKE", 250, 310, new_joke
)

# Create punchline reveal button
create_canvas_button("SHOW PUNCHLINE", 250, 355, show_punchline)

# Create quit button with sound effect
create_canvas_button("QUIT", 250, 400, lambda: (play_click(), root.destroy()))


# Start the application event loop
root.mainloop()
