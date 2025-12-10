import pytest
import sys
from pathlib import Path

# Add 2025 directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent / "2025"))

from day9 import point_inside_convex_polygon


class TestPointInsideConvexPolygon:
    """Unit tests for point_inside_convex_polygon function."""

    def test_point_inside_square(self):
        """Test point inside a square."""
        # Square with vertices: (0,0), (2,0), (2,2), (0,2)
        vertices = [(0, 0), (2, 0), (2, 2), (0, 2)]
        point = (1, 1)
        assert point_inside_convex_polygon(point, vertices) is True

    def test_point_outside_square(self):
        """Test point outside a square."""
        vertices = [(0, 0), (2, 0), (2, 2), (0, 2)]
        point = (3, 1)
        assert point_inside_convex_polygon(point, vertices) is False

    def test_point_on_edge(self):
        """Test point on an edge (boundary) - should return True."""
        vertices = [(0, 0), (2, 0), (2, 2), (0, 2)]
        point = (1, 0)  # On bottom edge
        assert point_inside_convex_polygon(point, vertices) is True

    def test_point_on_vertex(self):
        """Test point on a vertex (boundary) - should return True."""
        vertices = [(0, 0), (2, 0), (2, 2), (0, 2)]
        point = (0, 0)  # On vertex
        assert point_inside_convex_polygon(point, vertices) is True

    def test_point_inside_triangle(self):
        """Test point inside a triangle."""
        vertices = [(0, 0), (3, 0), (1, 3)]
        point = (1, 1)
        assert point_inside_convex_polygon(point, vertices) is True

    def test_point_outside_triangle(self):
        """Test point outside a triangle."""
        vertices = [(0, 0), (3, 0), (1, 3)]
        point = (4, 1)
        assert point_inside_convex_polygon(point, vertices) is False

    def test_point_on_triangle_edge(self):
        """Test point on triangle edge - should return True."""
        vertices = [(0, 0), (3, 0), (1, 3)]
        point = (1.5, 0)  # On base edge
        assert point_inside_convex_polygon(point, vertices) is True

    def test_counterclockwise_polygon(self):
        """Test with counterclockwise oriented polygon."""
        # Counterclockwise square
        vertices = [(0, 0), (0, 2), (2, 2), (2, 0)]
        point = (1, 1)
        assert point_inside_convex_polygon(point, vertices) is True

    def test_clockwise_polygon(self):
        """Test with clockwise oriented polygon."""
        # Clockwise square
        vertices = [(0, 0), (2, 0), (2, 2), (0, 2)]
        point = (1, 1)
        assert point_inside_convex_polygon(point, vertices) is True

    def test_point_near_edge_inside(self):
        """Test point very close to edge but inside."""
        vertices = [(0, 0), (2, 0), (2, 2), (0, 2)]
        point = (1, 0.5)  # Close to bottom edge but inside
        assert point_inside_convex_polygon(point, vertices) is True

    def test_point_near_edge_outside(self):
        """Test point very close to edge but outside."""
        vertices = [(0, 0), (2, 0), (2, 2), (0, 2)]
        point = (1, -0.5)  # Close to bottom edge but outside
        assert point_inside_convex_polygon(point, vertices) is False

    def test_pentagon_inside(self):
        """Test point inside a pentagon."""
        vertices = [(0, 0), (2, 0), (3, 2), (1, 3), (-1, 2)]
        point = (1, 1)
        assert point_inside_convex_polygon(point, vertices) is True

    def test_pentagon_outside(self):
        """Test point outside a pentagon."""
        vertices = [(0, 0), (2, 0), (3, 2), (1, 3), (-1, 2)]
        point = (4, 4)
        assert point_inside_convex_polygon(point, vertices) is False

    def test_rectangle_inside(self):
        """Test point inside a rectangle."""
        vertices = [(1, 1), (5, 1), (5, 4), (1, 4)]
        point = (3, 2)
        assert point_inside_convex_polygon(point, vertices) is True

    def test_rectangle_outside(self):
        """Test point outside a rectangle."""
        vertices = [(1, 1), (5, 1), (5, 4), (1, 4)]
        point = (0, 0)
        assert point_inside_convex_polygon(point, vertices) is False

    def test_point_on_corner_edge(self):
        """Test point on corner where two edges meet - should return True."""
        vertices = [(0, 0), (2, 0), (2, 2), (0, 2)]
        point = (2, 0)  # On corner
        assert point_inside_convex_polygon(point, vertices) is True

    def test_negative_coordinates_inside(self):
        """Test point inside polygon with negative coordinates."""
        vertices = [(-2, -2), (0, -2), (0, 0), (-2, 0)]
        point = (-1, -1)
        assert point_inside_convex_polygon(point, vertices) is True

    def test_negative_coordinates_outside(self):
        """Test point outside polygon with negative coordinates."""
        vertices = [(-2, -2), (0, -2), (0, 0), (-2, 0)]
        point = (1, 1)
        assert point_inside_convex_polygon(point, vertices) is False

    def test_large_polygon(self):
        """Test with larger coordinate values."""
        vertices = [(0, 0), (100, 0), (100, 100), (0, 100)]
        point = (50, 50)
        assert point_inside_convex_polygon(point, vertices) is True

    def test_point_on_middle_of_edge(self):
        """Test point exactly in the middle of an edge - should return True."""
        vertices = [(0, 0), (4, 0), (4, 4), (0, 4)]
        point = (2, 0)  # Middle of bottom edge
        assert point_inside_convex_polygon(point, vertices) is True

    def test_irregular_convex_polygon_inside(self):
        """Test point inside an irregular convex polygon."""
        vertices = [(0, 0), (4, 0), (5, 3), (3, 5), (0, 4)]
        point = (2, 2)
        assert point_inside_convex_polygon(point, vertices) is True

    def test_irregular_convex_polygon_outside(self):
        """Test point outside an irregular convex polygon."""
        vertices = [(0, 0), (4, 0), (5, 3), (3, 5), (0, 4)]
        point = (6, 6)
        assert point_inside_convex_polygon(point, vertices) is False

