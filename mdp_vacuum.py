import math
import random


environment_matrix = [[0, 0, 0, 0], [0, "X", 0, 0], [0, 0, 0, 0], [0, -1, 0, 10]]

directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

action_names = {(-1, 0): "North", (0, 1): "East", (1, 0): "South", (0, -1): "West"}

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
    best_action = None

    if current_val == 10 or current_val == -1:
        return 0, None

    if depth == 0:
        return 0, None

    for action in directions:
        expected_val = 0

        for probability, next_outcome in get_prob(matrix, start, action):
            r, c = next_outcome
            reward = matrix[r][c]
            if reward == 10 or reward == -1:
                future_val = 0

            else:
                future_val, _ = expectimax(matrix, start=next_outcome, depth=depth-1, living_cost=living_cost)

            expected_val += probability * (living_cost + future_val + reward)
        
        if expected_val > best_val:
            best_val, best_action = expected_val, action

    return best_val, best_action
    

### -------Part 2: Reward Functions-------------------------

def run_vacuum(matrix, start=(0, 3), depth=5, living_cost=-0.05, max_steps=30, seed=None):
    if seed is not None:
        random.seed(seed)
    position = start
    path = [position]
    total_reward = 0

    start_val, _ = expectimax(matrix, start, depth, living_cost)
    print(f"\nLiving cost: {living_cost} | Start value: {start_val:.3f}")
    print(f"Step 0: start at {position}")

    for step in range(1, max_steps + 1):
        q, action = expectimax(matrix, position, depth, living_cost)
        outcomes = get_prob(matrix, position, action)
        intended = outcomes[0][1]

        roll, cumulative, new_pos = random.random(), 0, outcomes[-1][1]
        for probability, nxt in outcomes:
            cumulative += probability
            if roll < cumulative:
                new_pos = nxt
                break

        r, c = new_pos
        total_reward += living_cost + matrix[r][c]
        note = "as intended" if new_pos == intended else "SLIPPED"
        print(f"Step {step}: at {position}, chose {action_names[action]} "
              f"(value={q:.3f}) -> {new_pos} [{note}]")
        position = new_pos
        path.append(position)

        if matrix[r][c] == 10:
            print(f"Reached recharge station in {step} steps. Total reward: {total_reward:.2f}")
            break
        if matrix[r][c] == -1:
            print(f"Fell into the trap in {step} steps. Total reward: {total_reward:.2f}")
            break
    else:
        print("Max steps reached without finishing.")

    print("Path:", " -> ".join(map(str, path)))
    return path

if __name__ == "__main__":
    # changeable living costs
    for lc in [-0.04, -0.5, -5.0]:
        run_vacuum(environment_matrix, living_cost=lc, seed=42)