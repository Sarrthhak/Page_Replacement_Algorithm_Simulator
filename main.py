from ui import SimulatorUI
from algorithms import fifo_algorithm

def run_simulation(pages, frames, algorithm):
    if algorithm == "FIFO":
        return fifo_algorithm(pages, frames)
    return 0, []

ui = SimulatorUI(run_simulation)
ui.run()
