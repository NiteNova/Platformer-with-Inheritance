import pygame
from pygame.math import Vector2
from pygame.rect import Rect
from pygame.surface import Surface
from pygame.color import Color
from enum import Enum


# config:
FRAMERATE = 60
SCREEN_SIZE = Vector2(1200, 800)

#CONSTANTS
GRAVITY = 10

JUMP_HEIGHT = 10
MOVE_SPEED = 20

# derived constants:
TILE_SIZE = SCREEN_SIZE[1] / 10

# pygame init:
pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Platformer Inheritance")


# definitions:
class GameState:
	# future class for storing progression data, such as powerups or current level
	pass
class GameObject:
	def update(
		self, 
		delta: float, 
		surface: Surface, 
		keys: pygame.key.ScancodeWrapper, 
		gameobjects: list["GameObject"]
	):
		pass

class Object2D(GameObject):
	def __init__(self, pos: Vector2, size: Vector2):
		self.pos = pos
		self.size = size

	def getRect(self) -> Rect:
		return Rect(self.pos, self.size)
	def draw(self):
		pass

class Player(Object2D):
	def __init__(self, pos: Vector2):
		super().__init__(pos, Vector2(TILE_SIZE, TILE_SIZE * 2))
		self.vel = Vector2(0, 0)

	def onGround(self, gameobjects: list[GameObject]) -> "TileType | None":
		for obj in gameobjects:
			if (
				isinstance(obj, Tile) 
				and obj.getRect().collidepoint(self.pos + Vector2(self.size.x / 2, self.size.y))
			):
				return obj.type
		return None



	def update(
		self, 
		delta: float, 
		surface: Surface, 
		keys: pygame.key.ScancodeWrapper, 
		gameobjects: list[GameObject]
	):
		if keys[pygame.K_UP]:
			self.vel.y = -JUMP_HEIGHT
		if keys[pygame.K_LEFT]:
			self.vel.x = -10
		elif keys[pygame.K_RIGHT]:
			self.vel.x = 10


class TileType(Enum):
	Ground = 0
	Ice = 1
	Bouncy = 2
	Gravity = 3
	Dream = 4

	def color(self) -> Color:
		match self:
			case self.Ground:
				return Color("#444444")
			case self.Ice:
				return Color("#b2dbe0")
			case self.Bouncy:
				return Color("#c050a4")
			case self.Gravity:
				return Color("#8235e7")
			case self.Dream:
				return Color("#47db91")

class Tile(Object2D):
	def __init__(self, pos: Vector2, type: TileType):
		super().__init__(pos, Vector2(TILE_SIZE, TILE_SIZE))
		self.type = type

	def update(
		self, 
		delta: float, 
		surface: Surface, 
		keys: pygame.key.ScancodeWrapper, 
		gameobjects: list[GameObject]
	):
		pygame.draw.rect(
			surface, 
			self.type.color(), 
			self.getRect()
		)


def main():
	# game setup:
	clock = pygame.time.Clock()
	
	gameobjs: list[GameObject] = []
	gameobjs.append(Player(Vector2(200, 750)))

	Link = pygame.image.load('link.png') #load your spritesheet
	Link.set_colorkey((255, 0, 255))


	# main loop:
	running = True
	while running:
		delta = clock.tick(FRAMERATE) / 1000

		# input:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
		keys = pygame.key.get_pressed()

		# draw:
		screen.fill("#000000")

		for obj in gameobjs:
			obj.update(delta, screen, keys, gameobjs)

		pygame.display.flip()

if __name__ == "__main__":
	main()