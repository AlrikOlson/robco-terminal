import heapq
import random


class Vault:
    WALL = 0
    FLOOR = 1
    START = 2
    EXIT = 3
    DOOR = 4
    ATRIUM = 5
    HALLWAY = 6

    def __init__(self, width, height, cell_size):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.layout = [[self.WALL for _ in range(width)] for _ in range(height)]
        self.start_pos = None
        self.exit_pos = None
        self.rooms = []
        self._generate_vault()

    def _generate_vault(self):
        self._create_outer_walls()
        self._create_atrium()
        self._generate_rooms()
        self._connect_rooms()
        self._create_start_pos()
        self._create_exit()

    def _create_outer_walls(self):
        for x in range(self.width):
            self.layout[0][x] = self.WALL
            self.layout[self.height - 1][x] = self.WALL
        for y in range(self.height):
            self.layout[y][0] = self.WALL
            self.layout[y][self.width - 1] = self.WALL

    def _create_atrium(self):
        atrium_width = self.width // 3
        atrium_height = self.height // 3
        atrium_x = (self.width - atrium_width) // 2
        atrium_y = (self.height - atrium_height) // 2
        self._create_room(atrium_x, atrium_y, atrium_width, atrium_height, self.ATRIUM)
        self.rooms.append((atrium_x, atrium_y, atrium_width, atrium_height))

    def _generate_rooms(self):
        min_room_size = 4
        max_room_size = min(self.width // 5, self.height // 5)
        num_rooms = random.randint(10, 18)
        attempts = 0
        max_attempts = 100

        while len(self.rooms) < num_rooms and attempts < max_attempts:
            x = random.randint(1, self.width - max_room_size - 1)
            y = random.randint(1, self.height - max_room_size - 1)
            width = random.randint(min_room_size, max_room_size)
            height = random.randint(min_room_size, max_room_size)

            if self._is_valid_room_position(x, y, width, height):
                self._create_room(x, y, width, height, self.FLOOR)
                self.rooms.append((x, y, width, height))
            attempts += 1

    def _is_valid_room_position(self, x, y, width, height):
        if x + width >= self.width - 1 or y + height >= self.height - 1:
            return False

        for i in range(y - 1, y + height + 1):
            for j in range(x - 1, x + width + 1):
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.layout[i][j] != self.WALL:
                        return False

        return True

    def _connect_rooms(self):
        # Use Prim's Algorithm to generate a Minimum Spanning Tree (MST) connecting all rooms
        num_rooms = len(self.rooms)
        connected = [False] * num_rooms
        connected_to_atrium = [False] * num_rooms
        priority_queue = [(0, 0, 0)]  # (cost, room_index, previous_room_index)
        mst_edges = []

        while priority_queue:
            cost, room_index, prev_room_index = heapq.heappop(priority_queue)
            if not connected[room_index]:
                connected[room_index] = True
                if room_index != prev_room_index:
                    mst_edges.append((room_index, prev_room_index))

                for i in range(num_rooms):
                    if not connected[i]:
                        distance = self._room_distance(
                            self.rooms[room_index], self.rooms[i]
                        )
                        heapq.heappush(priority_queue, (distance, i, room_index))

        # Connect the atrium to the closest 3 unique adjacent rooms
        atrium_index = 0
        atrium_connections = 0

        while atrium_connections < 3:
            closest_room_index = None
            min_distance = float("inf")

            for i in range(1, num_rooms):
                if not connected_to_atrium[i]:
                    distance = self._room_distance(
                        self.rooms[atrium_index], self.rooms[i]
                    )
                    if distance < min_distance:
                        min_distance = distance
                        closest_room_index = i

            if closest_room_index is not None:
                mst_edges.append((atrium_index, closest_room_index))
                connected_to_atrium[closest_room_index] = True
                atrium_connections += 1

        for room1_index, room2_index in mst_edges:
            self._create_l_shaped_hallway(
                self.rooms[room1_index], self.rooms[room2_index]
            )

    def _room_distance(self, room1, room2):
        x1, y1, w1, h1 = room1
        x2, y2, w2, h2 = room2
        center_x1, center_y1 = x1 + w1 // 2, y1 + h1 // 2
        center_x2, center_y2 = x2 + w2 // 2, y2 + h2 // 2
        return abs(center_x1 - center_x2) + abs(center_y1 - center_y2)

    def _create_l_shaped_hallway(self, room1, room2):
        x1, y1, w1, h1 = room1
        x2, y2, w2, h2 = room2
        start_x, start_y = x1 + w1 // 2, y1 + h1 // 2
        end_x, end_y = x2 + w2 // 2, y2 + h2 // 2

        corner_x, corner_y = start_x, end_y

        # Now, hallways are two cells wide
        self._create_hallway_segment(start_x, start_y, corner_x, corner_y)
        self._create_hallway_segment(corner_x, corner_y, end_x, end_y)

    def _create_hallway_segment(self, start_x, start_y, end_x, end_y):
        hallway_width = 2  # Making the hallway two cells wide for width
        if start_x == end_x:
            step = 1 if end_y > start_y else -1
            for y in range(start_y, end_y, step):
                for w in range(hallway_width):
                    if 0 <= start_x + w < self.width:
                        self.layout[y][start_x + w] = self.HALLWAY
        else:
            step = 1 if end_x > start_x else -1
            for x in range(start_x, end_x, step):
                for w in range(hallway_width):
                    if 0 <= start_y + w < self.height:
                        self.layout[start_y + w][x] = self.HALLWAY

    def _create_start_pos(self):
        self.start_pos = self._find_empty_cell()
        self.layout[self.start_pos[1]][self.start_pos[0]] = self.START

    def _create_exit(self):
        self.exit_pos = self._find_empty_cell()
        self.layout[self.exit_pos[1]][self.exit_pos[0]] = self.EXIT

    def _create_room(self, x, y, width, height, room_type):
        for i in range(y, y + height):
            for j in range(x, x + width):
                self.layout[i][j] = room_type

    def _find_empty_cell(self):
        while True:
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if self.layout[y][x] == self.FLOOR:
                return x, y

    def is_wall(self, x, y):
        return self.layout[y][x] == self.WALL

    def is_valid_move(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.layout[y][x] in [self.FLOOR, self.EXIT, self.DOOR, self.HALLWAY]
        return False

    def is_exit(self, x, y):
        return (x, y) == self.exit_pos
