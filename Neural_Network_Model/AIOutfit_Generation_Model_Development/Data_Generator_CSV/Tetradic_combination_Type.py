import random
import csv


def generate_tetradic_color_combinations(num_combinations):
    combinations = []
    for _ in range(num_combinations):
        color1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        color2 = generate_complementary_color(color1)
        color3 = generate_offset_color(color1)

        if is_tetradic(color1, color2, color3):
            combinations.append(("TETRADICA", color1, color2, color3, 1))  # 1 for combinable
        else:
            combinations.append(("TETRADICA", color1, color2, color3, 0))  # 0 for not combinable

    return combinations


def generate_complementary_color(color):
    # Generate the complementary color
    comp_color = (255 - color[0], 255 - color[1], 255 - color[2])
    return comp_color


def generate_offset_color(color):
    # Generate a color that is offset by 120 degrees on the color wheel (to form a triangle)
    angle = 120
    hue = (color[0] + angle) % 256
    return (hue, random.randint(0, 255), random.randint(0, 255))


def is_tetradic(color1, color2, color3):
    # Define a threshold to determine if colors are tetradic (adjust as needed)
    threshold = 60
    # Check the difference between each pair of colors
    diff12 = color_difference(color1, color2)
    diff23 = color_difference(color2, color3)
    diff31 = color_difference(color3, color1)
    # Colors are considered tetradic if their differences are within the threshold
    return diff12 <= threshold and diff23 <= threshold and diff31 <= threshold


def color_difference(color1, color2):
    # Calculate Euclidean distance between two RGB colors
    return sum((c1 - c2) ** 2 for c1, c2 in zip(color1, color2)) ** 0.5


def save_to_csv(filename, data):
    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ÍNDICE", "COLOR1", "COLOR2", "COLOR3", "COMBINABLE"])
        for row in data:
            writer.writerow([row[0], f"({row[1][0]},{row[1][1]},{row[1][2]})",
                             f"({row[2][0]},{row[2][1]},{row[2][2]})",
                             f"({row[3][0]},{row[3][1]},{row[3][2]})", row[4]])
    print(f"Datos guardados en '{filename}'.")


# Generate 200 color combinations and check if they are tetradic
num_combinations = 200
tetradic_combinations = generate_tetradic_color_combinations(num_combinations)

# Save the generated combinations to a CSV file
save_to_csv("tetradic_dataset.csv", tetradic_combinations)
