import tkinter as tk
from tkinter import messagebox

class SimulatorUI:
    def __init__(self, run_simulation):
        self.window = tk.Tk()
        self.window.title("Page Replacement Simulator")
        self.window.geometry("400x300")
        self.run_simulation = run_simulation

        tk.Label(self.window, text="Enter Page Reference String (e.g., 1,2,3):").pack(pady=5)
        self.page_entry = tk.Entry(self.window)
        self.page_entry.pack()

        tk.Label(self.window, text="Enter Number of Frames:").pack(pady=5)
        self.frame_entry = tk.Entry(self.window)
        self.frame_entry.pack()

        self.algo_var = tk.StringVar(value="FIFO")
        tk.Label(self.window, text="Select Algorithm:").pack(pady=5)
        tk.Radiobutton(self.window, text="FIFO", variable=self.algo_var, value="FIFO").pack()
        tk.Radiobutton(self.window, text="LRU", variable=self.algo_var, value="LRU").pack()
        tk.Radiobutton(self.window, text="Optimal", variable=self.algo_var, value="Optimal").pack()

        tk.Button(self.window, text="Simulate", command=self.simulate).pack(pady=10)

    def simulate(self):
        messagebox.showinfo("Info", "Simulation not implemented yet!")

    def run(self):
        self.window.mainloop()
