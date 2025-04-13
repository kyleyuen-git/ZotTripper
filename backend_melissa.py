from math import sin, cos, sqrt, atan2, pi

class Backend:
    def __init__(self, start, points):
        self.points = points
        self.start = start
        self.shortest_route = []
        self.min_dist = float('inf')

    def get_distance(self, p1, p2) -> None:
        R = 3959
        dLat = ((p2[0] - p1[0]) * pi) / 180
        dLng = ((p2[1] - p1[1]) * pi) / 180
        a = sin(dLat / 2) ** 2 + cos(p1[0] * pi / 180) * cos(p2[0] * pi / 180) * sin(dLng / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def create_distance_matrix(self) -> None:
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

    def three_opt(self) -> None:
        n = len(self.shortest_route)
        worked = False
        for i in range(1, n - 5):
            for j in range(i + 2, n - 3):
                for k in range(j + 2, n - 1):
                    seg1 = self.shortest_route[:i + 1]
                    seg2 = self.shortest_route[i + 1:j + 1]
                    seg3 = self.shortest_route[j + 1:k + 1]
                    seg4 = self.shortest_route[k + 1:]

                    new_routes = [seg1 + seg2[::-1] + seg3[::-1] + seg4,
                                  seg1 + seg2[::-1] + seg3 + seg4,
                                  seg1 + seg2 + seg3[::-1] + seg4,
                                  seg1 + seg3 + seg2 + seg4,
                                  seg1 + seg3 + seg2[::-1] + seg4,
                                  seg1 + seg3[::-1] + seg2 + seg4,
                                  seg1 + seg3[::-1] + seg2[::-1] + seg4
                    ]
                    new_dist = [((self.distances[seg1[-1]][seg2[-1]] + self.distances[seg2[0]][seg3[-1]] + self.distances[seg3[0]][seg4[0]])
                                    - (self.distances[seg3[-1]][seg4[0]] + self.distances[seg2[-1]][seg3[0]] + self.distances[seg1[-1]][seg2[0]])),
                                ((self.distances[seg1[-1]][seg2[-1]] + self.distances[seg2[0]][seg3[0]]) - (self.distances[seg1[-1]][seg2[0]] + self.distances[seg2[-1]][seg3[0]])),
                                ((self.distances[seg2[-1]][seg3[-1]] + self.distances[seg3[0]][seg4[0]]) - (self.distances[seg2[-1]][seg3[0]] + self.distances[seg3[-1]][seg4[0]])),
                                ((self.distances[seg1[-1]][seg3[0]] + self.distances[seg3[-1]][seg2[0]] + self.distances[seg2[-1]][seg4[0]])
                                    - (self.distances[seg1[-1]][seg2[0]] + self.distances[seg2[-1]][seg3[0]] + self.distances[seg3[-1]][seg4[0]])),
                                ((self.distances[seg1[-1]][seg3[0]] + self.distances[seg3[-1]][seg2[-1]] + self.distances[seg2[0]][seg4[0]])
                                    - (self.distances[seg1[-1]][seg2[0]] + self.distances[seg2[-1]][seg3[0]] + self.distances[seg3[-1]][seg4[0]])),
                                ((self.distances[seg1[-1]][seg3[0]] + self.distances[seg3[0]][seg2[0]] + self.distances[seg2[-1]][seg4[0]])
                                    - (self.distances[seg1[-1]][seg2[0]] + self.distances[seg2[-1]][seg3[0]] + self.distances[seg3[-1]][seg4[0]])),
                                ((self.distances[seg1[-1]][seg3[-1]] + self.distances[seg2[0]][seg4[0]]) - (self.distances[seg1[-1]][seg2[0]] + self.distances[seg3[-1]][seg4[0]]))
                    ]
                    min_d = 0
                    min_element = -1
                    for index in range(len(new_dist)):
                        if (new_dist[index] < 0) & (new_dist[index] < min_d):
                            min_d = new_dist[index]
                            min_element = index

                    if min_d == 0:
                        continue
                    else:
                        new_d = self.calculate_dist(new_routes[min_element])
                        if new_d < self.min_dist:
                            self.min_dist = new_d
                            self.shortest_route = new_routes[min_element]

    def calculate_dist(self, route) -> float:
        total_dist = 0
        for i in range(len(route) - 1):
            total_dist += self.distances[route[i]][route[i + 1]]
        return total_dist

    def iterative_opt(self) -> None:
        self.three_opt()
        result = True
        while result:
            result = self.two_opt()

    def greedy_search(self) -> None:
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
