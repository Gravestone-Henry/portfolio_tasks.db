import sqlite3
import os

DB_NAME = "portfolio_tasks.db"

def conectar():
    """Conecta ao banco de dados SQLite (cria o arquivo se não existir)."""
    return sqlite3.connect(DB_NAME)

def criar_tabela():
    """Cria a tabela de tarefas caso ela ainda não exista."""
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            categoria TEXT NOT NULL,
            status TEXT DEFAULT 'Pendente'
        )
    """)
    conn.commit()
    conn.close()

def adicionar_tarefa():
    print("\n--- Adicionar Nova Tarefa ---")
    titulo = input("Digite o título da tarefa: ")
    categoria = input("Digite a categoria (ex: Trabalho, Estudos,Pessoal): ")
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tarefas (titulo, categoria) VALUES (?, ?)", (titulo, categoria))
    conn.commit()
    conn.close()
    print("✅ Tarefa adicionada com sucesso!")

def listar_tarefas():
    print("\n--- Lista de Tarefas ---")
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, categoria, status FROM tarefas")
    tarefas = cursor.fetchall()
    conn.close()

    if not tarefas:
        print("Nenhuma tarefa cadastrada.")
        return

    print(f"{'ID':<4} | {'Título':<25} | {'Categoria':<15} | {'Status':<10}")
    print("-" * 60)
    for t in tarefas:
        print(f"{t[0]:<4} | {t[1]:<25} | {t[2]:<15} | {t[3]:<10}")

def concluir_tarefa():
    listar_tarefas()
    try:
        task_id = int(input("\nDigite o ID da tarefa que deseja concluir: "))
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("UPDATE tarefas SET status = 'Concluído' WHERE id = ?", (task_id,))
        conn.commit()
        conn.close()
        print(" Tarefa marcada como concluída!")
    except ValueError:
        print(" Por favor, digite um número de ID válido.")

def main():
    criar_tabela()
    while True:
        print("\n==============================")
        print("   GERENCIADOR DE TAREFAS     ")
        print("==============================")
        print("1. Adicionar Tarefa")
        print("2. Listar Tarefas")
        print("3. Concluir Tarefa")
        print("4. Sair")
        
        opcao = input("\nEscolha uma opção (1-4): ")
        
        if opcao == "1":
            adicionar_tarefa()
        elif opcao == "2":
            listar_tarefas()
        elif opcao == "3":
            concluir_tarefa()
        elif opcao == "4":
            print("\nAté logo! Saindo do sistema...")
            break
        else:
            print("❌ Opção inválida, tente novamente.")

if __name__ == "__main__":
    main()