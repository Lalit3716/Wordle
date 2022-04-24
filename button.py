import pygame

class Button:
	def __init__(self, pos, text, on_click=None, config={}):
		self.set_config(config)
		self.image = pygame.Surface(self.btn_size)
		self.rect = self.image.get_rect(center=pos)
		self.text = pygame.font.Font(None, self.text_size).render(text, True, self.text_color)
		self.text_rect = self.text.get_rect(center=self.rect.center)
		self.clicked = False
		self.on_click = on_click

	def set_config(self, config):
		self.btn_size = config.get("size") or (100, 40)
		self.bg_color = config.get("bg_color") or "green"
		self.text_size = config.get("text_size") or 30
		self.text_color = config.get("text_color") or "white"

	def detect_click(self):
		left_clk = pygame.mouse.get_pressed()[0]
		if left_clk and self.rect.collidepoint(pygame.mouse.get_pos()):
			if not self.clicked:
				if self.on_click:
					self.on_click()
				self.clicked = True
		else:
			self.clicked = False

	def draw(self, screen, status):
		if status == "on":
			pygame.draw.rect(screen, self.bg_color, self.rect)
		elif status == "off":
			pygame.draw.rect(screen, "#cccccc", self.rect)
		
		screen.blit(self.text, self.text_rect)

	def click(self):
		if self.on_click:
			self.on_click()

	def active(self, screen, status="on"):
		self.draw(screen, status)
		if status == "on":
			self.detect_click()
