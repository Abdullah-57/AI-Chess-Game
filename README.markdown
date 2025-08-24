# Console-Based Chess Game with AI Opponent

This repository contains the implementation of a console-based chess game developed for **Applied Artificial Intelligence** Assignment 3 at FAST – National University of Computer & Emerging Sciences, Islamabad Campus. The game allows a human player (white) to compete against an AI opponent (black), supporting all standard chess rules, including castling, en passant, pawn promotion, checkmate, and stalemate.

## Project Overview

**Objective**: Develop a Python-based chess game with a human player interface and an AI opponent powered by the Minimax algorithm with alpha-beta pruning, adhering to standard chess rules and providing a user-friendly console experience.

**Course**: Applied Artificial Intelligence (Spring 2025)  
**Instructor**: Dr. Atif Jilani  
**Submitted by**: Abdullah Daoud (22I-2626)  
**Section**: SE-E  
**Institution**: FAST-NUCES, Islamabad Campus

## Features

### Board Initialization
- **ChessBoard Class**: Initializes an 8x8 board with standard starting positions (white pieces on ranks 1-2, black on 7-8).
- **Representation**: Uses uppercase (P, N, B, R, Q, K) for white, lowercase (p, n, b, r, q, k) for black, and '.' for empty squares.
- Tracks game state (current player, move history, en passant, castling, move counters).

### Move Generation
- Generates legal moves for pawns, knights, bishops, rooks, queens, and kings.
- Supports special moves: castling, en passant, and pawn promotion.
- Filters moves to prevent the king from being left in check.

### Move Execution
- Updates the board for standard and special moves (e.g., castling moves rook, en passant captures pawn).
- Handles pawn promotion with user choice (Q, R, B, N).
- Maintains castling availability, en passant targets, and move counters.

### Check and Game State Detection
- Detects check, checkmate, and stalemate conditions.
- Validates moves by checking if squares are under attack.

### AI Decision-Making
- **ChessAI Class**: Uses Minimax with alpha-beta pruning (depth 3) to select the best move.
- **Evaluation Function**: Scores based on material, center control, pawn structure, mobility, and king safety.
- Ensures competitive play for casual games.

### Game Loop and User Interaction
- Alternates between human (white) and AI (black) turns.
- Accepts moves in algebraic notation (e.g., e2e4).
- Provides clear error messages for invalid inputs and supports quitting.
- Displays the board and game statistics in a formatted console UI.

## Results
- **Correct Board Setup**: Initializes and displays the board with algebraic notation.
- **Move Validation**: Supports all chess moves, including special cases (e.g., Scholar’s Mate: e4, e5, Bc4, Qh5, Qf7#).
- **Game State Detection**: Accurately identifies check, checkmate, and stalemate.
- **AI Performance**: Responds to common openings and delivers checkmate in simple positions.
- **User Interaction**: User-friendly with clear prompts and error handling.
- **Robustness**: Handles edge cases (invalid inputs, promotions, draws) without crashing.

## Known Issues
- **Move Validation Efficiency**: Uses deep copies for move validation, which may slow down in complex positions.
- **AI Strength**: Limited to depth 3, potentially missing deeper tactics.
- **Halfmove Clock**: May need refinement for strict FIDE rule compliance.

## Project Structure
```plaintext
.
├── src/
│   ├── chess_board.py     # ChessBoard class for board and move logic
│   ├── chess_ai.py        # ChessAI class for Minimax and evaluation
│   ├── main.py            # Game loop and user interaction
│   └── utils.py           # Utility functions for notation and validation
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
```

## Installation

### Prerequisites
- **Python**: v3.8 or later

### Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/username/chess-game-ai.git
   cd chess-game-ai
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Game**:
   ```bash
   python src/main.py
   ```

## Usage
- Launch the game with `python src/main.py`.
- Enter moves in algebraic notation (e.g., e2e4) as the white player.
- The AI (black) responds automatically.
- Use prompts to select pawn promotion pieces or quit the game.
- View the board and game status after each move.

## Contributing
Contributions to improve AI strength or optimize performance are welcome:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
MIT License - see `LICENSE` for details.

## Contact
- **Author**: Abdullah Daoud (22I-2626)
- **Instructor**: Dr. Atif Jilani
- **Institution**: FAST-NUCES, Islamabad Campus