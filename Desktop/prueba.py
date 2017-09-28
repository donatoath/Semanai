import os
import random
import time
from abc import ABCMeta, abstractmethod

width = 7
height = 6
iJugadores = [1 , 2]
jugador = 0

class LetsPlay(object):
	width = 7
	height = 6
	board = [[0 for y in range(height)]for x in range (width)]
	currentPlayer = None
	players = [None, None]
	gameFinished = False
	_numberPlayer = iJugadores

	def __init__(self):
		if jugador != 1:
			self.players[0] = _HumanP(self._numberPlayer[0]) 
			self.players[1] = _IA(self._numberPlayer[1])
		else:
			self.players[0] = _IA(self._numberPlayer[0]) 
			self.players[1] = _HumanP(self._numberPlayer[1])

	def start(self):
		while not self.gameFinished:
			self._next_move()

	def start_new(self):
		self.currentPlayer = self.players[jugador]
		self.start()

	def _switch_player(self):
		if self.currentPlayer == self.players[0]:
			self.currentPlayer = self.players[1]
		else:
			self.currentPlayer = self.players[0]

	def _next_move(self):
		column = self.currentPlayer.get_move(self.board)
		for i in range(self.height -1, -1, -1):
			if self.board[i][column] == 0:
				self.board[i][column] = self.currentPlayer._number
				self._switch_player()
				return
		print("This column is full. Please choose an other column")
		return

class _Player(object):
	global board, width, height
	metalclass = ABCMeta
	type1 = None
	_number = None

	def __init__(self, number):
		self._number = number

	@abstractmethod
	def get_move(self, board):
		pass

class _HumanP(_Player):
	global board, width, height

	def __init__(self, number):
		super(_HumanP, self).__init__(number)
		self.type1 = "Human"

	def get_move(self, board):
		column = None
		while column == None:
			try:
				column = int(input("Your turn: ")) -1
			except ValueError:
				column = None
			if 0 <= column <= 6:
				return column
			else:
				column = None
				print("Please, enter a number between 1 and 6")

class _IA(_Player):

	global board, width, height
	_Dificulty = 5

	def __init__(self, number):
		super(_IA, self).__init__(number)
		self.type1 = "IA"

	def get_move(self, board):
		return self._get_best_move(board)

	def _get_best_move(self, board):
		if self._number == iJugadores[0]:
			human_number = iJugadores[1]
		else:
			human_number = iJugadores[0]
		legal_moves = {}
		for col in range(width):
			if self._is_legal_move(col, board):
				tmp_board = self._simulate_move(board, col, self._number)
				legal_moves[col] = -self._find(self._Dificulty - 1, tmp_board, human_number)
		best_alpha = -99999999
		best_move = None
		moves = legal_moves.items()
		for move, alpha in moves:
			if alpha >= best_alpha:
				best_alpha = alpha
				best_move = move
		return best_move

	def _find(self, depth, board, player_number):
		legal_moves = []
		for i in range(height):
			if self._is_legal_move(i, board):
				tmp_board = self._simulate_move(board, i, player_number)
				legal_moves.append(tmp_board)
			if depth == 0 or len(legal_moves) == 0 or self._game_is_over(board):
				return self._eval_game(depth, board, player_number)
		if player_number == iJugadores[0]:
			opp_player_number = iJugadores[1]
		else:
			opp_player_number = iJugadores[0]
		alpha = -99999999
		for child in legal_moves:
			if child == None:
				print("child == None (search)")
			alpha = max(alpha, -self._find(depth - 1, child, opp_player_number))
		return alpha

	def _is_legal_move(self, column, board):
		for i in range(height -1, -1, -1):
			if board[i][column] == 0:
				return True
		return False

	def _game_is_over(self, board):
		if self._find_streak(board, iJugadores[0], 4) > 0:
			return True
		elif self._find_streak(board, iJugadores[1], 4) > 0:
			return True
		else:
			return False

	def _simulate_move(self, board, column, number):
		tmp_board = [x[:] for x in board]
		for i in range(height -1, -1, -1):
			if tmp_board[i][column] == 0:
				tmp_board[i][column] = number
				return tmp_board

def main():
	global board, width, height
	letplay = LetsPlay()
	jugador = input("Quien va a Empezar? (1) o (2)")
	bAux = False
	iAux = 0
	while bAux == False:
		letplay.start_new()
		iAux = input("Volver a Jugar? (1) Si (2) No")
		if iAux == 1:
			bAux = False
		else:
			bAux = True

main()