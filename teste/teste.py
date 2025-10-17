import random

def print_board(board):
    print("\n")
    for i in range(3):
        print(" | ".join(board[i]))
        if i < 2:
            print("--+---+--")
    print("\n")

def check_winner(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]],
    ]
    return [player]*3 in win_conditions

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

def player_move(board):
    while True:
        try:
            move = int(input("Escolha uma posição (1-9): ")) - 1
            row, col = divmod(move, 3)
            if board[row][col] == " ":
                return row, col
            else:
                print("Essa posição já está ocupada.")
        except:
            print("Entrada inválida. Tente novamente.")

def ai_move(board, difficulty):
    empty = get_empty_cells(board)
    if difficulty == "fácil":
        return random.choice(empty)
    elif difficulty == "médio":
        # Tenta ganhar ou bloquear
        for player in ["O", "X"]:
            for (i, j) in empty:
                board[i][j] = player
                if check_winner(board, player):
                    board[i][j] = " "
                    return i, j
                board[i][j] = " "
        return random.choice(empty)
    elif difficulty == "difícil":
        # Minimax simplificado
        best_score = -float("inf")
        best_move = None
        for (i, j) in empty:
            board[i][j] = "O"
            score = minimax(board, False)
            board[i][j] = " "
            if score > best_score:
                best_score = score
                best_move = (i, j)
        return best_move

def minimax(board, is_maximizing):
    if check_winner(board, "O"):
        return 1
    elif check_winner(board, "X"):
        return -1
    elif not get_empty_cells(board):
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for (i, j) in get_empty_cells(board):
            board[i][j] = "O"
            score = minimax(board, False)
            board[i][j] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for (i, j) in get_empty_cells(board):
            board[i][j] = "X"
            score = minimax(board, True)
            board[i][j] = " "
            best_score = min(score, best_score)
        return best_score

def main():
    print("🎮 Bem-vindo ao Jogo da Velha!")
    name = input("Digite seu nome: ")
    difficulty = input("Escolha a dificuldade (fácil, médio, difícil): ").lower()

    board = [[" "]*3 for _ in range(3)]
    print_board(board)

    for turn in range(9):
        if turn % 2 == 0:
            print(f"{name}, é sua vez!")
            row, col = player_move(board)
            board[row][col] = "X"
        else:
            print("IA está jogando...")
            row, col = ai_move(board, difficulty)
            board[row][col] = "O"

        print_board(board)

        if check_winner(board, "X"):
            print(f"🎉 {name} venceu!")
            break
        elif check_winner(board, "O"):
            print("🤖 IA venceu!")
            break
    else:
        print("😐 Empate!")

if __name__ == "__main__":
    main()