from pathlib import Path


BASE_DIR = Path(__file__).parent


def get_cats_info(path):
    cats = []

    try:
        with open(path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                cat_id, name, age = line.split(",")
                cats.append({
                    "id": cat_id,
                    "name": name,
                    "age": age,
                })

        return cats

    except FileNotFoundError:
        print(f"File not found: {path}")
        return []
    except ValueError:
        print("Invalid file format.")
        return []
    except Exception as error:
        print(f"An error occurred: {error}")
        return []


if __name__ == "__main__":
    cats_path = BASE_DIR / "cats_file.txt"
    print(get_cats_info(cats_path))
