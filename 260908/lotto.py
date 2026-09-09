import tkinter as tk
import random

def get_ball_color(number):
    if 1 <= number <= 10:
        return "#fbc400"  # Yellow
    elif 11 <= number <= 20:
        return "#69c8f2"  # Blue
    elif 21 <= number <= 30:
        return "#ff7272"  # Red
    elif 31 <= number <= 40:
        return "#aaaaaa"  # Grey
    else:
        return "#b0d840"  # Green

def generate_lotto():
    # Clear previous results
    canvas.delete("all")
    
    for i in range(5):
        # Generate 6 unique numbers
        numbers = sorted(random.sample(range(1, 46), 6))
        
        # Display numbers as colored balls
        y_offset = 20 + (i * 70)
        canvas.create_text(30, y_offset + 25, text=f"Set {i+1}:", font=("Arial", 12, "bold"), anchor="w")
        
        for j, num in enumerate(numbers):
            x_offset = 100 + (j * 60)
            color = get_ball_color(num)
            
            # Draw ball
            canvas.create_oval(x_offset, y_offset, x_offset + 50, y_offset + 50, fill=color, outline="white", width=2)
            # Draw number
            canvas.create_text(x_offset + 25, y_offset + 25, text=str(num), font=("Arial", 14, "bold"), fill="white" if num > 20 else "black")

# Main Window
root = tk.Tk()
root.title("Lotto Number Generator")
root.geometry("500x450")
root.resizable(False, False)

# UI Elements
title_label = tk.Label(root, text="Lotto 6/45 Generator", font=("Arial", 20, "bold"), pady=20)
title_label.pack()

generate_button = tk.Button(root, text="Generate 5 Sets", font=("Arial", 14), command=generate_lotto, bg="#4CAF50", fg="white", padx=20, pady=10)
generate_button.pack()

canvas = tk.Canvas(root, width=480, height=350, bg="white", highlightthickness=0)
canvas.pack(pady=20)

root.mainloop()
