import helpers as h
from helpers import sub, visualize_points
from itertools import combinations
from typing import Optional
import math

input = h.readdaylines(9, 2025, example=True)

def area(p1: tuple[int, int], p2: tuple[int, int]):
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)

def parse(input: list[str]):
    return [tuple(map(int, line.split(','))) for line in input]

def part1():
    parsed = parse(input)

    max_area = 0
    for p1, p2 in combinations(parsed, 2):
        a = area(p1, p2)
        if a > max_area:
            max_area = a

    return max_area

def other_corners(p1: tuple[int, int], p2: tuple[int, int]):
    return (p1[0], p2[1]), (p2[0], p1[1])

def vertices_ordered_along_boundary(vertices: list[tuple[int, int]]) -> bool:
    """
    Checks if vertices are ordered along the polygon boundary.
    Returns True if consecutive vertices form edges with consistent orientation
    (all turning in the same direction), False otherwise.
    """
    if len(vertices) < 3:
        return True  # Degenerate cases are considered ordered

    edge_sign = None
    for i in range(len(vertices)):
        e1 = sub(vertices[(i+1) % len(vertices)], vertices[i])
        e2 = sub(vertices[(i+2) % len(vertices)], vertices[(i+1) % len(vertices)])
        cross = cross_product(e1, e2)

        # Skip zero cross products (collinear edges)
        if cross != 0:
            if edge_sign is None:
                edge_sign = cross > 0
            elif (cross > 0) != edge_sign:
                return False

    return True

def point_inside_convex_polygon(point: tuple[int, int], vertices: list[tuple[int, int]]):
    """
    Checks if point is inside a convex polygon by verifying all cross products
    have the same sign (point is on the same side of all edges).
    Returns False if point is on the boundary (all cross products are zero).
    """
    sign = None
    for i in range(len(vertices)):
        v1 = vertices[i]
        v2 = vertices[(i+1) % len(vertices)]
        cross = cross_product(sub(v2, v1), sub(point, v1))

        # Skip zero cross products (point on edge) when determining initial sign
        if cross == 0:
            continue

        if sign is None:
            sign = cross > 0
        elif (cross > 0) != sign:
            return False

    # If sign is still None, all cross products were zero (point on boundary)
    return sign is not None


def cross_product(p1: tuple[int, int], p2: tuple[int, int]):
    return p1[0] * p2[1] - p1[1] * p2[0]

def part2():
    parsed = parse(input)

    if not vertices_ordered_along_boundary(parsed):
        raise ValueError("Vertices are not ordered along the polygon boundary")

    max_area = 0
    for i, p in enumerate(parsed):
        p1 = p
        p2 = parsed[(i + 2) % len(parsed)]

        corners = other_corners(p1, p2)
        in_polygon = all(point_inside_convex_polygon(corner, parsed) for corner in corners)
        if in_polygon:
            a = area(p1, p2)
            if a > max_area:
                max_area = a

    return max_area