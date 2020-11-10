import argparse
import os.path
import sys
import range_tree
import skyline_operator
import r_tree
import time


def argument_validity():
    parser = argparse.ArgumentParser()

    parser.add_argument("x_from", type=float,
                        help="lower bound of data range for dimension x")
    parser.add_argument("x_to", type=float,
                        help="upper bound of data range for dimension x")
    parser.add_argument("y_from", type=float,
                        help="lower bound of data range for dimension y")
    parser.add_argument("y_to", type=float,
                        help="upper bound of data range for dimension y")
    parser.add_argument("--d3", nargs=2, metavar=("z_from", "z_to"), type=float, default=None,
                        help="flag to indicate usage of 3dimensional data, "
                             "requires lower and upper bounds of data range for dimension z")
    parser.add_argument("-i", "--input", type=str, default="input.txt",
                        help="data file to be used, defauls is input.txt", dest="data")
    parser.add_argument("-t", "--tree", choices=['r', "range"],
                        default="range", dest="structure",
                        help="data structure to be used for input storage")

    args = parser.parse_args()

    return args.x_from, args.x_to, args.y_from, args.y_to, args.d3, args.data, args.structure


def input_parse(input_file, dimensions):
    if not os.path.isfile(input_file) or os.path.splitext(input_file)[1] != ".txt":
        print("Please enter a valid text file as input.")
        sys.exit()

    output = []
    with open(input_file, 'r', encoding="UTF-8") as input_file:
        # assume input in the following format: POINT_NAME DIM_X DIM_Y [DIM_Z]
        for line in input_file:
            items = line.split()
            if dimensions == 3:
                try:
                    output.append([items[0], float(items[1]), float(items[2]), float(items[3])])
                except IndexError:
                    print("Please enter a valid text file as input.")
                    sys.exit()
            else:
                try:
                    output.append([items[0], float(items[1]), float(items[2])])
                except IndexError:
                    print("Please enter a valid text file as input.")
                    sys.exit()

    output = sorted(output, key=lambda x: x[1])

    return output


if __name__ == "__main__":
    x_from, x_to, y_from, y_to, z, file_to_read, data_structure = argument_validity()
    if z is None:
        dimensions = 2
    else:
        dimensions = 3
    data = input_parse(file_to_read, dimensions)

    start_time = time.time()
    if data_structure == "range" and dimensions == 2:
        tree = range_tree.RangeTree()
        root, _ = tree.create_tree(data, 1)
        points = tree.query_2d(root, x_from, x_to, y_from, y_to, 1)
    elif data_structure == "range" and dimensions == 3:
        tree = range_tree.RangeTree()
        root, _ = tree.create_tree(data, 1)
        points = tree.query_3d(root, x_from, x_to, y_from, y_to, z[0], z[1])
    else:
        tree = r_tree.RTree()
        root = tree.create_rtree(data, dimensions)
        if dimensions == 2:
            points = tree.query(root, [x_from, x_to, y_from, y_to], dimensions)
        else:
            points = tree.query(root, [x_from, x_to, y_from, y_to, z[0], z[1]], dimensions)

    skyline = skyline_operator.nearest_neighbour(sorted(points, key=lambda x: x[1]))
    execution_time = time.time() - start_time

    print(execution_time)
    print("Skyline:", skyline)
