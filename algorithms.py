def fifo_algorithm(pages, frames):
    memory = []
    faults = 0
    steps = []
    for page in pages:
        if page not in memory and len(memory) < frames:
            memory.append(page)
            faults += 1
        elif page not in memory:
            memory.pop(0)
            memory.append(page)
            faults += 1
        steps.append(memory.copy())
    return faults, steps
