import bankers

def recover_from_deadlock(allocation, available, strategy="terminate"):
    """
    Recovery strategies:
    - "terminate": Terminate the process holding the most resources.
    - "preempt": Preempt resources from the process holding the most resources (release all its resources).
    - "rollback": Rollback a process to a safe state (simulated as releasing all its resources).
    Returns a dict with victim and released resources.
    """
    if not allocation or not available:
        return None

    num_processes = len(allocation)
    num_resources = len(available)

    # Find the process holding the most resources
    max_resources = -1
    victim = -1
    for i, alloc in enumerate(allocation):
        total = sum(alloc)
        if total > max_resources:
            max_resources = total
            victim = i

    if victim == -1:
        return None

    released = allocation[victim][:]
    if strategy == "terminate":
        # Terminate the process and release its resources
        for j in range(num_resources):
            available[j] += allocation[victim][j]
            allocation[victim][j] = 0
        return {"victim": victim, "released": released}

    elif strategy == "preempt":
        # Preempt all resources from the victim process
        for j in range(num_resources):
            available[j] += allocation[victim][j]
            allocation[victim][j] = 0
        return {"victim": victim, "released": released}

    elif strategy == "rollback":
        #rollback by releasing all resources of the victim process
        for j in range(num_resources):
            available[j] += allocation[victim][j]
            allocation[victim][j] = 0
        return {"victim": victim, "released": released}

    return None
