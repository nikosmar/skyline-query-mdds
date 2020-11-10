import math


class MinimumBoundingObject:
    def __init__(self, low, high):
        self.low = low
        self.high = high
        self.child = None


def minimum_bounding_object_calculator(points, dimensions):
    if type(points[0]) is MinimumBoundingObject:
        starting_index = 1
        ending_index = dimensions
        lower = [points[0].low[0]] + (dimensions - 1) * [float('inf')]
        upper = [points[-1].high[0]] + (dimensions - 1) * [float('-inf')]
    else:
        starting_index = 2
        ending_index = dimensions + 1
        lower = [points[0][1]] + (dimensions - 1) * [float('inf')]
        upper = [points[-1][1]] + (dimensions - 1) * [float('-inf')]

    if type(points[0]) is MinimumBoundingObject:
        for point in points:
            for i in range(starting_index, ending_index):
                if point.low[i] < lower[i]:
                    lower[i] = point.low[i]
                elif point.high[i] > upper[i]:
                    upper[i] = point.high[i]
    else:
        for point in points:
            for i in range(starting_index, ending_index):
                if point[i] < lower[i - 1]:
                    lower[i - 1] = point[i]
                elif point[i] > upper[i - 1]:
                    upper[i - 1] = point[i]

    return MinimumBoundingObject(lower, upper)


class Node:
    def __init__(self, items):
        self.items = items


class RTree:
    def create_rtree(self, points, dimensions):
        M = 4
        m = 2
        upper_level_items = []

        if 0 < len(points) % M < m:
            remaining_points = M + len(points) % M
            last_two_groups_length = [math.ceil(remaining_points / m), math.floor(remaining_points / m)]
        elif len(points) % M >= m:
            last_two_groups_length = [M, len(points) % M]
        else:
            if len(points) == M:
                last_two_groups_length = []
            else:
                last_two_groups_length = [M, M]

        for i in range(math.ceil((len(points) / M)) - 2):
            new_minimum_bounding_object = minimum_bounding_object_calculator(points[:M], dimensions)
            new_minimum_bounding_object.child = Node(points[:M])
            upper_level_items.append(new_minimum_bounding_object)
            del points[:M]

        for i in range(len(last_two_groups_length)):
            items_per_group = last_two_groups_length[i]
            new_minimum_bounding_object = minimum_bounding_object_calculator(points[:items_per_group], dimensions)
            new_minimum_bounding_object.child = Node(points[:items_per_group])
            upper_level_items.append(new_minimum_bounding_object)
            del points[:items_per_group]

        if len(upper_level_items) <= M:
            return Node(upper_level_items)
        else:
            return self.create_rtree(upper_level_items, dimensions)

    def query(self, root, bound_points, dimension):
        points = []
        current_node = root

        if type(current_node.items[0]) is not list:
            for item in current_node.items:
                if dimension == 2:
                    if bound_points[0] <= item.high[0] and bound_points[2] <= item.high[1]:
                        result = self.query(item.child, bound_points, dimension)
                        if result is not None:
                            points += result
                else:
                    if bound_points[0] <= item.high[0] and bound_points[2] <= item.high[1] and bound_points[4] <= item.high[2]:
                        result = self.query(item.child, bound_points, dimension)
                        if result is not None:
                            points += result
        else:
            for i in range(len(current_node.items)):
                if dimension == 2:
                    if bound_points[0] <= current_node.items[i][1] <= bound_points[1]:
                        if bound_points[2] <= current_node.items[i][2] <= bound_points[3]:
                            points.append(current_node.items[i])
                else:
                    if bound_points[0] <= current_node.items[i][1] <= bound_points[1]:
                        if bound_points[2] <= current_node.items[i][2] <= bound_points[3]:
                            if bound_points[4] <= current_node.items[i][3] <= bound_points[5]:
                                points.append((current_node.items[i]))
        if points:
            return points
        else:
            return
