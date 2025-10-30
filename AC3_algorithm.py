from collections import deque

# Revise domain of xi with respect to xj by removing values that don't meet the constraint xi != xj
def revise(domains, xi, xj):
    revised = False

    # If xj only has one value then remove it from xi's domain
    if len(domains[xj]) == 1:
        value = next(iter(domains[xj])) # Get the value
        # If xi has that value then remove because xi != xj
        if value in domains[xi]:
            domains[xi].remove(value)
            revised = True

    return revised # Will return true if any values are removed from the domain of xi

# Implement AC-3 Algorithm
def AC3(domains, neighbours):
    queue = deque((xi, xj) for xi in domains for xj in neighbours[xi]) # Make queue with all arcs for every variable and neighbours
    length_queue = [] # Track queue length

    # Loop through queue until empty
    while queue:
        length_queue.append(len(queue)) # Update queue length before each pop
        xi, xj = queue.popleft() # Take an arc

        # Revise if needed
        if revise(domains, xi, xj):
            # If xi's domain is empty then the csp is inconsistent
            if len(domains[xi]) == 0:
                length_queue.append(len(queue))
                return domains, length_queue
            # If we revise then recheck all arcs for xk in xi's neighbors
            for xk in neighbours[xi]:
                if xk != xj: # Don't add the same arc back right away
                    queue.append((xk, xi))

    return domains, length_queue # Return the domain and queue length