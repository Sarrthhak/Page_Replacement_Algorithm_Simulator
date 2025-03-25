import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

class SimulatorUI:
    def __init__(self, run_simulation):
        self.window = tk.Tk()
        self.window.title("Page Replacement Simulator")
        self.window.geometry("500x350")
        self.window.resizable(True,True)
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
        tk.Button(self.window,text="Clear",command=self.clear).pack(pady=5)
        self.result_label = tk.Label(self.window, text="Page Faults: N/A")
        self.result_label.pack(pady=5)

    def simulate(self):
        try:
            pages = [int(x) for x in self.page_entry.get().split(",")]
            frames = int(self.frame_entry.get())
            if frames < 1 or frames >10:
                messagebox.showerror("Error", "Frames must be between 1 and 10!")
                return
            fifo_faults, fifo_steps = self.run_simulation(pages, frames, "FIFO")
            lru_faults, lru_steps = self.run_simulation(pages, frames, "LRU")
            opt_faults, opt_steps = self.run_simulation(pages, frames, "Optimal")
            faults, steps = self.run_simulation(pages, frames, self.algo_var.get())
            messagebox.showinfo("Result", f"{self.algo_var.get()} Page Faults: {faults}\nSteps: {steps}")
            self.result_label.config(text=f"Page Faults: {faults}")
            self.plot_results(fifo_faults, lru_faults, opt_faults)
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Use numbers and commas.")

    def plot_results(self, fifo_faults, lru_faults, opt_faults):
        algorithms = ["FIFO", "LRU", "Optimal"]
        faults = [fifo_faults, lru_faults, opt_faults]
        plt.bar(algorithms, faults, color=["blue", "green", "red"])
        plt.title("Page Faults Comparison")
        plt.xlabel("Algorithm")
        plt.ylabel("Number of Page Faults")
        plt.grid(True)
        plt.show()
    def clear(self):
        self.page_entry.delete(0, tk.END)
        self.frame_entry.delete(0,tk.END)
        self.result_label.config(text="Page Faults: N/A")

    def run(self):
        self.window.mainloop()
