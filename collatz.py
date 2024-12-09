import tkinter as tk
from tkinter import messagebox
from math import sin, cos, radians, pi
from matplotlib import pyplot as plt

def collatz_sequence(n):
    """Generate the Collatz sequence for a given number n."""
    sequence = [n]
    while n != 1:
        if n % 2 == 0:
            n //= 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    return sequence

def draw_bubble(canvas, x, y, text, radius=20):
    """Draw a number bubble on the canvas."""
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="#ff2f5d", outline="black", width=2)
    canvas.create_text(x, y, text=text, fill="white", font=("Arial", 10, "bold"))

def draw_arrow(canvas, x1, y1, x2, y2):
    """Draw an arrow between two points."""
    canvas.create_line(x1, y1, x2, y2, arrow=tk.LAST, width=2, fill="black")

def animate_sequence():
    """Generate and animate the Collatz sequence."""
    global bubbles, zoom_level
    try:

        number = int(entry.get())
        if number <= 0:
            raise ValueError("Number must be a positive integer.")

        canvas.delete("all")

        sequence = collatz_sequence(number)

        bubble_radius = 20
        max_bubbles = len(sequence)
        angle_step = 360 / max_bubbles
        radius_step = min(canvas.winfo_width(), canvas.winfo_height()) / (2 * max_bubbles)

        bubbles = []
        prev_x, prev_y = None, None

        center_x, center_y = canvas.winfo_width() / 2, canvas.winfo_height() / 2
        current_radius = 0

        for i, num in enumerate(sequence):

            current_angle = radians(i * angle_step)
            x = center_x + current_radius * cos(current_angle)
            y = center_y + current_radius * sin(current_angle)

            bubbles.append((x, y, num))

            draw_bubble(canvas, x, y, num, radius=bubble_radius)

            if prev_x is not None and prev_y is not None:
                draw_arrow(canvas, prev_x, prev_y, x, y)

            prev_x, prev_y = x, y
            current_radius += radius_step

        plot_chart(sequence)

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def plot_chart(sequence):
    """Display the Collatz sequence as a line chart."""
    plt.figure(figsize=(8, 5))
    plt.plot(range(len(sequence)), sequence, marker="o", color="#ff2f5d", linestyle="-")
    plt.title("Collatz Sequence Chart")
    plt.xlabel("Step")
    plt.ylabel("Value")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.show()

def zoom_canvas(scale_factor):
    """Zoom in or out on the canvas."""
    global bubbles, zoom_level

    canvas.delete("all")  
    zoom_level *= scale_factor

    for x, y, num in bubbles:
        scaled_x = canvas.winfo_width() / 2 + (x - canvas.winfo_width() / 2) * zoom_level
        scaled_y = canvas.winfo_height() / 2 + (y - canvas.winfo_height() / 2) * zoom_level
        draw_bubble(canvas, scaled_x, scaled_y, num)

    for i in range(len(bubbles) - 1):
        x1, y1, _ = bubbles[i]
        x2, y2, _ = bubbles[i + 1]
        scaled_x1 = canvas.winfo_width() / 2 + (x1 - canvas.winfo_width() / 2) * zoom_level
        scaled_y1 = canvas.winfo_height() / 2 + (y1 - canvas.winfo_height() / 2) * zoom_level
        scaled_x2 = canvas.winfo_width() / 2 + (x2 - canvas.winfo_width() / 2) * zoom_level
        scaled_y2 = canvas.winfo_height() / 2 + (y2 - canvas.winfo_height() / 2) * zoom_level
        draw_arrow(canvas, scaled_x1, scaled_y1, scaled_x2, scaled_y2)

def start_panning(event):
    """Start panning the canvas."""
    canvas.scan_mark(event.x, event.y)

def do_panning(event):
    """Perform panning on the canvas."""
    canvas.scan_dragto(event.x, event.y, gain=1)

window = tk.Tk()
window.title("Collatz Conjecture Animation")
window.geometry("900x700")

bubbles = []
zoom_level = 1.0

frame = tk.Frame(window)
frame.pack(pady=10)

label = tk.Label(frame, text="Enter a positive integer:")
label.grid(row=0, column=0, padx=5)
entry = tk.Entry(frame, width=10)
entry.grid(row=0, column=1, padx=5)
start_button = tk.Button(frame, text="Animate", command=animate_sequence)
start_button.grid(row=0, column=2, padx=5)

zoom_frame = tk.Frame(window)
zoom_frame.pack(pady=5)
zoom_in_button = tk.Button(zoom_frame, text="Zoom In", command=lambda: zoom_canvas(1.2))
zoom_in_button.grid(row=0, column=0, padx=5)
zoom_out_button = tk.Button(zoom_frame, text="Zoom Out", command=lambda: zoom_canvas(0.8))
zoom_out_button.grid(row=0, column=1, padx=5)

canvas = tk.Canvas(window, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

canvas.bind("<ButtonPress-3>", start_panning)  
canvas.bind("<B3-Motion>", do_panning)        

window.mainloop()