from typing import List, Tuple
Point = Tuple[int, int]

def orientation(p: Point, q: Point, r: Point) -> int:
    return (q[1] - p[1]) * (r[0] - q[0]) - (r[1] - q[1]) * (q[0] - p[0])

def distance_sq(p: Point, q: Point) -> int:
    return (p[0] - q[0])**2 + (p[1] - q[1])**2

def jarvis_march(points: List[Point], handle_collinear: bool = False) -> List[Point]:
    if len(points) < 3:
        return points[:]
    start = min(points, key=lambda p: (p[0], p[1]))
    hull = []
    p = start
    n = len(points)
    while True:
        hull.append(p)
        idx = points.index(p)
        q = points[(idx + 1) % n]
        for r in points:
            if r == p or r == q:
                continue
            orient = orientation(p, q, r)
            if orient > 0:
                q = r
            elif orient == 0 and handle_collinear:
                if distance_sq(p, r) > distance_sq(p, q):
                    q = r
        p = q
        if p == start:
            break
    return hull


if __name__ == '__main__':
    sets = [
        [(0, 3), (0, 0), (0, 1), (3, 0), (3, 3)],
        [(0, 3), (0, 1), (0, 0), (3, 0), (3, 3)],
        [(2, 2), (4, 3), (5, 4), (0, 3), (0, 2), (0, 0), (2, 1), (2, 0), (4, 0)]
    ]

    for pts in sets:
        hull_basic = jarvis_march(pts, handle_collinear=False)
        print(f"{hull_basic}")
        hull_improved = jarvis_march(pts, handle_collinear=True)
        print(f"{hull_improved}\n")