from queue import PriorityQueue


def manhattan_distance(current_state, goal_state, verbose=False):
    total_distance = 0
    moves = []

    for row_index in range(3):
        for col_index in range(3):
            current_tile = current_state[row_index][col_index]

            if current_tile != 0:
                goal_row, goal_col = next(
                    (row, col)
                    for row, row_state in enumerate(goal_state)
                    for col, value in enumerate(row_state)
                    if value == current_tile
                )

                total_distance += abs(row_index - goal_row) + abs(col_index - goal_col)

                if verbose and (row_index != goal_row or col_index != goal_col):
                    moves.append(f"Peça {current_tile} está em ({row_index}, {col_index}) e deveria estar em ({goal_row}, {goal_col}) = {abs(row_index - goal_row) + abs(col_index - goal_col)}")

    return total_distance, moves

def get_neighbors(state):
    neighbors = []
    zero_row, zero_col = next((r, c) for r, row in enumerate(state) for c, val in enumerate(row) if val == 0)
    directions = {'up': (-1, 0), 'down': (1, 0), 'left': (0, -1), 'right': (0, 1)}

    for direction, (dr, dc) in directions.items():
        new_row, new_col = zero_row + dr, zero_col + dc
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            swapped_state = [row[:] for row in state]
            swapped_state[zero_row][zero_col], swapped_state[new_row][new_col] = swapped_state[new_row][new_col], swapped_state[zero_row][zero_col]
            neighbors.append((swapped_state, direction))
    return neighbors

def state_to_key(state):
    return ';'.join(','.join(str(tile) for tile in row) for row in state)

def print_state(state):
    for row in state:
        print(row)
    print()

def a_star_search(initial, goal):
    print("Objetivo:")
    print_state(goal)

    print("Estado inicial:")
    print_state(initial)

    visited = set()
    queue = PriorityQueue()
    queue.put((manhattan_distance(initial, goal), 0, initial, []))

    while not queue.empty():
        total_cost, path_cost, current, path = queue.get()
        current_key = state_to_key(current)
        heuristic, moves = manhattan_distance(current, goal, verbose=path)

        if (path): 
            print()
            print("#############################################")
            print("Explorando caminho:", ' -> '.join(path) or 'inicial', f"com custo de caminho g(n) {path_cost} e heurística h(n) {heuristic}")
            print_state(current)

        if current == goal:
            print("Caminho final encontrado com custo total:", total_cost)
            return path

        if current_key not in visited:
            visited.add(current_key)

            for neighbor, action in get_neighbors(current):
                if state_to_key(neighbor) not in visited:
                    cost = path_cost + 1
                    future_heuristic, moves = manhattan_distance(neighbor, goal, verbose=True)
                    queue.put((cost + future_heuristic, cost, neighbor, path + [action]))

                    print()
                    print(f"Ação: {action}, g(n): {cost} h(n): {future_heuristic} e f(n): {cost + future_heuristic}")
                    print_state(neighbor)
                    print_state(moves)

    return None

# initial_state = [[2, 3, 6], [1, 8, 4], [7, 0, 5]]
initial_state = [
    [2, 8, 3], 
    [1, 6, 4], 
    [7, 0, 5]
    ]
goal_state = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]

solution_path = a_star_search(initial_state, goal_state)

if solution_path:
    print("Solução encontrada:")
    for move in solution_path:
        print(f"Movimento do zero: {move}")
else:
    print("Solução não encontrada.")
