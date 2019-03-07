import pygame
import sys
import random

pygame.init()	#initialize python

WIDTH = 800
HEIGHT = 600

bg_color = (0,0,0)

RED = (255, 0 , 0)			#variable with RGB value for RED
BLUE = (0,0,255)

player_size = 30
player_pos = [WIDTH/2, HEIGHT-2*player_size]

enemy_size = 50
enemy_pos = [random.randint(0, WIDTH), 0]
enemy_list = [enemy_pos]
SPEED = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))	#create screen with size 800x600

game_over = False						#set new boolean for game over event to false

score = 0								#initialize score to 0
myFont = pygame.font.SysFont("calibri", 35)
clock = pygame.time.Clock()

def set_level(score, SPEED):
	if score < 50:
		speed = 5
	elif score < 100:
		speed = 10
	elif score < 150:
		speed = 15
	elif score > 200:
		speed = 25		
	return SPEED	



def drop_enemies(enemy_list):
	delay = random.random()
	if len(enemy_list) < 10 and delay < 0.3:
		x_pos = random.randint(0, WIDTH - enemy_size)
		y_pos = 0
		enemy_list.append([x_pos, y_pos])


def draw_enemies(enemy_list):
	for enemy_pos in enemy_list:
		pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))


def update_enemy_positions(enemy_list, score):
	for idx, enemy_pos in enumerate(enemy_list):
		#updating position of enemy
		if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
			enemy_pos[1] += SPEED
		else:
			enemy_list.pop(idx)
			score += 1
	return score
			
def collision_check(enemy_list, player_pos):
	for enemy_pos in enemy_list:
		if detect_collision(enemy_pos, player_pos):
			return True
	return False		



def detect_collision(player_pos, enemy_pos):			#detects enemy collision with player
	p_x = player_pos[0]
	p_y = player_pos[1]

	e_x = enemy_pos[0]
	e_y = enemy_pos[1]

	if (e_x >= p_x and e_x < (p_x + player_size)) or (p_x >= e_x and p_x < (e_x + enemy_size)):
		if (e_y >= p_y and e_y < (p_y + player_size)) or (p_y >= e_y and p_y < (e_y + enemy_size)):
			return True
	return False	

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()					#ability to exit game with button

	if event.type == pygame.KEYDOWN:

		x = player_pos[0]
		y = player_pos[1]

		if event.key == pygame.K_LEFT:
			x -= player_size
		elif event.key == pygame.K_RIGHT:
			x += player_size


		player_pos = [x,y]

	screen.fill(bg_color)

	

	if detect_collision(player_pos, enemy_pos):
		game_over = True

	draw_enemies(enemy_list)
	score = update_enemy_positions(enemy_list, score)
	SPEED = set_level(score, SPEED)
	
	text = "Score: " + str(score)
	label = myFont.render(text, 1, (255,255,255))
	screen.blit(label, (WIDTH - 200, HEIGHT - 40))

	if collision_check(enemy_list, player_pos):
		game_over = True
		break

	drop_enemies(enemy_list)

	pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], player_size, player_size))

	clock.tick(30)

	pygame.display.update()					#update pygame to show changes

