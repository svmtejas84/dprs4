Deadlock Prevention & Recovery (DPR) A Streamlit-based interactive tool to demonstrate deadlock prevention, detection, and recovery in operating systems using the Banker's Algorithm. This project allows users to simulate resource allocation, check for safe states, and apply various deadlock recovery strategies including process termination, resource preemption, and process rollback.

Features:
Banker's Algorithm for safe state checking and resource allocation
Deadlock detection using system state analysis
Interactive resource request simulation
Deadlock recovery with three strategies:
Terminate: Kill a process to release its resources
Preempt: Forcefully reclaim resources from a process
Rollback: Simulate rolling back a process to a safe state
Resource Allocation Graph (RAG) visualization and cycle detection
User-friendly Streamlit web interface

Working:
Input the number of processes and resource types
Enter the Allocation, Max Demand, and Available matrices
View the system state and check for safe/unsafe (deadlock) conditions
Request resources for any process and observe the system’s response
If deadlock is detected, choose a recovery strategy (terminate, preempt, rollback)
Visualize the Resource Allocation Graph and detect cycles

Usage:
Step 1:Enter the number of processes and resource types.
Step 2:Input the Allocation, Max Demand, and Available matrices.
Step 3:View the current system state and whether it is safe or in deadlock.
Step 4:Request resources for any process and see if the request is granted.
Step 5: If a deadlock is detected, choose a recovery strategy:
  Terminate Process:Kills a process and releases its resources.
  Preempt Resources:Forcefully reclaims resources from a process.
  Rollback Process: Simulates rolling back a process to a safe state.
Step 6: Visualize the Resource Allocation Graph and check for cycles.


Deadlock Concepts:
Deadlock Prevention:Avoids deadlocks by careful resource allocation (e.g., Banker's Algorithm)[3][4].
Deadlock Detection:Identifies deadlocks using safe state checks and resource allocation graphs[3].
Deadlock Recovery:Resolves deadlocks by terminating processes, preempting resources, or rolling back processes[3][4].
