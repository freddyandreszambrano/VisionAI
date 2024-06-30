import random
import csv


def generate_monochromatic_color(base_color):
    variations = []
    for _ in range(3):
        variation = tuple(min(255, max(0, base_color[i] + random.randint(-40, 40))) for i in range(3))
        variations.append(variation)
    return variations


def main():
    data = []

    for _ in range(100):
        base_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        colors = generate_monochromatic_color(base_color)
        combinable = random.choice([0, 1])
        data.append(["MONOCROMATICA", colors[0], colors[1], colors[2], combinable])

    with open("monochromatic_dataset.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ÍNDICE", "COLOR1", "COLOR2", "COLOR3", "COMBINABLE"])
        for row in data:
            writer.writerow([row[0], f"({row[1][0]},{row[1][1]},{row[1][2]})",
                             f"({row[2][0]},{row[2][1]},{row[2][2]})",
                             f"({row[3][0]},{row[3][1]},{row[3][2]})", row[4]])

    print("Datos guardados en 'monochromatic_dataset.csv'.")


if __name__ == "__main__":
    main()
