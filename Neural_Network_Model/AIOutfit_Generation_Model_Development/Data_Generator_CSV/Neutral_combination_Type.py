import random
import csv

# Define colores neutros
neutral_colors = [
    (255, 255, 255),  # Blanco
    (0, 0, 0),        # Negro
    (128, 128, 128),  # Gris
    (192, 192, 192),  # Gris claro
    (169, 169, 169),  # Gris oscuro
    (245, 245, 220),  # Beige
    (210, 180, 140),  # Marrón claro
    (139, 69, 19),    # Marrón
    (105, 105, 105),  # Gris pizarra oscuro
    (47, 79, 79)      # Verde oscuro (casi neutro)
]

def generate_neutral_colors():
    return random.sample(neutral_colors, 3)

def main():
    data = []

    for _ in range(100):
        colors = generate_neutral_colors()
        combinable = random.choice([0, 1])
        data.append(["NEUTRAL", colors[0], colors[1], colors[2], combinable])

    with open("neutral_dataset.csv", "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ÍNDICE", "COLOR1", "COLOR2", "COLOR3", "COMBINABLE"])
        for row in data:
            writer.writerow([row[0], f"({row[1][0]},{row[1][1]},{row[1][2]})",
                             f"({row[2][0]},{row[2][1]},{row[2][2]})",
                             f"({row[3][0]},{row[3][1]},{row[3][2]})", row[4]])

    print("Datos guardados en 'neutral_dataset.csv'.")

if __name__ == "__main__":
    main()
