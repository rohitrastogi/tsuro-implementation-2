from position import Position
from copy import deepcopy

class Tile:
	""" data structure that contains tile metadata """

	def __init__(self, identifier, paths):
		self.identifier = identifier
		self.paths = paths

	def move_along_path(self, starting_position, square):
		start = starting_position.get_player_coordinates()
		coordinates = square.get_coordinates()

		for i, coor in enumerate(coordinates):
			if coor == start:
				start_path = i
		for path in self.paths:
			if path[0] == start_path:
				end_path = path[1]
			if path[1] == start_path:
				end_path = path[0]

		return Position(coordinates[end_path][0], coordinates[end_path][1], square)

	def rotate_tile(self):
		for path in self.paths:
			path[0] = (path[0] + 2)%8
			path[1] = (path[1] + 2)%8
			if path[0] > path[1]:
				path[0], path[1] = path[1], path[0]

		self.paths = sorted(self.paths)

	def symmetry(self):
		original_paths = deepcopy(self.paths)
		rotated_paths = [original_paths]
		for i in range(3):
			self.rotate_tile()
			if self.paths not in rotated_paths:
				rotated_paths.append(deepcopy(self.paths))

		self.rotate_tile()
		sym = len(rotated_paths)

		return sym
