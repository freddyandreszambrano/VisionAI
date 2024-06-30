import random
import csv

# Definir colores complementarios en el círculo cromático
complementary_pairs = [
    ((255, 0, 0), (0, 255, 255)),  # Rojo y Cian
    ((0, 255, 0), (255, 0, 255)),  # Verde y Magenta
    ((0, 0, 255), (255, 255, 0))  # Azul y Amarillo
]


def generate_complementary_colors():
    pair1 = random.choice(complementary_pairs)
    pair2 = random.choice(complementary_pairs)

    color1 = pair1[0]
    color2 = pair1[1]
    color3 = pair2[0]

    # Generar tonos aleatorios para cada color
    color1_variation = tuple(min(255, max(0, color1[i] + random.randint(-40, 40))) for i in range(3))
    color2_variation = tuple(min(255, max(0, color2[i] + random.randint(-40, 40))) for i in range(3))
    color3_variation = tuple(min(255, max(0, color3[i] + random.randint(-40, 40))) for i in range(3))

    return color1_variation, color2_variation, color3_variation


def main():
    data = []

    for _ in range(50):
        color1, color2, color3 = generate_complementary_colors()
        combinable = random.choice([0, 1])
        data.append(["COMPLEMENTARIO", color1, color2, color3, combinable])

    with open("color_dataset.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["TIPO", "COLOR1", "COLOR2", "COLOR3", "COMBINABLE"])
        for row in data:
            writer.writerow([
                row[0],
                f"({row[1][0]},{row[1][1]},{row[1][2]})",
                f"({row[2][0]},{row[2][1]},{row[2][2]})",
                f"({row[3][0]},{row[3][1]},{row[3][2]})",
                row[4]
            ])

    print("Datos guardados en 'color_dataset.csv'.")


if __name__ == "__main__":
    main()
