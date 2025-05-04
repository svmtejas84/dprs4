def calculate_need(allocation, max_demand):
    """
    Calculate the Need matrix, which represents the remaining resources each process needs.
    Need = Max Demand - Allocation
    """
    if not allocation or not max_demand:
        return []
    need = [
        [max_demand[i][j] - allocation[i][j] for j in range(len(allocation[0]))]
        for i in range(len(allocation))
    ]
    print("Need Matrix:", need)  # Debugging line
    return need

def is_safe_state(allocation, max_demand, available):
    """
    Check if the system is in a safe state using Banker's algorithm.
    """
    if not allocation or not max_demand or not available:
        return False, []

    num_processes = len(allocation)
    num_resources = len(available)
    
    # Step 1: Calculate need matrix
    need = calculate_need(allocation, max_demand)
    
    # Step 2: Initialize work and finish arrays
    work = available[:]
    finish = [False] * num_processes
    safe_sequence = []
    
    print(f"Initial Available Resources: {available}")
    
    # Step 3: Try to find a safe sequence
    while len(safe_sequence) < num_processes:
        progress = False
        for i in range(num_processes):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(num_resources)):
                print(f"Process P{i} can proceed.")
                for j in range(num_resources):
                    work[j] += allocation[i][j]
                finish[i] = True
                safe_sequence.append(i)
                progress = True
                print(f"Updated Available Resources (work): {work}")
        if not progress:  # No progress, deadlock detected
            print("No progress, deadlock detected.")
            return False, []
    
    return True, safe_sequence

def request_resources(process_id, request, allocation, max_demand, available):
    """
    Request resources for a process and check if the request can be granted safely.
    """
    num_processes = len(allocation)
    num_resources = len(available)

    # Edge case: Validate process_id
    if not (0 <= process_id < num_processes):
        return False, "Error: Invalid process ID."

    # Edge case: Empty allocation
    if not allocation or not max_demand or not available:
        return False, "Error: Allocation, max_demand, or available is empty."

    need = calculate_need(allocation, max_demand)

    # Check if request is less than need
    if any(request[j] > need[process_id][j] for j in range(num_resources)):
        return False, "Error: Request exceeds process's maximum claim."

    # Check if request is less than available
    if any(request[j] > available[j] for j in range(num_resources)):
        return False, "Error: Not enough resources available."

    # Try to allocate resources temporarily
    temp_allocation = [row[:] for row in allocation]
    temp_available = available[:]
    for j in range(num_resources):
        temp_allocation[process_id][j] += request[j]
        temp_available[j] -= request[j]

    safe, sequence = is_safe_state(temp_allocation, max_demand, temp_available)
    if safe:
        # Grant the request
        for j in range(num_resources):
            allocation[process_id][j] += request[j]
            available[j] -= request[j]
        return True, f"Request granted. Safe sequence: {sequence}"
    else:
        return False, "Request denied: System would be unsafe."