import streamlit as st
import matplotlib.pyplot as plt

# FIFO Algorithm
def fifo(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    
    for page in pages:
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                memory.pop(0)  # Remove the oldest page
                memory.append(page)
            page_faults += 1  # Increment page fault when page is not in memory
        memory_states.append(memory[:])  # Store the state of memory after each page reference
    
    return page_faults, memory_states

# LRU Algorithm
def lru(pages, frames):
    memory, page_faults = [], 0
    memory_states = []
    page_indices = {}  # Dictionary to track the last usage of each page
    
    for i, page in enumerate(pages):
        if page not in memory:
            if len(memory) < frames:
                memory.append(page)
            else:
                # Find the least recently used page and replace it
                lru_page = min(memory, key=lambda p: page_indices.get(p, -1))
                memory.remove(lru_page)
                memory.append(page)
            page_faults += 1  # Increment page fault when page is not in memory
        page_indices[page] = i  # Update the last used index for the page
        memory_states.append(memory[:])  # Store the state of memory after each page reference
    
    return page_faults, memory_states

# Optimal Algorithm
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
                        future_indices.append(float('inf'))  # If the page won't appear again, mark it as infinity
                
                replace_index = future_indices.index(max(future_indices))  # Replace the page that will not be used for the longest period
                memory[replace_index] = page
            page_faults += 1  # Increment page fault when page is not in memory
        memory_states.append(memory[:])  # Store the state of memory after each page reference
    
    return page_faults, memory_states

# Function to run the selected algorithm. It takes type of algorithm, pages sequence and no. of frames as arguments
def run_algorithm(algorithm, pages, frames):
    if algorithm == "FIFO":
        return fifo(pages, frames)
    elif algorithm == "LRU":
        return lru(pages, frames)
    elif algorithm == "Optimal":
        return optimal(pages, frames)

# Interface of Streamlit
st.title("Page Replacement Algorithm Simulator")
st.write(
    "This application simulates and compares the performance of different page replacement algorithms: "
    "FIFO, LRU, and Optimal. Enter the page reference string and number of frames, select an algorithm, "
    "and visualize the results."
)

# Initializing session state for inputs
if "pages_input" not in st.session_state:
    st.session_state.pages_input = ""
if "frames" not in st.session_state:
    st.session_state.frames = 3

# Taking Input for page reference string and number of frames
pages_input = st.text_input(
    "Enter page reference string (comma-separated):", value=st.session_state.pages_input
)
frames = st.number_input(
    "Enter number of frames:", min_value=1, max_value=10, value=st.session_state.frames
)

# Selecting the algorithm
algorithm = st.selectbox("Select Algorithm", ["FIFO", "LRU", "Optimal"])

# Adding the run simulation and clear button side by side for better UI
col1, col2, _ = st.columns([1, 1, 3])

# Adding run simulation button
with col1:
    run_clicked = st.button("Run Simulation")

# Adding clear button
with col2:
    clear_clicked = st.button("Clear")

# Handling the run simulation button
if run_clicked:
    if pages_input:
        pages = list(map(int, pages_input.split(",")))
        page_faults, memory_states = run_algorithm(algorithm, pages, frames)

        st.write(f"**Number of Page Faults:** {page_faults}")
        st.write("**Memory State Changes:**")

        # Split the states into columns to display them side by side
        columns = st.columns(4)  # 4 columns for better layout
        for i, state in enumerate(memory_states):
            with columns[i % 4]:  # Distribute memory states into columns
                st.write(f"Step {i+1}: {state}")

        # Bar graph to compare page faults
        fig, ax = plt.subplots(figsize=(8, 6))
        algorithms = ["FIFO", "LRU", "Optimal"]
        faults = [
            fifo(pages, frames)[0],
            lru(pages, frames)[0],
            optimal(pages, frames)[0],
        ]
        colors = ["#4C72B0", "#55A868", "#C44E52"]
        ax.bar(algorithms, faults, color=colors, width=0.6, edgecolor="black")

        ax.set_ylabel("Page Faults", fontsize=12, fontweight="bold")
        ax.set_xlabel("Algorithm", fontsize=12, fontweight="bold")
        ax.set_title("Comparison of Page Faults Across Algorithms", fontsize=14, fontweight="bold")
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        st.pyplot(fig)

        # Finding algorithms with minimum and maximum page faults
        min_faults = min(faults)
        max_faults = max(faults)
        
        best_algorithms = [algorithms[i] for i, fault in enumerate(faults) if fault == min_faults]
        worst_algorithms = [algorithms[i] for i, fault in enumerate(faults) if fault == max_faults]
        
        # Format the insights properly
        best_algorithm_str = ", ".join(best_algorithms)
        worst_algorithm_str = ", ".join(worst_algorithms)

        st.write("### Insights from the Simulation")
        # Highlight the best and worst algorithms
        st.write(f"**Best Algorithm(s):** {best_algorithm_str} with the least page faults.")
        st.write(f"**Worst Algorithm(s):** {worst_algorithm_str} with the highest page faults.")
        
        if min_faults == faults[0]:
            st.write(
                "**Why FIFO is preferred:** FIFO works well when the page reference pattern has fewer repeated pages and the order of page usage is predictable. "
                "However, it may cause Belady's anomaly, where adding more frames increases page faults."
            )
        if min_faults == faults[1]:
            st.write(
                "**Why LRU is preferred:** LRU performs best when the most recently used pages are likely to be used again soon. "
                "It's more efficient for workloads where recent usage predicts future usage but requires tracking page usage history."
            )
        if min_faults == faults[2]:
            st.write(
                "**Why Optimal is preferred:** Optimal provides the least number of page faults since it replaces the page that won’t be used for the longest period. "
                "However, it's unrealistic for real-world scenarios as future requests are unknown."
            )
        
        if max_faults == faults[0]:
            st.write(
                "**FIFO Limitation:** FIFO can be inefficient in situations where recently used pages are accessed repeatedly, "
                "as it doesn’t consider the frequency or recency of use."
            )
        if max_faults == faults[1]:
            st.write(
                "**LRU Limitation:** LRU can suffer from high overhead due to frequent updates of the page usage history, "
                "especially when the page reference string is long."
            )
        if max_faults == faults[2]:
            st.write(
                "**Optimal Limitation:** Optimal is theoretical and impractical because it requires perfect knowledge of future requests, "
                "which is not possible in real-world systems."
            )
