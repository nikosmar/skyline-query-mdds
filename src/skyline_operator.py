import math


def merge_skylines(skyline_1, skyline_2, dimension):
    # check if any tuple can be eliminated
    for point1 in skyline_1:
        for point2 in skyline_2:
            domination_flag = len(point1) - 1
            for dim in range(dimension, len(point1)):
                if point1[dim] <= point2[dim]:
                    domination_flag -= 1
            if domination_flag == 0:
                skyline_2.remove(point2)

    # the recursion ends if all dimensions have been considered
    # or if one of the two parts contains one or no items
    if (len(skyline_1) < 2 or len(skyline_2) < 2
            or len(skyline_1[0]) - 1 == dimension):
        return skyline_1 + skyline_2

    # divide both skylines by using the median of dimension
    median_of_skyline_1 = len(skyline_1) // 2
    median_of_skyline_2 = len(skyline_2) // 2
    skyline_1 = sorted(skyline_1, key=lambda x: x[dimension + 1])
    skyline_2 = sorted(skyline_2, key=lambda x: x[dimension + 1])
    skyline_1_1 = skyline_1[:median_of_skyline_1]
    skyline_1_2 = skyline_1[median_of_skyline_1:]
    skyline_2_1 = skyline_2[:median_of_skyline_2]
    skyline_2_2 = skyline_2[median_of_skyline_2:]

    # skyline_1_i is better than skyline_2_i in dimension 1
    # skyline_i_1 is better than skyline_i_2 in dimension 2
    out1 = merge_skylines(skyline_1_1, skyline_2_1, dimension)
    out2 = merge_skylines(skyline_1_2, skyline_2_2, dimension)
    out3 = merge_skylines(skyline_1_1, out2, dimension + 1)

    return out1 + out3


def divide_and_conquer(data):
    # it is assumed that data are pre-sorted in dimension 1 (x)
    if len(data) == 1:
        return data

    median = len(data) // 2
    part_1 = data[:median]
    part_2 = data[median:]

    # compute the skyline of each part
    skyline_1 = divide_and_conquer(part_1)
    skyline_2 = divide_and_conquer(part_2)

    # compute the overall skyline
    skyline = merge_skylines(skyline_1, skyline_2, 1)

    return skyline


# calculates the distance from point(x,y,z) to O(0,0,0) (in 2D or 3D)
def euclidean_distance(point):
    distance = 0
    for i in point:
        distance += i**2
    return math.sqrt(distance)


def bounded_nearest_neighbour_search(data_set, region):
    nearest_point = None
    distance_to_point = float("inf")

    if len(data_set[0]) == 3:
        for point in data_set:
            if region[2] >= point[1] >= region[0] and region[3] >= point[2] >= region[1]:
                temp_distance = euclidean_distance(point[1:])
                if temp_distance < distance_to_point:
                    nearest_point = point
                    distance_to_point = temp_distance
    else:
        for point in data_set:
            if (region[3] > point[1] > region[0] and region[4] > point[2] > region[1]
                    and region[5] > point[3] > region[2]):
                temp_distance = euclidean_distance(point[1:])
                if temp_distance < distance_to_point:
                    nearest_point = point
                    distance_to_point = temp_distance

    return nearest_point


def nearest_neighbour(data):
    if len(data[0]) == 3:
        to_do = [[0, 0, float("inf"), float("inf")]]
    else:
        to_do = [[0, 0, 0, float("inf"), float("inf"), float("inf")]]

    skyline = []
    while to_do and data:
        region = to_do[0]
        del to_do[0]
        point = bounded_nearest_neighbour_search(data, region)
        if point is not None:
            data.remove(point)
            if data and len(data[0]) == 3:
                # region bounded by point's y dimension
                to_do.append([point[1], region[1], region[2], point[2]])
                # region bounded by point's x dimension
                to_do.append([region[0], point[2], point[1], region[3]])
            else:
                # region bounded by point's x dimension
                to_do.append([region[0], region[1], region[2], point[1], region[4], region[5]])
                # region bounded by point's y dimension
                to_do.append([region[0], region[1], region[2], region[3], point[2], region[5]])
                # region bounded by point's z dimension
                to_do.append([region[0], region[1], region[2], region[3], region[4], point[3]])
            skyline.append(point)

    return skyline
