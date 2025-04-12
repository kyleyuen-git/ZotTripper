from math import acos, sin, cos

class Backend:
    def __init__(self, start, points):
        self.points = points
        self.start = start
        self.shortest_route = []
        self.min_dist = float('inf')

    def get_distance(self, p1, p2):
        return 3959 * acos(sin(p1[0]) * sin(p2[0]) + cos(p1[0]) * cos(p2[0]) * cos(p2[1] - p1[1]))

    def create_distance_matrix(self):
        n = len(self.points)
        self.distances = []
        for i in range(n):
            self.distances.append([])
            for j in range(n):
                self.distances[i].append(0)

        for i in range(n):
            for j in range(i + 1, n):
                distance = self.get_distance(self.points[i], self.points[j])
                self.distances[i][j] = self.distances[j][i] = distance

    def two_opt(self) -> bool:
        n = len(self.shortest_route)
        worked = False
        for i in range(1, n - 2):
            for j in range(i + 2, n - 1):
                new_route = (self.shortest_route[:i]
                             + self.shortest_route[i: j + 1][::-1]
                             + self.shortest_route[j + 1:])
                new_dist = self.calculate_dist(new_route)

                if new_dist < self.min_dist:
                    self.min_dist = new_dist
                    self.shortest_route = new_route
                    worked = True
        return worked

    def three_opt(self) -> bool:
        n = len(self.shortest_route)
        worked = False
        for i in range(1, n - 3):
            j = i + 2
            k = n - 2
            moved = True
            while j < k - 1:
                new_route = (self.shortest_route[:i]
                            + self.shortest_route[i: j + 1][::-1]
                            + self.shortest_route[j + 1: k + 1][::-1]
                            + self.shortest_route[k + 1:])
                new_dist = self.calculate_dist(new_route)
                if new_dist < self.min_dist:
                    self.min_dist = new_dist
                    self.shortest_route = new_route
                    worked = True

                if moved:
                    j += 1
                    moved = False
                else:
                    k -= 1
                    moved = True
        return worked

    def four_opt(self) -> bool:
        n = len(self.shortest_route)
        worked = False
        for i in range(1, n - 4):
            j = i + 2
            x = n - 2
            k = (x + j) // 2
            moved = True
            while j < k - 1 & k < x - 1:
                new_route = (self.shortest_route[:i]
                             + self.shortest_route[i: j + 1][::-1]
                             + self.shortest_route[j + 1: k + 1][::-1]
                             + self.shortest_route[k + 1: x + 1][::-1]
                             + self.shortest_route[x + 1:])
                new_dist = self.calculate_dist(new_route)
                if new_dist < self.min_dist:
                    self.min_dist = new_dist
                    self.shortest_route = new_route
                    worked = True

                if moved:
                    j += 1
                    moved = False
                else:
                    x -= 1
                    moved = True
        return worked

    def calculate_dist(self, route):
        total_dist = 0
        for i in range(len(route) - 1):
            total_dist += self.distances[route[i]][route[i + 1]]
        return total_dist

    def iterative_opt(self):
        result = True
        while result:
            if (self.two_opt()):
                continue
            else:
                result = False
        result = True
        while result:
            if (self.three_opt()):
                continue
            else:
                result = False
        result = True
        while result:
            if (self.four_opt()):
                continue
            else:
                result = False

    def greedy_search(self):
        num_points = len(self.distances)
        visited = [False] * num_points
        visited[self.start] = True
        last = self.start
        self.shortest_route.append(self.start)
        total_dist = 0

        for i in range(1, len(self.distances)):
            min = float('inf')
            temp_last = last
            for j in range(len(self.distances[last])):
                if (self.distances[last][j] < min) & (not visited[j]):
                    min = self.distances[last][j]
                    temp_last = j
                else:
                    continue
            self.shortest_route.append(temp_last)
            visited[temp_last] = True
            last = temp_last
            total_dist += min
        self.shortest_route.append(0)
        self.min_dist = total_dist + self.distances[last][self.start]

if __name__ == '__main__':
    points = []
    addresses = []
    with open("Addresses.csv", 'r') as file:
        first = True
        for line in file.readlines():
            if first:
                first = False
                continue
            container = line.split(',')
            tup = float(container[1]), float(container[2].strip('\n'))
            points.append(tup)
            addresses.append(container[0])

    b = Backend(0, points)
    b.create_distance_matrix()
    b.greedy_search()
    b.iterative_opt()
    print("Route: ", end = '')
    for p in b.shortest_route:
        print(addresses[p], end=' -> ')
    print()
    print("Total distance: ", b.min_dist, " miles")