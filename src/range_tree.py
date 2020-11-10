import sys


class Leaf:
    def __init__(self, value, linked_tree):
        self.data = value
        self.next = None
        self.previous = None
        self.linked_tree = linked_tree


class Node:
    def __init__(self, value, left, right, linked_tree):
        self.data = value
        self.left = left
        self.right = right
        self.linked_tree = linked_tree


class RangeTree:
    def create_tree(self, data, dimension, last_leaf=None):
        middle = len(data) // 2 + len(data) % 2
        linked_tree = None

        if len(data[0]) - 1 > dimension:
            linked_tree, _ = self.create_tree(sorted(data, key=lambda x:
                                              x[dimension + 1]), dimension + 1)

        if len(data) == 1:
            new_leaf = Leaf(data[0], linked_tree)
            return new_leaf, new_leaf

        left, last_left_leaf = self.create_tree(data[:middle], dimension, last_leaf)
        right, last_right_leaf = self.create_tree(data[middle:], dimension, last_left_leaf)

        root = Node(data[middle - 1][dimension], left, right, linked_tree)

        if type(right) is Leaf:
            last_left_leaf.next = last_right_leaf
            last_right_leaf.previous = last_left_leaf

        if last_leaf is not None and last_leaf.next is None:
            last_leaf.next = last_left_leaf
            last_left_leaf.previous = last_leaf

        return root, last_right_leaf

    # a basic Pre-Order traverse method
    def traverse(self, node):
        if node is not None:
            print(node.data)
            if type(node) is not Leaf:
                self.traverse(node.left)
                self.traverse(node.right)

    def list_traverse(self, node):
        while type(node) is not Leaf:
            node = node.left

        while node is not None:
            print(node.data)
            node = node.next

    def list_reverse_traverse(self, node):
        while type(node) is not Leaf:
            node = node.right

        while node is not None:
            print(node.data)
            node = node.previous

    @staticmethod
    def find_split_node(current_node, lower_bound, upper_bound):
        while type(current_node) is not Leaf:
            if lower_bound <= current_node.data and upper_bound <= current_node.data:
                current_node = current_node.left
            elif lower_bound > current_node.data and upper_bound > current_node.data:
                current_node = current_node.right
            else:
                break

        if type(current_node) is Leaf:
            print("No items found within range.")
            sys.exit()

        return current_node

    def query_1d(self, root, low, high, dimension):
        points = []

        split_node = self.find_split_node(root, low, high)

        if type(split_node) is Leaf:
            if low <= split_node.data[dimension] <= high:
                return [split_node.data]
            else:
                return []

        left_path = split_node.left
        right_path = split_node.right

        # find the left (low) bound
        while type(left_path) is not Leaf:
            if low <= left_path.data:
                left_path = left_path.left
            else:
                left_path = left_path.right

        # check if the found leaf is within range
        if not low <= left_path.data[dimension] <= high:
            left_path = left_path.next

        # find the right (high) bound
        while type(right_path) is not Leaf:
            if high <= right_path.data:
                right_path = right_path.left
            else:
                right_path = right_path.right

        # check if the found leaf is within range
        if not low <= right_path.data[dimension] <= high:
            right_path = right_path.previous

        # create the list of the points found within [low, high]
        while left_path != right_path.next:
            points.append(left_path.data)
            left_path = left_path.next

        return points

    def query_2d(self, root, d0_low, d0_high, d1_low, d1_high, dimension):
        points = []

        split_node = self.find_split_node(root, d0_low, d0_high)

        if type(split_node) is Leaf:
            if (d0_low <= split_node.data[dimension] <= d0_high
                    and d1_low <= split_node.data[dimension + 1] <= d1_high):
                return split_node.data

        left_path = split_node.left
        right_path = split_node.right

        # call the 1D query method for the left path
        while type(left_path) is not Leaf:
            if d0_low <= left_path.data:
                if type(left_path.right) is Node:
                    points += self.query_1d(left_path.right.linked_tree, d1_low, d1_high, dimension + 1)
                elif type(left_path.right) is Leaf:
                    if d1_low <= left_path.right.data[-1] <= d1_high:
                        points.append(left_path.right.data)
                left_path = left_path.left
            else:
                left_path = left_path.right

        # check if the found leaf is within range
        if (d0_low <= left_path.data[dimension] <= d0_high
                and d1_low <= left_path.data[dimension + 1] <= d1_high):
            points.append(left_path.data)

        # call the 1D query method for the right path
        while type(right_path) is not Leaf:
            if d0_high <= right_path.data:
                right_path = right_path.left
            else:
                if type(right_path.left) is Node:
                    points += self.query_1d(right_path.left.linked_tree, d1_low, d1_high, dimension + 1)
                elif type(right_path.left) is Leaf:
                    if d1_low <= right_path.left.data[-1] <= d1_high:
                        points.append(right_path.left.data)
                right_path = right_path.right

        # check if the found leaf is within range
        if (d0_low <= right_path.data[dimension] <= d0_high
                and d1_low <= right_path.data[dimension + 1] <= d1_high):
            points.append(right_path.data)

        return points

    def query_3d(self, root, x_low, x_high, y_low, y_high, z_low, z_high):
        points = []

        split_node = self.find_split_node(root, x_low, x_high)

        if type(split_node) is Leaf:
            if (x_low <= split_node.data[1] <= x_high
                    and y_low <= split_node.data[2] <= y_high
                    and z_low <= split_node.data[3] <= z_high):
                return split_node.data

        left_path = split_node.left
        right_path = split_node.right

        # call the 2D query method for the left path
        while type(left_path) is not Leaf:
            if x_low <= left_path.data:
                if type(left_path.right) is Node:
                    points += self.query_2d(left_path.right.linked_tree, y_low, y_high, z_low, z_high, 2)
                elif type(left_path.right) is Leaf:
                    if (y_low <= left_path.right.data[2] <= y_high
                            and z_low <= left_path.right.data[3] <= z_high):
                        points.append(left_path.right.data)
                left_path = left_path.left
            else:
                left_path = left_path.right

        # check if the found leaf is within range
        if (x_low <= left_path.data[1] <= x_high
                and y_low <= left_path.data[2] <= y_high
                and z_low <= left_path.data[3] <= z_high):
            points.append(left_path.data)

        # call the 2D query method for the right path
        while type(right_path) is not Leaf:
            if x_high <= right_path.data:
                right_path = right_path.left
            else:
                if type(right_path) is not Leaf and type(right_path.left) is Node:
                    points += self.query_2d(right_path.left.linked_tree, y_low, y_high, z_low, z_high, 2)
                elif type(right_path) is not Leaf and type(right_path.left) is Leaf:
                    if (y_low <= right_path.left.data[2] <= y_high
                            and z_low <= right_path.left.data[3] <= z_low):
                        points.append(right_path.left.data)
                right_path = right_path.right

        # check if the found leaf is within range
        if (x_low <= right_path.data[1] <= x_high
                and y_low <= right_path.data[2] <= y_high
                and z_low <= right_path.data[3] <= z_high):
            points.append(right_path.data)

        return points
