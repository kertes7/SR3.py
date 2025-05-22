import json

class Film:
    def __init__(self, title, genre, year, rating):
        self.title = title
        self.genre = genre
        self.year = year
        self.rating = rating

    def to_dict(self):
        return {
            'title': self.title,
            'genre': self.genre,
            'year': self.year,
            'rating': self.rating
        }

    def __str__(self):
        return f"{self.title} ({self.year}) — {self.genre}, рейтинг: {self.rating}"

class Catalog:
    def __init__(self):
        self.films = []

    def add_film(self, film):
        self.films.append(film)

    def save_to_file(self, filename="films.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([film.to_dict() for film in self.films], f, ensure_ascii=False, indent=2)

    def load_from_file(self, filename="films.json"):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.films = [Film(**item) for item in data]
        except FileNotFoundError:
            self.films = []

    def filter_by_genre(self, genre):
        return [film for film in self.films if film.genre.lower() == genre.lower()]

    def sort_by_rating(self, descending=True):
        return sorted(self.films, key=lambda x: x.rating, reverse=descending)

    def save_selected_to_file(self, films, filename="selected_films.json"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump([film.to_dict() for film in films], f, ensure_ascii=False, indent=2)

    def show_all(self):
        if not self.films:
            print("Каталог порожній.")
            return
        for i, film in enumerate(self.films, 1):
            print(f"{i}. {film}")


def add_film(catalog):
    title = input("Назва фільму: ")
    genre = input("Жанр: ")
    year = int(input("Рік: "))
    rating = float(input("Рейтинг: "))
    catalog.add_film(Film(title, genre, year, rating))
    catalog.save_to_file()
    print("Фільм додано.")

def show_all_films(catalog):
    catalog.show_all()

def filter_by_genre(catalog):
    genre = input("Введіть жанр: ")
    filtered = catalog.filter_by_genre(genre)
    if filtered:
        for film in filtered:
            print(film)
    else:
        print("Фільмів такого жанру не знайдено.")

def sort_by_rating(catalog):
    sorted_films = catalog.sort_by_rating()
    for film in sorted_films:
        print(film)

def save_selected(catalog):
    catalog.show_all()
    indexes = input("Введіть номери фільмів для збереження через кому: ")
    try:
        selected_indexes = [int(i.strip()) - 1 for i in indexes.split(",")]
        selected_films = [catalog.films[i] for i in selected_indexes if 0 <= i < len(catalog.films)]
        catalog.save_selected_to_file(selected_films)
        print("Фільми збережено у selected_films.json.")
    except Exception as e:
        print(f"Помилка: {e}")

def menu():
    catalog = Catalog()
    catalog.load_from_file()

    while True:
        print("\n=== Каталог українського кіно ===")
        print("1. Додати фільм")
        print("2. Показати всі фільми")
        print("3. Фільтрувати за жанром")
        print("4. Сортувати за рейтингом")
        print("5. Зберегти обрані фільми у файл")
        print("6. Вийти")

        choice = input("Оберіть дію: ")

        if choice == "1":
            add_film(catalog)
        elif choice == "2":
            show_all_films(catalog)
        elif choice == "3":
            filter_by_genre(catalog)
        elif choice == "4":
            sort_by_rating(catalog)
        elif choice == "5":
            save_selected(catalog)
        elif choice == "6":
            print("Завершення програми.")
            break
        else:
            print("Невірна команда. Спробуйте ще раз.")


if __name__ == "__main__":
    menu()
