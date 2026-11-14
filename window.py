from cv2.typing import MatLike
import pygame
import numpy as np
import cv2


class Window:
	def __init__(
		self,
		text: str = "",
		color: str = "white",
		bg: str = "black",
		size: int = 200,
		window_width: int = 1600,
		window_height: int = 600,
	) -> None:
		pygame.init()
		self.screen = pygame.display.set_mode((window_width, window_height))
		self.font = pygame.font.Font(None, size)
		self.bg = bg
		self.text = text
		self.color = color
		self.frame_surface = None

	def update_text(self, text: str, color: str = "white") -> None:
		self.text = text
		self.color = color

	def set_frame(self, bgr_image: MatLike) -> None:
		# OpenCV is BGR, pygame wants RGB
		rgb = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
		# numpy is (height, width, channels); pygame surfarray is (width, height, channels)
		self.frame_surface = pygame.surfarray.make_surface(np.swapaxes(rgb, 0, 1))

	def update(self) -> None:
		pygame.event.pump()
		self.screen.fill(self.bg)

		if self.frame_surface is not None:
			self.screen.blit(self.frame_surface, (10, 10))

		img = self.font.render(self.text, True, self.color)
		self.screen.blit(img, img.get_rect(center=self.screen.get_rect().center))

		pygame.display.flip()
