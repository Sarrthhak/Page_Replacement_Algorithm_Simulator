import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Algorithm Implementations
def fifo(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    for page in pages:
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)
            page_faults += 1
        memory_states.append(memory.copy())
    return page_faults, memory_states

def lru(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    page_indices = {}
    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                lru_page = min(memory, key=lambda p: page_indices.get(p, -1))
                memory.remove(lru_page)
                memory.append(page)
            page_faults += 1
        page_indices[page] = i
        memory_states.append(memory.copy())
    return page_faults, memory_states

def optimal(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                future_indices = []
                for mem_page in memory:
                    if mem_page in pages[i:]:
                        future_indices.append(pages[i:].index(mem_page))
                    else:
                        future_indices.append(float('inf'))
                replace_index = future_indices.index(max(future_indices))
                memory[replace_index] = page
            page_faults += 1
        memory_states.append(memory.copy())
    return page_faults, memory_states

# UI Configuration
st.set_page_config(layout="centered")
st.title("Page Replacement Algorithm Simulator")

algorithm = st.selectbox("Select algorithm", ["FIFO", "LRU", "Optimal"])
frames = st.number_input("Enter number of frames", min_value=1, max_value=10, value=3)
ref_string = st.text_input("Enter reference string (separated by spaces)", "6 7 8 9 6 7 1 6 7 8 9 1")

if st.button("Generate"):
    pages = list(map(int, ref_string.split()))
    
    # Computation Outline
    st.markdown("---")
    st.header("Computation Outline")
    st.write(f"**Algorithm:** {algorithm}")
    st.write(f"**Frames:** {frames}")
    st.write(f"**Reference Length:** {len(pages)}")
    st.write(f"**Reference String:** {' '.join(map(str, pages))}")
    
    # Run selected algorithm
    if algorithm == "FIFO":
        page_faults, memory_states = fifo(pages, frames)
    elif algorithm == "LRU":
        page_faults, memory_states = lru(pages, frames)
    else:
        page_faults, memory_states = optimal(pages, frames)
    
    # Results
    st.markdown("---")
    st.header("Results")
    
    hit_count = len(pages) - page_faults
    miss_rate = (page_faults / len(pages)) * 100
    hit_rate = (hit_count / len(pages)) * 100
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Page Faults", page_faults)
    with col2:
        st.metric("Hits", hit_count)
    
    # Battery-like Visualization
    st.subheader("Battery-style Hit/Miss Visualization")

    def battery_bar(percentage, label):
        fig, ax = plt.subplots(figsize=(4, 1.2))
        color = (
            "#ff1a1a" if percentage <= 10 else
            "#ff9900" if percentage <= 30 else
            "#ffff33" if percentage <= 60 else
            "#66ff66"
        )
        ax.barh([0], percentage, color=color, height=0.5)
        ax.set_xlim(0, 100)
        ax.set_xticks([0, 25, 50, 75, 100])
        ax.set_xticklabels(["0%", "25%", "50%", "75%", "100%"])
        ax.set_yticks([])
        ax.set_title(f"{label}: {percentage:.1f}%", fontsize=10)
        ax.grid(True, axis='x', linestyle='--', alpha=0.5)
        st.pyplot(fig)

    battery_bar(hit_rate, "Hit Rate")
    battery_bar(miss_rate, "Miss Rate")
    
    # Memory States Table
    st.markdown("---")
    st.header("Memory State Changes")
    state_data = []
    for i, state in enumerate(memory_states):
        fault = "✔️" if pages[i] not in (memory_states[i-1] if i > 0 else []) else "➖"
        row = {
            "Step": i+1,
            "Frame 1": state[0] if len(state) > 0 else "-",
            "Frame 2": state[1] if len(state) > 1 else "-",
            "Frame 3": state[2] if len(state) > 2 else "-",
            "Page Fault": fault
        }
        state_data.append(row)
    st.table(state_data)
    
    # Algorithm Comparison
    st.markdown("---")
    st.header("Algorithm Comparison")
    fig, ax = plt.subplots(figsize=(8, 4))
    algorithms = ["FIFO", "LRU", "Optimal"]
    faults = [fifo(pages, frames)[0], lru(pages, frames)[0], optimal(pages, frames)[0]]
    ax.bar(algorithms, faults, color=["#4C72B0", "#55A868", "#C44E52"])
    ax.set_ylabel("Page Faults")
    ax.set_title("Page Faults by Algorithm")
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)
    
    # Insights
    st.markdown("---")
    st.header("Algorithm Insights")
    if algorithm == "Optimal":
        st.info("""
        Optimal provides the theoretical minimum page faults by replacing the page that won't be used for the longest time. 
        While impossible to implement in practice, it serves as a useful benchmark.
        """)
    elif algorithm == "LRU":
        st.info("""
        LRU performs well when recently used pages are likely to be used again soon.
        It approximates optimal behavior but requires tracking usage history.
        """)
    else:
        st.info("""
        FIFO works well when page references are evenly distributed without clustering.
        It's simple but may suffer from Belady's anomaly where increasing frames can increase page faults.
        """)

st.markdown("---")
st.caption("Made by Sarthak Pipladiya, Abhishek Kumar, Himanshu Gobari")
