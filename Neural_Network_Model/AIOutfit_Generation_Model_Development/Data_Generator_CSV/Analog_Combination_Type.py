import random
import csv


def generate_analogous_color_combinations(num_combinations):
    combinations = []
    for _ in range(num_combinations):
        color1 = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # Generate two analogous colors based on color1
        color2 = (color1[0], random.randint(0, 255), random.randint(0, 255))
        color3 = (color1[0], random.randint(0, 255), random.randint(0, 255))

        # Check if colors are within a certain range to be considered analogous
        if is_analogous(color1, color2, color3):
            combinations.append(("ANALOGO", color1, color2, color3, 1))  # 1 for combinable
        else:
            combinations.append(("ANALOGO", color1, color2, color3, 0))  # 0 for not combinable

    return combinations


def is_analogous(color1, color2, color3):
    # Define a threshold to determine if colors are analogous (adjust as needed)
    threshold = 30
    # Check the difference between each pair of colors
    diff12 = color_difference(color1, color2)
    diff23 = color_difference(color2, color3)
    diff31 = color_difference(color3, color1)
    # Colors are considered analogous if their differences are within the threshold
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


# Generate 200 color combinations and check if they are analogous
num_combinations = 200
analogous_combinations = generate_analogous_color_combinations(num_combinations)

# Save the generated combinations to a CSV file
save_to_csv("analogous_dataset.csv", analogous_combinations)
