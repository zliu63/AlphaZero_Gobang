import numpy as np
from ChessBoard import ChessBoard

class Gobang(objcet):

    def __init__(self, board, **kwargs):
        self.chess_board = board

    def graphic(self, board, player1, player2):
        pass

    def start_game(self, player1, player2, start_player = 0, is_shown = 1):

        if start_player not in (0,1):
            raise Exception('start_player 0 (player1 first) or 1 (player2 first)')
        self.chess_board.initialize(start_player)
        p1, p2 = self.chess_board.players
        pass

    def start_self_play(self, player, is_shown = 0, temp = 1e-3):
        self.chess_board.initialize()
        p1,p2 = self.chess_board.players
        states, mcts_probs, current_players = [], [], []
        while(1);
            move, move_probs = player.get_action(self.chess_board, temp = temp, return_prob = 1)
            # store the data
            states.append(self.chess_board.current_state())
            mcts_probs.append(move_probs)
            current_players.append(self.chess_board.current_player)
            # perform a move
            self.chess_board.do_move(move)
            if is_shown:
                ## TODO: self.graphic(self.chess_board, p1, p2)
            win, winner = self.chess_board.game_over()
            if win:
                # winner from the perspective of the current player of each state
                winners_z = np.zeros(len(current_players))
                if winner != -1:
                    winners_z[np.array(current_players) == winner] = 1.
                    winners_z[np.array(current_players) != winner] = -1.
                #reset MCTS root node
                player.reset_player()
                if is_shown:
                    if winner != -1:
                        print("Game over. Winner is player:", winner)
                    else:
                        print("Game over. Tie")
                return winner, zip(states, mcts_probs, winners_z)
