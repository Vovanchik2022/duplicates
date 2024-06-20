import os
from PIL import Image
import imagehash
import matplotlib.pyplot as plt


def load_images_from_folder(folder):
    supported_formats = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
    images = []
    for filename in os.listdir(folder):
        if filename.lower().endswith(supported_formats):
            try:
                img = Image.open(os.path.join(folder, filename))
                if img is not None:
                    images.append((filename, img))
            except (IOError, OSError) as e:
                print(f"Error loading {filename}: {e}")
    return images


def find_duplicates(images):
    hashes = {}
    duplicates = []

    for filename, img in images:
        img_hash = imagehash.average_hash(img)
        if img_hash in hashes:
            duplicates.append((filename, hashes[img_hash]))
        else:
            hashes[img_hash] = filename

    return duplicates


def print_duplicates(duplicates):
    if not duplicates:
        print("Дубликаты не найдены.")
    else:
        for dup1, dup2 in duplicates:
            print(f"Дубликаты: {dup1} и {dup2}")


def show_duplicates(duplicates, folder1, folder2):
    for dup1, dup2 in duplicates:
        img1_path = os.path.join(folder1, dup1) if os.path.exists(
            os.path.join(folder1, dup1)) else os.path.join(folder2, dup1)
        img2_path = os.path.join(folder1, dup2) if os.path.exists(
            os.path.join(folder1, dup2)) else os.path.join(folder2, dup2)

        img1 = Image.open(img1_path)
        img2 = Image.open(img2_path)

        fig, axes = plt.subplots(1, 2)
        axes[0].imshow(img1)
        axes[0].set_title(dup1)
        axes[1].imshow(img2)
        axes[1].set_title(dup2)
        plt.show()


def main():
    folder1 = input("Введите директорию первой папки: ")
    folder2 = input(
        "Введите директорию второй папки: (или нажмите Enter для пропуска): ")

    images1 = load_images_from_folder(folder1)
    images2 = load_images_from_folder(folder2) if folder2 else []

    if images2:
        combined_images = images1 + images2
    else:
        combined_images = images1

    duplicates_hash = find_duplicates(combined_images)

    print_duplicates(duplicates_hash)

    if duplicates_hash:
        show_duplicates(duplicates_hash, folder1, folder2)


if __name__ == "__main__":
    main()
