import numpy as np

def catmull_rom(p0, p1, p2, p3, n_points=20):
    t = np.linspace(0, 1, n_points)[:, None]
    p0, p1, p2, p3 = map(np.array, (p0, p1, p2, p3))
    a = 2*p1
    b = -p0 + p2
    c = 2*p0 - 5*p1 + 4*p2 - p3
    d = -p0 + 3*p1 - 3*p2 + p3
    return 0.5 * (a + (b*t) + (c*t**2) + (d*t**3))


def build_catmull_rom_chain(points, samples_per_segment=100):
    curve = []
    for i in range(len(points) - 3):
        seg = catmull_rom(points[i], points[i+1], points[i+2], points[i+3], samples_per_segment)
        curve.extend(seg)
    return np.array(curve)

def get_heading(v1, v2):
    vector = np.array(v1) - np.array(v2)
    dir = vector / np.linalg.norm(vector)

    return dir

def rotate_point(point, angle):
    x, y = point
    cos_theta = np.cos(angle)
    sin_theta = np.sin(angle)
    x_rot = x * cos_theta - y * sin_theta
    y_rot = x * sin_theta + y * cos_theta
    return (x_rot, y_rot)

def rotate_spline(spline, angle):
    new_spline = []
    for i in range(len(spline)):
        new_spline.append(rotate_point(spline[i], angle))
    return np.array(new_spline)
