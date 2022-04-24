import pygame
from random import choice
from string import ascii_letters
import requests as request
import numpy as np
from button import Button

# Init pygame
pygame.init()

# Basic Game Setup
WINDOW_SIZE = 1280, 720
FPS = 60
RANDOM_WORDS = ["DOCTOR"]

# Pygame setup
screen = pygame.display.set_mode(WINDOW_SIZE)
clock = pygame.time.Clock()

# Heading
font = pygame.font.Font(None, 50)
heading = font.render("Wordle", True, "#ffffff")
heading_pos = heading.get_rect(center=(WINDOW_SIZE[0]/2, 50))

class Game:
	def __init__(self):
		# Word Setup
		self.word = choice(RANDOM_WORDS)
		self.word_freq_map = dict.fromkeys(self.word, 0)
		for w in self.word:
			self.word_freq_map[w] += 1

		# General Setup
		self.grid = np.full((len(self.word), len(self.word) + 1), None, dtype=object)
		self.grid_colors = np.full(self.grid.shape, None, dtype=object)
		self.grid_values = np.zeros(self.grid.shape, dtype=str)
		self.active_row = 0
		self.active_cell = 0
		self.button_status = "off"
		self.won = False
		self.loose = False
		self.create_grid()

		# Font Setup
		self.font = pygame.font.Font(None, 40)
		self.win_surf = self.font.render("You Won", True, "white")
		self.loose_surf = self.font.render("You Lost", True, "white")

		# Button
		button_pos = WINDOW_SIZE[0]/2 + 400, WINDOW_SIZE[1] / 2
		self.button = Button(button_pos, "Continue", on_click=self.on_btn_click)

	def create_grid(self):
		size = 80
		mid_offset = len(self.word) // 2
		include_half = 1 if len(self.word) % 2 == 1 else 0
		offset_x = (WINDOW_SIZE[0] / 2) - (size * mid_offset) - (size / 2) * include_half
		offset_y = (WINDOW_SIZE[1] / 2) - (size * mid_offset) - (size / 2) * include_half
		for ix, iy in np.ndindex(self.grid.shape):
			pos = offset_x + size * ix, offset_y + size * iy
			rect = pygame.Rect(pos, (size, size))
			self.grid[ix, iy] = rect

	def take_input(self, event):

		if event.key == pygame.K_RETURN:
			if self.active_row >= self.grid.shape[1] or self.won:
				self.__init__()
			elif self.button_status == "on":
				self.button.click()

		if self.won: return

		if self.active_cell < len(self.word):
			if event.unicode in ascii_letters and event.unicode != "":
				self.grid_values[self.active_cell, self.active_row] = event.unicode.upper()
				if self.active_cell < len(self.word):
					self.active_cell += 1

		if event.key == pygame.K_BACKSPACE:
			if self.active_cell > 0:
				self.grid_values[self.active_cell - 1, self.active_row] = ""
				self.active_cell -= 1

		if self.active_cell == len(self.word):
			self.button_status = "on"
		else:
			self.button_status = "off"

	def draw_grid(self):
		for ix, iy in np.ndindex(self.grid.shape):
			if x := self.grid_colors[ix, iy]:
				pygame.draw.rect(screen, x, self.grid[ix, iy])
			color = "green" if self.active_row == iy else "white"
			pygame.draw.rect(screen, color, self.grid[ix, iy], 1)

	def draw_grid_values(self):
		for ix, iy in np.ndindex(self.grid_values.shape):
			if (x := self.grid_values[ix, iy]) != 0:
				surf = self.font.render(x, True, "#ffffff")
				pos = surf.get_rect(center=self.grid[ix, iy].center)
				screen.blit(surf, pos)

	def on_btn_click(self):
		self.check_move()
		self.button_status = "off"
		if not self.won:
			if self.active_row <= self.grid.shape[1] - 1:
				self.active_row += 1
				self.active_cell = 0
			else:
				self.loose = True

	def show_win_loose(self):
		if self.won:
			rect = self.win_surf.get_rect(center=(WINDOW_SIZE[0]/2, 100))
			screen.blit(self.win_surf, rect)

		if self.loose:
			rect = self.loose_surf.get_rect(center=(WINDOW_SIZE[0]/2, 100))
			screen.blit(self.loose_surf, rect)

	def check_move(self):
		guessed_word = "".join(self.grid_values[:, self.active_row]).upper()
		guessed_freq_map = dict.fromkeys(guessed_word, 0)
		marked_green = dict.fromkeys(self.word, False)
		for i, letter in enumerate(self.word):
			if guessed_word[i] == letter:
				self.grid_colors[i, self.active_row] = "green"
				guessed_freq_map[letter] += 1
				marked_green[letter] = True
			elif guessed_word[i] in self.word:
				if not marked_green[guessed_word[i]]:
					if guessed_freq_map[guessed_word[i]] < self.word_freq_map[guessed_word[i]]:
						self.grid_colors[i, self.active_row] = "#c9c11e"
						guessed_freq_map[guessed_word[i]] += 1
				else:
					if guessed_freq_map[guessed_word[i]] < self.word_freq_map[guessed_word[i]]:
						self.grid_colors[i, self.active_row] = "#c9c11e"
						guessed_freq_map[guessed_word[i]] += 1

		for i, color in enumerate(self.grid_colors[:, self.active_row]):
			if color == "#c9c11e":
				l = guessed_word[i]
				if guessed_freq_map[l] > self.word_freq_map[l] and marked_green[l]:
					self.grid_colors[i, self.active_row] = None

		colors = self.grid_colors[:, self.active_row]
		self.won = all([True if c == "green" else False for c in colors])

	def run(self):
		# Grid
		self.draw_grid()
		self.draw_grid_values()
		
		# Button
		self.button.active(screen, self.button_status)

		# Win/Loss Status :)
		self.show_win_loose()

game = Game()

while True:
	screen.fill("black")
	screen.blit(heading, heading_pos)
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			exit()
		if event.type == pygame.KEYDOWN:
			game.take_input(event)

	game.run()

	pygame.display.update()
	clock.tick(FPS)
