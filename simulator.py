import tkinter as tk

window = tk.Tk()
window.title("Page Replacement Simulator")
window.geometry("400x300")

tk.Label(window, text="Enter Page Reference String (e.g., 1,2,3):").pack(pady=5)
page_entry = tk.Entry(window)
page_entry.pack()

tk.Label(window, text="Enter Number of Frames:").pack(pady=5)
frame_entry = tk.Entry(window)
frame_entry.pack()

window.mainloop()