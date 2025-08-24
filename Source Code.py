import copy
import math
from typing import List, Tuple, Optional

class ChessBoard:
    def __init__(self):
        # Initialize 8x8 board with starting position
        self.board = [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
        self.current_player = 'white'
        self.move_history = []
        self.en_passant_target = None
        self.castling_availability = {
            'white_king': True, 'white_queen': True,
            'black_king': True, 'black_queen': True
        }
        self.halfmove_clock = 0
        self.fullmove_number = 1

    def print_board(self):
        """Print the current state of the chessboard"""
        print('\n  a b c d e f g h')
        for i in range(8):
            print(f'{8-i} ', end='')
            for j in range(8):
                print(self.board[i][j], end=' ')
            print(f'{8-i}')
        print('  a b c d e f g h\n')

    def get_piece(self, pos: Tuple[int, int]) -> str:
        """Get piece at given position"""
        return self.board[pos[0]][pos[1]]

    def move_piece(self, start: Tuple[int, int], end: Tuple[int, int], promotion: str = None):
        """Move piece from start to end position, handle castling and promotion"""
        piece = self.get_piece(start)
        self.board[end[0]][end[1]] = piece if not promotion else promotion
        self.board[start[0]][start[1]] = '.'
        
        # Update castling availability
        if piece.lower() == 'k':
            self.castling_availability[f'{self.current_player}_king'] = False
            self.castling_availability[f'{self.current_player}_queen'] = False
        elif piece.lower() == 'r':
            if start == (7, 0) and self.current_player == 'white':
                self.castling_availability['white_queen'] = False
            elif start == (7, 7) and self.current_player == 'white':
                self.castling_availability['white_king'] = False
            elif start == (0, 0) and self.current_player == 'black':
                self.castling_availability['black_queen'] = False
            elif start == (0, 7) and self.current_player == 'black':
                self.castling_availability['black_king'] = False

        # Handle castling
        if piece.lower() == 'k' and abs(start[1] - end[1]) == 2:
            if end[1] > start[1]:  # Kingside
                self.board[start[0]][5] = self.board[start[0]][7]  # Move rook from h to f
                self.board[start[0]][7] = '.'
            else:  # Queenside
                self.board[start[0]][3] = self.board[start[0]][0]  # Move rook from a to d
                self.board[start[0]][0] = '.'

        # Handle en passant
        if piece.lower() == 'p':
            if self.en_passant_target and end == self.en_passant_target:
                capture_row = end[0] + (1 if self.current_player == 'white' else -1)
                self.board[capture_row][end[1]] = '.'
            # Set en passant target for two-square pawn moves
            if abs(start[0] - end[0]) == 2:
                self.en_passant_target = (
                    start[0] + (1 if self.current_player == 'black' else -1),
                    start[1]
                )
            else:
                self.en_passant_target = None
        else:
            self.en_passant_target = None

        # Update move counters
        if piece.lower() == 'p' or self.get_piece(end) != '.':
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1
        
        if self.current_player == 'black':
            self.fullmove_number += 1

    def get_legal_moves(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get all legal moves for current player"""
        moves = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece != '.' and (
                    (piece.isupper() and self.current_player == 'white') or 
                    (piece.islower() and self.current_player == 'black')
                ):
                    moves.extend(self.get_legal_moves_for_piece((i, j)))
        return moves

    def get_legal_moves_for_piece(self, pos: Tuple[int, int]) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get legal moves for a specific piece"""
        piece = self.get_piece(pos).lower()
        moves = []
        
        if piece == 'p':
            moves.extend(self.get_pawn_moves(pos))
        elif piece == 'n':
            moves.extend(self.get_knight_moves(pos))
        elif piece == 'b':
            moves.extend(self.get_bishop_moves(pos))
        elif piece == 'r':
            moves.extend(self.get_rook_moves(pos))
        elif piece == 'q':
            moves.extend(self.get_bishop_moves(pos))
            moves.extend(self.get_rook_moves(pos))
        elif piece == 'k':
            moves.extend(self.get_king_moves(pos))
        
        # Filter out moves that would leave own king in check
        legal_moves = []
        for move in moves:
            temp_board = copy.deepcopy(self)
            temp_board.move_piece(move[0], move[1])
            if not temp_board.is_in_check(self.current_player):
                legal_moves.append(move)
                
        return legal_moves

    def get_pawn_moves(self, pos: Tuple[int, int]) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get legal pawn moves, including captures and two-square advances"""
        moves = []
        row, col = pos
        direction = -1 if self.current_player == 'white' else 1
        start_row = 6 if self.current_player == 'white' else 1
        
        # One square forward
        if 0 <= row + direction < 8 and self.board[row + direction][col] == '.':
            moves.append((pos, (row + direction, col)))
            # Two squares forward from starting position
            if row == start_row and self.board[row + 2 * direction][col] == '.' and self.board[row + direction][col] == '.':
                moves.append((pos, (row + 2 * direction, col)))
        
        # Captures
        for dc in [-1, 1]:
            new_col = col + dc
            if 0 <= new_col < 8 and 0 <= row + direction < 8:
                target = self.board[row + direction][new_col]
                if target != '.' and (
                    target.isupper() != self.get_piece(pos).isupper()
                ):
                    moves.append((pos, (row + direction, new_col)))
                elif self.en_passant_target and (
                    row + direction, new_col
                ) == self.en_passant_target:
                    moves.append((pos, (row + direction, new_col)))
        
        return moves

    def get_knight_moves(self, pos: Tuple[int, int]) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get legal knight moves"""
        moves = []
        row, col = pos
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for dr, dc in knight_moves:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target == '.' or target.isupper() != self.get_piece(pos).isupper():
                    moves.append((pos, (new_row, new_col)))
        
        return moves

    def get_bishop_moves(self, pos: Tuple[int, int]) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get legal bishop moves"""
        moves = []
        row, col = pos
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = self.board[r][c]
                moves.append((pos, (r, c)))
                if target != '.':
                    if target.isupper() != self.get_piece(pos).isupper():
                        break
                    else:
                        moves.pop()  # Remove move to own piece's square
                        break
                r += dr
                c += dc
        
        return moves

    def get_rook_moves(self, pos: Tuple[int, int]) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get legal rook moves"""
        moves = []
        row, col = pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                target = self.board[r][c]
                moves.append((pos, (r, c)))
                if target != '.':
                    if target.isupper() != self.get_piece(pos).isupper():
                        break
                    else:
                        moves.pop()  # Remove move to own piece's square
                        break
                r += dr
                c += dc
        
        return moves

    def get_king_moves(self, pos: Tuple[int, int]) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get legal king moves including castling"""
        moves = []
        row, col = pos
        directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1), (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
        
        # Normal king moves
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < 8 and 0 <= new_col < 8:
                target = self.board[new_row][new_col]
                if target == '.' or target.isupper() != self.get_piece(pos).isupper():
                    moves.append((pos, (new_row, new_col)))
        
        # Castling
        if self.castling_availability[f'{self.current_player}_king'] and not self.is_in_check(self.current_player):
            # Kingside
            if (
                self.board[row][col + 1] == '.' and
                self.board[row][col + 2] == '.' and
                not self.is_square_attacked((row, col + 1), self.current_player) and
                not self.is_square_attacked((row, col + 2), self.current_player)
            ):
                moves.append((pos, (row, col + 2)))
            # Queenside
            if (
                self.board[row][col - 1] == '.' and
                self.board[row][col - 2] == '.' and
                self.board[row][col - 3] == '.' and
                not self.is_square_attacked((row, col - 1), self.current_player) and
                not self.is_square_attacked((row, col - 2), self.current_player)
            ):
                moves.append((pos, (row, col - 2)))
        
        return moves

    def is_in_check(self, player: str) -> bool:
        """Check if player's king is in check"""
        king_pos = None
        for i in range(8):
            for j in range(8):
                if self.board[i][j].lower() == 'k' and (
                    (player == 'white' and self.board[i][j].isupper()) or
                    (player == 'black' and self.board[i][j].islower())
                ):
                    king_pos = (i, j)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False
        return self.is_square_attacked(king_pos, player)

    def is_square_attacked(self, pos: Tuple[int, int], player: str) -> bool:
        """Check if a square is attacked by opponent's pieces"""
        row, col = pos
        opponent = 'black' if player == 'white' else 'white'
        
        # Check knight attacks
        knight_moves = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        for dr, dc in knight_moves:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = self.board[r][c]
                if piece.lower() == 'n' and (
                    (opponent == 'white' and piece.isupper()) or
                    (opponent == 'black' and piece.islower())
                ):
                    return True

        # Check diagonal attacks (bishop/queen)
        for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = self.board[r][c]
                if piece != '.':
                    if (
                        piece.lower() in ('b', 'q') and
                        ((opponent == 'white' and piece.isupper()) or
                         (opponent == 'black' and piece.islower()))
                    ):
                        return True
                    break
                r += dr
                c += dc

        # Check rank/file attacks (rook/queen)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                piece = self.board[r][c]
                if piece != '.':
                    if (
                        piece.lower() in ('r', 'q') and
                        ((opponent == 'white' and piece.isupper()) or
                         (opponent == 'black' and piece.islower()))
                    ):
                        return True
                    break
                r += dr
                c += dc

        # Check pawn attacks
        pawn_dir = 1 if opponent == 'white' else -1
        for dc in [-1, 1]:
            r, c = row + pawn_dir, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                piece = self.board[r][c]
                if piece.lower() == 'p' and (
                    (opponent == 'white' and piece.isupper()) or
                    (opponent == 'black' and piece.islower())
                ):
                    return True

        # Check king attacks
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                r, c = row + dr, col + dc
                if 0 <= r < 8 and 0 <= c < 8:
                    piece = self.board[r][c]
                    if piece.lower() == 'k' and (
                        (opponent == 'white' and piece.isupper()) or
                        (opponent == 'black' and piece.islower())
                    ):
                        return True

        return False

    def is_checkmate(self) -> bool:
        """Check if current position is checkmate"""
        if not self.is_in_check(self.current_player):
            return False
        return len(self.get_legal_moves()) == 0

    def is_stalemate(self) -> bool:
        """Check if current position is stalemate"""
        if self.is_in_check(self.current_player):
            return False
        return len(self.get_legal_moves()) == 0

class ChessAI:
    def __init__(self, depth: int = 3):
        self.depth = depth
        self.piece_values = {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9, 'k': 100}
        # Positional bonuses
        self.center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        self.pawn_structure_bonus = 0.5
        self.mobility_bonus = 0.1

    def evaluate_position(self, board: ChessBoard) -> float:
        """Evaluate board position with material and positional factors"""
        score = 0
        
        # Material evaluation
        for i in range(8):
            for j in range(8):
                piece = board.board[i][j]
                if piece != '.':
                    value = self.piece_values[piece.lower()]
                    if piece.isupper():
                        score += value
                    else:
                        score -= value
                    # Center control bonus
                    if (i, j) in self.center_squares and piece.lower() in ('p', 'n', 'b'):
                        score += 0.5 if piece.isupper() else -0.5
                    # Mobility bonus
                    if piece.lower() != 'k':
                        moves = len(board.get_legal_moves_for_piece((i, j)))
                        score += moves * self.mobility_bonus if piece.isupper() else -moves * self.mobility_bonus
        
        # Pawn structure bonus
        for col in range(8):
            white_pawns = sum(1 for row in range(8) if board.board[row][col] == 'P')
            black_pawns = sum(1 for row in range(8) if board.board[row][col] == 'p')
            if white_pawns > 1:
                score += self.pawn_structure_bonus
            if black_pawns > 1:
                score -= self.pawn_structure_bonus
                
        # King safety penalty
        for player in ['white', 'black']:
            king_pos = None
            for i in range(8):
                for j in range(8):
                    if board.board[i][j].lower() == 'k' and (
                        (player == 'white' and board.board[i][j].isupper()) or
                        (player == 'black' and board.board[i][j].islower())
                    ):
                        king_pos = (i, j)
                        break
                if king_pos:
                    break
            if king_pos:
                attackers = sum(1 for r in range(8) for c in range(8) 
                              if board.board[r][c] != '.' and 
                              board.board[r][c].isupper() != (player == 'white') and
                              board.is_square_attacked(king_pos, player))
                score += -attackers * 0.5 if player == 'white' else attackers * 0.5
                
        return score

    def minimax(self, board: ChessBoard, depth: int, alpha: float, beta: float, maximizing: bool) -> Tuple[float, Optional[Tuple[Tuple[int, int], Tuple[int, int]]]]:
        """Min-Max algorithm with Alpha-Beta pruning"""
        if depth == 0 or board.is_checkmate() or board.is_stalemate():
            return self.evaluate_position(board), None

        if maximizing:
            max_eval = -math.inf
            best_move = None
            for move in board.get_legal_moves():
                temp_board = copy.deepcopy(board)
                temp_board.move_piece(move[0], move[1])
                temp_board.current_player = 'black' if temp_board.current_player == 'white' else 'white'
                eval_score, _ = self.minimax(temp_board, depth - 1, alpha, beta, False)
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = math.inf
            best_move = None
            for move in board.get_legal_moves():
                temp_board = copy.deepcopy(board)
                temp_board.move_piece(move[0], move[1])
                temp_board.current_player = 'black' if temp_board.current_player == 'white' else 'white'
                eval_score, _ = self.minimax(temp_board, depth - 1, alpha, beta, True)
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
            return min_eval, best_move

    def get_best_move(self, board: ChessBoard) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Get AI's best move"""
        _, move = self.minimax(board, self.depth, -math.inf, math.inf, board.current_player == 'white')
        return move

def pos_to_notation(pos: Tuple[int, int]) -> str:
    """Convert position to algebraic notation"""
    return f"{chr(ord('a') + pos[1])}{8 - pos[0]}"

def notation_to_pos(notation: str) -> Tuple[int, int]:
    """Convert algebraic notation to position"""
    col = ord(notation[0].lower()) - ord('a')
    row = 8 - int(notation[1])
    return (row, col)

def main():
    """Main game loop"""
    board = ChessBoard()
    ai = ChessAI(depth=3)
    
    while True:
        board.print_board()
        print(f"Move {board.fullmove_number}. {board.current_player}'s turn")
        
        if board.is_checkmate():
            print(f"Checkmate! {'Black' if board.current_player == 'white' else 'White'} wins!")
            break
        if board.is_stalemate():
            print("Stalemate! The game is a draw.")
            break
            
        if board.current_player == 'white':
            # Human player's move
            while True:
                move = input("Enter your move (e.g., e2e4) or 'quit' to exit: ").lower()
                if move == 'quit':
                    print("Game ended.")
                    return
                
                if len(move) == 4:
                    try:
                        start = notation_to_pos(move[:2])
                        end = notation_to_pos(move[2:])
                        # Validate piece belongs to current player
                        piece = board.get_piece(start)
                        if piece == '.' or (piece.isupper() != (board.current_player == 'white')):
                            print("Invalid move: No valid piece at start position.")
                            continue
                        
                        move_tuple = (start, end)
                        legal_moves = board.get_legal_moves()
                        if move_tuple not in legal_moves:
                            print("Illegal move. Try again.")
                            continue
                            
                        promotion = None
                        # Check for pawn promotion
                        if (
                            piece.lower() == 'p' and 
                            ((end[0] == 0 and board.current_player == 'white') or 
                             (end[0] == 7 and board.current_player == 'black'))
                        ):
                            promotion = input("Promote to (Q/R/B/N): ").upper()
                            if promotion not in ['Q', 'R', 'B', 'N']:
                                print("Invalid promotion piece.")
                                continue
                        
                        board.move_piece(start, end, promotion)
                        board.move_history.append((move, promotion))
                        break
                    except (ValueError, IndexError):
                        print("Invalid move format. Use algebraic notation (e.g., e2e4).")
                else:
                    print("Invalid move format. Use algebraic notation (e.g., e2e4).")
        else:
            # AI's move
            print("AI is thinking...")
            start, end = ai.get_best_move(board)
            move_notation = pos_to_notation(start) + pos_to_notation(end)
            promotion = None
            
            # Handle AI pawn promotion (always promote to queen)
            if (
                board.get_piece(start).lower() == 'p' and 
                ((end[0] == 0 and board.current_player == 'white') or 
                 (end[0] == 7 and board.current_player == 'black'))
            ):
                promotion = 'q' if board.current_player == 'black' else 'Q'
            
            board.move_piece(start, end, promotion)
            board.move_history.append((move_notation, promotion))
            print(f"AI moves: {move_notation}")
            if promotion:
                print(f"Promoted to {'Queen' if promotion.lower() == 'q' else promotion}")
        
        board.current_player = 'black' if board.current_player == 'white' else 'white'

if __name__ == "__main__":
    main()