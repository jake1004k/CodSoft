import streamlit as st
import numpy as np

# Initialize the game state
if 'board' not in st.session_state:
    st.session_state.board = np.full((3, 3), ' ')
if 'turn' not in st.session_state:
    st.session_state.turn = 'X'  # Human goes first
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

def reset_game():
    st.session_state.board = np.full((3, 3), ' ')
    st.session_state.turn = 'X'
    st.session_state.winner = None
    st.session_state.game_over = False

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != ' ':
            return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != ' ':
            return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != ' ':
        return board[0][2]
    if np.all(board != ' '):
        return 'Draw'
    return None

def minimax(board, is_maximizing):
    winner = check_winner(board)
    if winner == 'X':
        return -1
    elif winner == 'O':
        return 1
    elif winner == 'Draw':
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    score = minimax(board, False)
                    board[i][j] = ' '
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    score = minimax(board, True)
                    board[i][j] = ' '
                    best_score = min(score, best_score)
        return best_score

def best_move(board):
    best_score = -float('inf')
    move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                score = minimax(board, False)
                board[i][j] = ' '
                if score > best_score:
                    best_score = score
                    move = (i, j)
    return move

st.title("Tic-Tac-Toe with AI")

if st.button("Reset Game"):
    reset_game()

for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        with cols[j]:
            if st.button(st.session_state.board[i][j], key=f'{i}-{j}'):
                if st.session_state.board[i][j] == ' ' and st.session_state.turn == 'X' and not st.session_state.game_over:
                    st.session_state.board[i][j] = 'X'
                    st.session_state.turn = 'O'
                    st.session_state.winner = check_winner(st.session_state.board)
                    if st.session_state.winner:
                        st.session_state.game_over = True
                    else:
                        ai_move = best_move(st.session_state.board)
                        if ai_move:
                            st.session_state.board[ai_move[0]][ai_move[1]] = 'O'
                            st.session_state.turn = 'X'
                            st.session_state.winner = check_winner(st.session_state.board)
                            if st.session_state.winner:
                                st.session_state.game_over = True

if st.session_state.winner:
    if st.session_state.winner == 'Draw':
        st.write("It's a draw!")
    else:
        st.write(f"The winner is {st.session_state.winner}!")
else:
    st.write(f"Turn: {st.session_state.turn}")