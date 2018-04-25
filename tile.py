class Tile:
	""" data structure that contains tile metadata """

	def __init__(self, identifier, paths):
		self.identifier = identifier
		self.paths = paths

	def move_along_path(self, start, coordinates):
		for i, coor in enumerate(coordinates):
			if coor == start:
				start_path = i
		for path in self.paths:
			if path[0] == start_path:
				end_path = path[1]
			if path[1] == start_path:
				end_path = path[0]

		return coordinates[end_path]

	def rotate_tile(self):
		for path in self.paths:
			path[0] = (path[0] + 2)%8
			path[1] = (path[1] + 2)%8
			if path[0] > path[1]:
				path[0], path[1] = path[1], path[0]
