# For computing the parameters for the fancy loading animation
import math


def polar_to_cartesian(r: float, theta: float):
    x = r * math.cos(math.radians(theta))
    y = r * math.sin(math.radians(theta))
    return x, y


def create_animation(start, end, name="NAME"):
    offset = end[0] - start[0], end[1] - start[1]
    return f"@keyframes {name} {{\n \
    0% {{transform: translate({end[0]}px, {end[1]}px);}}\n \
    20% {{transform: translate({start[0]}px, {start[1]}px);}}\n \
    40%, 100% {{transform: translate({end[0]}px, {end[1]}px);}}\n \
    }}\n"


def main():
    CONTAINER_WIDTH = 150  # Width and height of loading container in pixels
    NUMBER_OF_DOTS = 5
    OUTER_RADIUS = 45
    INNER_RADIUS = 20
    DOT_WIDTH = 20

    center_x = CONTAINER_WIDTH // 2
    dot_center = DOT_WIDTH // 2
    for num, angle_degrees in enumerate(range(0, 360, 360 // NUMBER_OF_DOTS)):
        start_offset = polar_to_cartesian(OUTER_RADIUS, angle_degrees)
        end_offset = polar_to_cartesian(INNER_RADIUS, angle_degrees)

        start_position = start_offset[0] - dot_center, start_offset[1] - dot_center
        end_position = end_offset[0] - dot_center, end_offset[1] - dot_center

        # print(f"({int(start_position[0])}, {int(start_position[1])}), ({int(end_position[0])}, {int(end_position[1])}), ")

        print(create_animation(start_position, end_position, f"dot{num + 1}"))


if __name__ == '__main__':
    main()
