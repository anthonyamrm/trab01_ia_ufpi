import time
import heapq
from collections import deque


ESTADO_FINAL = (1, 2, 3, 4, 5, 6, 7, 8, 0)

#A tupla de movimentos (dr, dc, descrição)
MOVES = ((-1, 0, 'CIMA'), (1, 0, 'BAIXO'), (0, -1, 'ESQUERDA'), (0, 1, 'DIREITA'))

# Contador global para desempate na heap
cout = 0

class Node:
    #Representa um estado do tabuleiro e o caminho para chegar a ele.
    def __init__(self, state, parent=None, action=None, cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost      # Profundidade/Custo do caminho (g(n))

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __repr__(self):
        return f"Node(state={self.state}, cost={self.cost})"

def get_successors(node):
    #Gera todos os estados sucessores válidos a partir do estado atual.
    state_list = list(node.state)
    zero_index = state_list.index(0)
    row, col = divmod(zero_index, 3)
    successors = []

    for dr, dc, action in MOVES:
        new_row, new_col = row + dr, col + dc

        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_zero_index = new_row * 3 + new_col
            new_state_list = state_list[:]

            # Realiza a troca (swap)
            new_state_list[zero_index], new_state_list[new_zero_index] = \
                new_state_list[new_zero_index], new_state_list[zero_index]

            new_state = tuple(new_state_list)
            successors.append(Node(new_state, node, action, node.cost + 1))

    return successors

def reconstruct_path(node, search_type):
    #Reconstrói e imprime o caminho da solução passo a passo.
    path = []
    current = node
    while current.parent is not None:
        path.append((current.state, current.action))
        current = current.parent
    path.append((current.state, None))
    path.reverse()

    print(f"\n--- SOLUÇÃO ENCONTRADA VIA {search_type.upper()} (Custo: {node.cost}) ---")

    for i, (state, action) in enumerate(path):
        action_str = f"AÇÃO: {action}" if action else "INÍCIO"
        print(f"\nPasso {i}: ({action_str})")

        # Formata o tabuleiro para impressão
        board = [str(x) if x != 0 else ' ' for x in state]

        # Imprime o tabuleiro 3x3
        print(f"| {board[0]} | {board[1]} | {board[2]} |")
        print(f"| {board[3]} | {board[4]} | {board[5]} |")
        print(f"| {board[6]} | {board[7]} | {board[8]} |")

    return path

def heuristica(state):
    #Calcula a Distância de Manhattan (h2) para o estado.
    distance = 0
    goal_positions = {
        1: (0, 0), 2: (0, 1), 3: (0, 2),
        4: (1, 0), 5: (1, 1), 6: (1, 2),
        7: (2, 0), 8: (2, 1), 0: (2, 2)
    }

    for i in range(9):
        tile = state[i]
        if tile != 0:  # Ignora o espaço vazio
            current_row, current_col = divmod(i, 3)
            goal_row, goal_col = goal_positions[tile]
            distance += abs(current_row - goal_row) + abs(current_col - goal_col)

    return distance


def resolver_jogo_do_8(initial_state, search_type='bfs', max_depth=None):
    """Executa BFS ou DFS."""
    start_time = time.time()

    if initial_state == ESTADO_FINAL:
        return Node(initial_state), 1, 0, 0.0

    if search_type == 'bfs':
        frontier = deque([Node(initial_state)])
        pop_func = frontier.popleft
    elif search_type == 'dfs':
        frontier = [Node(initial_state)]
        pop_func = frontier.pop
    else:
        raise ValueError("Tipo de busca cega inválido.")

    visited = {initial_state}
    nodes_generated = 1

    while frontier:
        current_node = pop_func()

        # Verifica objetivo ao remover da fronteira (bom para DFS também)
        if current_node.state == ESTADO_FINAL:
            end_time = time.time()
            return current_node, nodes_generated, len(frontier), end_time - start_time

        if search_type == 'dfs' and max_depth is not None and current_node.cost >= max_depth:
            continue

        for successor in get_successors(current_node):
            if successor.state not in visited:
                visited.add(successor.state)
                frontier.append(successor)
                nodes_generated += 1

    end_time = time.time()
    return None, nodes_generated, 0, end_time - start_time

def gulosa(initial_state):
    """Busca Gulosa: utiliza f(n) = h(n)."""
    global cout
    start_time = time.time()

    cout = 0

    # Fronteira: Fila de Prioridade (h_cost, counter, node)
    frontier = [(heuristica(initial_state), cout, Node(initial_state, cost=0))]
    visited_expanded = set()   # estados já removidos/expandidos
    in_frontier = {initial_state}  # para evitar inserções duplicadas (simples)
    nodes_generated = 1

    while frontier:
        _, _, current_node = heapq.heappop(frontier)

        # Se este estado já foi expandido, pular
        if current_node.state in visited_expanded:
            continue

        in_frontier.discard(current_node.state)
        visited_expanded.add(current_node.state)

        if current_node.state == ESTADO_FINAL:
            end_time = time.time()
            return current_node, nodes_generated, len(frontier), end_time - start_time

        for successor in get_successors(current_node):
            if successor.state in visited_expanded:
                continue
            if successor.state not in in_frontier:
                h_cost = heuristica(successor.state)
                cout += 1
                heapq.heappush(frontier, (h_cost, cout, successor))
                in_frontier.add(successor.state)
                nodes_generated += 1

    end_time = time.time()
    return None, nodes_generated, 0, end_time - start_time


def a_star_search(initial_state):
    """Busca A*: utiliza f(n) = g(n) + h(n)."""
    global cout
    start_time = time.time()

    cout = 0

    start_node = Node(initial_state, cost=0)
    start_h = heuristica(initial_state)
    start_f = start_node.cost + start_h

    frontier = [(start_f, cout, start_node)]
    g_scores = {initial_state: 0}
    nodes_generated = 1
    visited_expanded = set()

    while frontier:
        f_cost, _, current_node = heapq.heappop(frontier)

        # Se o nó é obsoleto (g diferente do melhor conhecido), pular
        best_g = g_scores.get(current_node.state, None)
        if best_g is not None and current_node.cost != best_g:
            continue

        if current_node.state in visited_expanded:
            continue

        visited_expanded.add(current_node.state)

        if current_node.state == ESTADO_FINAL:
            end_time = time.time()
            return current_node, nodes_generated, len(frontier), end_time - start_time

        for successor in get_successors(current_node):
            new_g_cost = current_node.cost + 1

            # Se já existe um caminho melhor para esse estado, pular
            if successor.state in g_scores and new_g_cost >= g_scores[successor.state]:
                continue

            # Caso novo ou melhor caminho:
            g_scores[successor.state] = new_g_cost
            successor.cost = new_g_cost  # garantir consistência do cost no nó
            new_h = heuristica(successor.state)
            new_f = new_g_cost + new_h

            cout += 1
            heapq.heappush(frontier, (new_f, cout, successor))
            nodes_generated += 1

    end_time = time.time()
    return None, nodes_generated, 0, end_time - start_time


if __name__ == "__main__":
    # ESTADO DE TESTE INTERMEDIÁRIO (Custo: 16)
    INITIAL_STATE = (1, 3, 6, 5, 2, 0, 4, 7, 8)

    # 1. BFS EXECUÇÃO
    print("=" * 40); print("--- EXECUTANDO 1. BFS (Cega) ---"); print("=" * 40)
    bfs_solution, bfs_nodes, bfs_frontier_len, bfs_time = resolver_jogo_do_8(INITIAL_STATE, search_type='bfs')
    if bfs_solution:
        reconstruct_path(bfs_solution, 'BFS')
        print(f"\n--- MÉTRICAS BFS --- Nós Gerados: {bfs_nodes}, Tempo: {bfs_time:.4f}s, Custo Caminho: {bfs_solution.cost}")
    else:
        print("BFS: Solução não encontrada (pode ser por limite de memória/tempo).")
        print(f"Nós Gerados: {bfs_nodes}, Tempo: {bfs_time:.4f}s")

    # 2. DFS EXECUÇÃO 
    print("\n" + "=" * 40 + "\n"); print("=" * 40); print("--- EXECUTANDO 2. DFS (Cega) ---"); print("  (Max Depth ajustado para 50)"); print("=" * 40)
    dfs_solution, dfs_nodes, dfs_frontier_len, dfs_time = resolver_jogo_do_8(INITIAL_STATE, search_type='dfs', max_depth=50)
    if dfs_solution:
        reconstruct_path(dfs_solution, 'DFS')
        print(f"\n--- MÉTRICAS DFS --- Nós Gerados: {dfs_nodes}, Tempo: {dfs_time:.4f}s, Custo Caminho: {dfs_solution.cost}")
    else:
        print("DFS: Solução não encontrada (Limite de profundidade atingido ou ineficiência).")
        print(f"Nós Gerados: {dfs_nodes}, Tempo: {dfs_time:.4f}s")

    # 3. GULOSA EXECUÇÃO
    print("\n" + "=" * 40 + "\n"); print("=" * 40); print("--- EXECUTANDO 3. GULOSA (h(n)) ---"); print("=" * 40)
    greedy_solution, greedy_nodes, greedy_frontier_len, greedy_time = gulosa(INITIAL_STATE)
    if greedy_solution:
        reconstruct_path(greedy_solution, 'GULOSA')
        print(f"\n--- MÉTRICAS GULOSA --- Nós Gerados: {greedy_nodes}, Tempo: {greedy_time:.4f}s, Custo Caminho: {greedy_solution.cost}")
    else:
        print("GULOSA: Solução não encontrada (Gulosa não é completa).")
        print(f"Nós Gerados: {greedy_nodes}, Tempo: {greedy_time:.4f}s")

    # 4. A* EXECUÇÃO
    print("\n" + "=" * 40 + "\n"); print("=" * 40); print("--- EXECUTANDO 4. A* (f(n) = g(n) + h(n)) ---"); print("=" * 40)
    astar_solution, astar_nodes, astar_frontier_len, astar_time = a_star_search(INITIAL_STATE)
    if astar_solution:
        reconstruct_path(astar_solution, 'A*')
        print(f"\n--- MÉTRICAS A* --- Nós Gerados: {astar_nodes}, Tempo: {astar_time:.4f}s, Custo Caminho: {astar_solution.cost}")
    else:
        print("A*: Solução não encontrada.")
        print(f"Nós Gerados: {astar_nodes}, Tempo: {astar_time:.4f}s")
