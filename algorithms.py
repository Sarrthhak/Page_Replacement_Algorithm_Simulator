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

def lru_algorithm(pages, frames):
    memory = []
    faults = 0
    steps = []
    recent = []
    for page in pages:
        if page not in memory and len(memory) < frames:
            memory.append(page)
            recent.append(page)
            faults += 1
        elif page not in memory:
            lru_page = recent.pop(0)
            memory.remove(lru_page)
            memory.append(page)
            recent.append(page)
            faults += 1
        elif page in memory:
            recent.remove(page)
            recent.append(page)
        steps.append(memory.copy())
    return faults, steps

def optimal_algorithm(pages, frames):
    memory = []
    faults = 0
    steps = []
    for i, page in enumerate(pages):
        if page not in memory and len(memory) < frames:
            memory.append(page)
            faults += 1
        elif page not in memory:
            future = pages[i+1:]
            replace = memory[0]
            max_dist = -1
            for mem_page in memory:
                dist = future.index(mem_page) if mem_page in future else len(future)
                if dist > max_dist:
                    max_dist = dist
                    replace = mem_page
            memory.remove(replace)
            memory.append(page)
            faults += 1
        steps.append(memory.copy())
    return faults, steps
