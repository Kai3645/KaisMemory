import sys, pygame

import numpy as np

pygame.init()

size = w, h = 1080, 720

screen = pygame.display.set_mode(size)

while True:
	event = pygame.event.poll()
	print(event)
	if event.type == pygame.QUIT: break

	img = np.random.random((h, w, 3)) * 255
	img = pygame.surfarray.make_surface(img)

	screen.blit(img, (0, 0))
	pygame.display.update()

pygame.quit()
sys.exit()
