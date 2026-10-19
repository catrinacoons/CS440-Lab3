import math

environment_matrix = [[0, 0, 0, 0], [0, "X", 0, 0], [0, 0, 0, 0], [0, -1, 0, 10]]

directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def get_neighbors(row, col, max_rows = 4, max_cols = 4):
    neighbors = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < max_rows and 0 <= c < max_cols:
            if environment_matrix[r][c] != "X":
                neighbors.append((r, c))
    return neighbors

def move(matrix, position, direction):
    row, col = position
    dr, dc = direction

    new_row = row + dr
    new_col = col + dc

    if not(0 <= new_row < 4 and 0 <= new_col < 4):
        return position

    if matrix[new_row][new_col] == "X":
        return position
    
    return (new_row, new_col)

def get_prob(matrix, position, action):
    index = directions.index(action)
    intended = directions[index]

    left = directions[(index + 1) % 4]
    right = directions[(index - 1) % 4]

    return [(0.8, move(matrix, position, intended)), (0.1, move(matrix, position, left)), (0.1, move(matrix, position, right))]

def expectimax(matrix, start=(0,3), depth=5, living_cost=-0.05): #depth of 5 enough to reach chargning station
    current_row, current_col = start
    current_val = matrix[current_row][current_col]
    path = [(current_row, current_col, current_val)]

    best_val = float("-inf")

    if current_val == 10 or current_val == -1:
        return 0

    if depth == 0:
        return 0

    for action in directions:
        expected_val = 0

        for probability, next_outcome in get_prob(matrix, start, action):
            r, c = next_outcome
            reward = matrix[r][c]
            if reward == 10 or reward == -1:
                future_val = 0

            else:
                future_val = expectimax(matrix, start=next_outcome, depth=depth-1, living_cost=living_cost)

            expected_val += probability * (living_cost + future_val + reward)

        best_val = max(best_val, expected_val)

    return best_val
    
