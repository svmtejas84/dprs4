import streamlit as st
import numpy as np
import pandas as pd
import bankers  # Ensure bankers.py is correctly imported
import recovery  # Import the recovery module

#Fonts
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;700&display=swap');
    @font-face {
      font-family: 'Inge';
      src: url('https://fonts.cdnfonts.com/s/17307/Inge.woff') format('woff');
    }
    html, body, [class*="css"]  {
      font-family: 'IBM Plex Sans', Arial, sans-serif;
      background: #f7f7fa;
    }
    h1, h2, h3 {
      font-family: 'Inge', 'IBM Plex Sans', Arial, sans-serif;
      letter-spacing: 1px;
    }
    .stButton>button {
      font-family: 'IBM Plex Sans', Arial, sans-serif;
      font-size: 1.1em;
      border-radius: 7px;
      padding: 0.4em 1.5em;
      background: #437ef7;
      color: #fff;
      border: none;
    }
    </style>
""", unsafe_allow_html=True)

#Helper Functions for Display 
def matrix_input(label, rows, cols, key_prefix):
    st.write(f"**{label}**")
    matrix = []
    for i in range(rows):
        cols_vals = st.text_input(f"{label} for P{i} (space separated)", key=f"{key_prefix}_{i}")
        if cols_vals:
            try:
                vals = [int(x) for x in cols_vals.strip().split()]
                if len(vals) == cols:
                    matrix.append(vals)
                else:
                    st.warning(f"Enter exactly {cols} values for P{i}.")
                    return None
            except ValueError:
                st.warning(f"Please enter valid integers for P{i}.")
                return None
        else:
            return None
    return matrix

def vector_input(label, cols, key):
    vals = st.text_input(f"{label} (space separated)", key=key)
    if vals:
        try:
            vals = [int(x) for x in vals.strip().split()]
            if len(vals) == cols:
                return vals
            else:
                st.warning(f"Enter exactly {cols} values.")
                return None
        except ValueError:
            st.warning(f"Please enter valid integers for the vector.")
            return None
    return None

def display_matrix(matrix, row_labels, col_labels, caption):
    st.write(f"**{caption}**")
    arr = np.array(matrix)
    st.table(
        pd.DataFrame(arr, index=row_labels, columns=col_labels)
    )

def display_state(allocation, max_demand, available, need):
    n_proc = len(allocation)
    n_res = len(available)
    proc_labels = [f"P{i}" for i in range(n_proc)]
    res_labels = [f"R{j}" for j in range(n_res)]
    display_matrix(allocation, proc_labels, res_labels, "Allocation Matrix")
    display_matrix(max_demand, proc_labels, res_labels, "Max Demand Matrix")
    display_matrix(need, proc_labels, res_labels, "Need Matrix")
    st.write(f"**Available:** {available}")

def show_rag(allocation, request, available):
    n_proc = len(allocation)
    n_res = len(available)
    st.write("**Resource Allocation Graph (RAG):**")
    for i in range(n_proc):
        for j in range(n_res):
            if allocation[i][j] > 0:
                st.write(f"R{j} → P{i} (Allocated {allocation[i][j]})")
    for i in range(n_proc):
        for j in range(n_res):
            if request[i][j] > 0:
                st.write(f"P{i} → R{j} (Requested {request[i][j]})")

def find_cycle(allocation, request):
    n_proc = len(allocation)
    n_res = len(allocation[0])
    graph = {}
    for i in range(n_proc):
        graph[f"P{i}"] = []
        for j in range(n_res):
            if request[i][j] > 0:
                graph[f"P{i}"].append(f"R{j}")
    for j in range(n_res):
        graph[f"R{j}"] = []
        for i in range(n_proc):
            if allocation[i][j] > 0:
                graph[f"R{j}"].append(f"P{i}")
    stack = []
    def dfs(node):
        if node in stack:
            return stack[stack.index(node):]
        stack.append(node)
        for neighbor in graph.get(node, []):
            cycle = dfs(neighbor)
            if cycle:
                return cycle
        stack.pop()
        return None
    for node in graph:
        cycle = dfs(node)
        if cycle:
            return cycle
    return None

# Streamlit UI
def run_ui(bankers, recovery):
    st.title("Deadlock Prevention & Recovery (DPR)")
    st.caption("Project by Tejas V K with inputs from Ayush and Muskan.")

    if "step" not in st.session_state:
        st.session_state.step = 0
    if "np" not in st.session_state:
        st.session_state.np = None
    if "nr" not in st.session_state:
        st.session_state.nr = None
    if "allocation" not in st.session_state:
        st.session_state.allocation = None
    if "max_demand" not in st.session_state:
        st.session_state.max_demand = None
    if "available" not in st.session_state:
        st.session_state.available = None
    if "need" not in st.session_state:
        st.session_state.need = None

    # Step 0: Input number of processes/resources
    if st.session_state.step == 0:
        st.header("Step 1: Enter Number of Processes and Resources")
        with st.form(key="step1_form"):
            np_ = st.number_input("Number of processes", min_value=1, max_value=10, value=3)
            nr_ = st.number_input("Number of resource types", min_value=1, max_value=10, value=3)
            submit_button = st.form_submit_button(label="Next")
            if submit_button:
                st.session_state.np = np_
                st.session_state.nr = nr_
                st.session_state.step = 1
                st.rerun()

    # Step 1: Input matrices
    elif st.session_state.step == 1:
        st.header("Step 2: Enter Allocation, Max Demand, and Available")
        with st.form(key="step2_form"):
            allocation = matrix_input("Allocation Matrix", st.session_state.np, st.session_state.nr, "alloc")
            max_demand = matrix_input("Max Demand Matrix", st.session_state.np, st.session_state.nr, "max")
            available = vector_input("Available Resources", st.session_state.nr, "avail")
            submit_button = st.form_submit_button(label="Next")
            if allocation and max_demand and available and submit_button:
                need = bankers.calculate_need(allocation, max_demand)
                st.session_state.allocation = allocation
                st.session_state.max_demand = max_demand
                st.session_state.available = available
                st.session_state.need = need
                st.write("Matrices entered successfully.")
                st.session_state.step = 2
                st.rerun()

    # Step 2: Display state and deadlock detection
    elif st.session_state.step == 2:
        st.header("Step 3: System State & Deadlock Detection")
        allocation = st.session_state.allocation
        max_demand = st.session_state.max_demand
        available = st.session_state.available
        need = st.session_state.need
        display_state(allocation, max_demand, available, need)
        safe, seq = bankers.is_safe_state(allocation, max_demand, available)
        if safe:
            st.success(f"System is in a safe state. Safe sequence: {seq}")
        else:
            st.error("System is NOT in a safe state. Deadlock possible.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Request Resources"):
                st.session_state.step = 3
                st.rerun()
        with col2:
            if not safe and st.button("Recover from Deadlock"):
                st.session_state.step = 4
                st.rerun()
        st.write("---")
        if st.button("Show Resource Allocation Graph (RAG)"):
            st.session_state.step = 5
            st.rerun()

    # Step 3: Request resources
    elif st.session_state.step == 3:
        st.header("Step 4: Request Resources")
        np_ = st.session_state.np
        nr_ = st.session_state.nr
        pid = st.number_input("Process ID", min_value=0, max_value=np_-1, value=0)
        request = vector_input("Request Vector", nr_, "reqvec")
        if request:
            ok, msg = bankers.request_resources(
                pid, request,
                st.session_state.allocation,
                st.session_state.max_demand,
                st.session_state.available
            )
            if ok:
                st.success(msg)
                st.session_state.need = bankers.calculate_need(
                    st.session_state.allocation, st.session_state.max_demand)
            else:
                st.error(msg)
        if st.button("Back to State"):
            st.session_state.step = 2
            st.rerun()

    # Step 4: Deadlock recovery with all strategies
    elif st.session_state.step == 4:
        st.header("Step 5: Deadlock Recovery")
        st.write("Choose a recovery strategy:")
        col1, col2, col3 = st.columns(3)
        result = None

        with col1:
            if st.button("Terminate Process"):
                result = recovery.recover_from_deadlock(
                    st.session_state.allocation,
                    st.session_state.available,
                    strategy="terminate"
                )
                if result:
                    st.success(f"Terminated process P{result['victim']}. Resources released: {result['released']}")
                else:
                    st.error("No process could be terminated.")

        with col2:
            if st.button("Preempt Resources"):
                result = recovery.recover_from_deadlock(
                    st.session_state.allocation,
                    st.session_state.available,
                    strategy="preempt"
                )
                if result:
                    st.success(f"Preempted all resources from P{result['victim']}. Resources released: {result['released']}")
                else:
                    st.error("No process could be preempted.")

        with col3:
            if st.button("Rollback Process"):
                result = recovery.recover_from_deadlock(
                    st.session_state.allocation,
                    st.session_state.available,
                    strategy="rollback"
                )
                if result:
                    st.success(f"Rolled back process P{result['victim']}. Resources released: {result['released']}")
                else:
                    st.error("No process could be rolled back.")

        if st.button("Back to State"):
            st.session_state.step = 2
            st.rerun()

    # Step 5: Show RAG and cycle
    elif st.session_state.step == 5:
        st.header("Resource Allocation Graph (RAG) and Cycle Detection")
        allocation = st.session_state.allocation
        available = st.session_state.available
        need = st.session_state.need
        request = need  
        show_rag(allocation, request, available)
        cycle = find_cycle(allocation, request)
        if cycle:
            st.warning(f"Cycle detected: {' → '.join(cycle)}")
        else:
            st.success("No cycle detected. No deadlock.")
        if st.button("Back to State"):
            st.session_state.step = 2
            st.rerun()
