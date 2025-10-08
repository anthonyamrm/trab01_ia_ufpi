import tkinter as tk
from tkinter import messagebox

from jogodo8 import (
    resolver_jogo_do_8, gulosa, a_star_search,
    reconstruct_path
)

def run_searches():
    user_input = entry.get().strip()
    try:
        numbers = tuple(map(int, user_input.replace(",", " ").split()))
    except ValueError:
        messagebox.showerror("Erro", "Entrada inválida, use apenas números de 0 a 8.")
        return

    if set(numbers) != set(range(9)):
        messagebox.showerror("Erro", "Você deve inserir todos os números de 0 a 8, sem repetir.")
        return

    initial_state = numbers

    print("\n=======================================")
    print(f"ESTADO INICIAL: {initial_state}")
    print("=======================================\n")

    # --- 1. BFS ---
    print("=" * 40)
    print("--- EXECUTANDO 1. BFS (Cega) ---")
    print("=" * 40)
    bfs_solution, bfs_nodes, _, bfs_time = resolver_jogo_do_8(initial_state, 'bfs')
    if bfs_solution:
        reconstruct_path(bfs_solution, 'BFS')
        messagebox.showinfo("BFS", f"Solução encontrada!\nNós: {bfs_nodes}\nTempo: {bfs_time:.4f}s\nCusto: {bfs_solution.cost}")
    else:
        messagebox.showinfo("BFS", f"Solução não encontrada.\nNós: {bfs_nodes}\nTempo: {bfs_time:.4f}s")

    # --- 2. DFS ---
    print("\n" + "=" * 40)
    print("--- EXECUTANDO 2. DFS (Cega) ---")
    print("=" * 40)
    dfs_solution, dfs_nodes, _, dfs_time = resolver_jogo_do_8(initial_state, 'dfs', max_depth=50)
    if dfs_solution:
        reconstruct_path(dfs_solution, 'DFS')
        messagebox.showinfo("DFS", f"Solução encontrada!\nNós: {dfs_nodes}\nTempo: {dfs_time:.4f}s\nCusto: {dfs_solution.cost}")
    else:
        messagebox.showinfo("DFS", f"Solução não encontrada.\nNós: {dfs_nodes}\nTempo: {dfs_time:.4f}s")

    # --- 3. Gulosa ---
    print("\n" + "=" * 40)
    print("--- EXECUTANDO 3. GULOSA ---")
    print("=" * 40)
    greedy_solution, greedy_nodes, _, greedy_time = gulosa(initial_state)
    if greedy_solution:
        reconstruct_path(greedy_solution, 'GULOSA')
        messagebox.showinfo("Gulosa", f"Solução encontrada!\nNós: {greedy_nodes}\nTempo: {greedy_time:.4f}s\nCusto: {greedy_solution.cost}")
    else:
        messagebox.showinfo("Gulosa", f"Solução não encontrada.\nNós: {greedy_nodes}\nTempo: {greedy_time:.4f}s")

    # --- 4. A* ---
    print("\n" + "=" * 40)
    print("--- EXECUTANDO 4. A* ---")
    print("=" * 40)
    astar_solution, astar_nodes, _, astar_time = a_star_search(initial_state)
    if astar_solution:
        reconstruct_path(astar_solution, 'A*')
        messagebox.showinfo("A*", f"Solução encontrada!\nNós: {astar_nodes}\nTempo: {astar_time:.4f}s\nCusto: {astar_solution.cost}")
    else:
        messagebox.showinfo("A*", f"Solução não encontrada.\nNós: {astar_nodes}\nTempo: {astar_time:.4f}s")

root = tk.Tk()
root.title("Jogo do 8 — Inserir Estado Inicial")

tk.Label(root, text="Digite o estado inicial (números 0 a 8):").pack(pady=8)

entry = tk.Entry(root, width=30, font=("Arial", 12))
entry.pack(pady=5)
entry.insert(0, "1 3 6 5 2 0 4 7 8") 

tk.Button(root, text="Executar Buscas", command=run_searches, bg="#4CAF50", fg="white", font=("Arial", 11, "bold")).pack(pady=10)

root.mainloop()
