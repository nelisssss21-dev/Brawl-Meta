# -*- coding: utf-8 -*-
"""
Название проекта: «Brawl Meta: Чат-бот для пика героев под ранговый режим»

[КРИТЕРИЙ 1] Описание проекта:
Это чат-бот, который помогает игрокам Brawl Stars правильно выбирать бойцов 
для конкретных карт в Ранговом режиме. Бот анализирует текущую карту, режим 
и подсказывает, какие герои будут наиболее эффективны, а каких лучше не брать.

[КРИТЕРИЙ 2] Функционал (Интерфейс взаимодействия с пользователем):
1. Выбор карты и режима.
2. Рекомендация «Топ-3 пика» с пояснениями.
3. Анти-пик (Кого НЕ брать).
4. Учет контр-пиков.
5. Сохранение истории выборов.
6. Актуальность (Мета-обновления).

[КРИТЕРИЙ 3] Значимость проекта:
Проект решает главную проблему рангового режима – неправильный пик.
1. Экономия времени: бот выдает ответ с опорой на «актуальную мету» за пару секунд.
2. Доступность для всех: работает без мощного железа.
3. Повышение ранга: помогает выбирать «метовых» героев, увеличивая шанс на победу.
"""

# [КРИТЕРИЙ 11] Импорт сторонних библиотек (colorama, PIL) и стандартных (json, os, datetime)
import json
import os
import datetime
from colorama import Fore, Style  # СТОРОННЯЯ: цветной вывод в консоли
from PIL import Image             # СТОРОННЯЯ: работа с изображениями

# ---------- НАСТРОЙКИ И ПУТИ ----------
IMG_FOLDER = r"C:\Users\student\Desktop\brawl_images" 

map_images = {
    "Гем-граб": "map_gem.jpg", "Ограбление": "map_robbery.jpg",
    "Нокаут": "map_knockout.jpg", "Броубол": "map_brawlball.jpg"
}
hero_images = {
    "Мортис": "hero_mortis.jpg", "Леон": "hero_leon.jpg", "Спайк": "hero_spike.jpg",
    "Динамайк": "hero_dynamike.jpg", "Эль Примо": "hero_elprimo.jpg",
    "Кольт": "hero_colt.jpg", "Пайпер": "hero_piper.jpg"
}

# [КРИТЕРИЙ 4 и 8] Переменные, словари и списки
maps_db = {
    "Гем-граб": {
        "режим": "Захват кристаллов",
        "топ": [("Джин", "контролирует центр"), ("Пайпер", "урон издалека"), ("Динамайк", "контроль зон")],
        "анти": ["Эль Примо", "Булл"]
    },
    "Ограбление": {
        "режим": "Ограбление",
        "топ": [("Кольт", "урон по сейфу"), ("Брок", "дальний бой"), ("Рико", "рикошеты")],
        "анти": ["Динамайк", "Тик"]
    },
    "Нокаут": {
        "режим": "Нокаут",
        "топ": [("Спайк", "урон по площади"), ("Леон", "невидимость"), ("Сэнди", "песчаная буря")],
        "анти": ["Джесси", "Нита"]
    },
    "Броубол": {
        "режим": "Броубол",
        "топ": [("Эль Примо", "танк"), ("Булл", "рывок"), ("Дэррил", "быстрый прорыв")],
        "анти": ["Пайпер", "Бо"]
    }
}

counter_picks = {
    "Мортис": "Пайпер или Поко (держи дистанцию)",
    "Леон": "Поко или Спайк (урон по площади)",
    "Спайк": "Ворон или Мортис (быстрое сближение)",
    "Динамайк": "Кольт или Брок (перестреляй издалека)",
    "Эль Примо": "Кольт или Пайпер (не подпускай близко)",
    "Кольт": "Мортис или Булл (сблизись с ним)",
    "Пайпер": "Мортис или Леон (подкрадывайся)"
}

HISTORY_FILE = "brawl_history.json"

def show_image(filename):
    """Показывает картинку. Работает в Jupyter, в .exe просто выводит путь."""
    path = os.path.join(IMG_FOLDER, filename)
    if not os.path.exists(path):
        print(Fore.LIGHTBLACK_EX + f"  (нет картинки: {filename})" + Style.RESET_ALL)
        return
    try:
        from IPython.display import display
        display(Image.open(path))
    except Exception:
        print(f"  🖼  Картинка: {path}")

def load_history():
    """[КРИТЕРИЙ 10] Ввод данных из файла (JSON)."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_to_history(hero):
    """[КРИТЕРИЙ 10] Вывод данных в файл (JSON)."""
    history = load_history()
    record = {
        "hero": hero,
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "source": "recommendation"
    }
    history.append(record)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def normalize_input(text):
    """[КРИТЕРИЙ 7] Функции обработки строк: strip(), lower(), split(), join()."""
    cleaned = text.strip().lower()
    cleaned = " ".join(cleaned.split())
    return cleaned

def format_hero_name(name):
    """[КРИТЕРИЙ 7] Функции обработки строк: strip(), title()."""
    return name.strip().title()

def func1_pick_for_map():
    """Функция 1: Выбор карты, Топ-3 пик + Анти-пик."""
    print(Fore.CYAN + "\n🗺  ДОСТУПНЫЕ КАРТЫ:" + Style.RESET_ALL)
    map_list = list(maps_db.keys())
    for i, name in enumerate(map_list, 1):  # [КРИТЕРИЙ 6] Цикл for
        print(f"  {i}. {name} ({maps_db[name]['режим']})")
    choice = input("\nВведи номер карты: ")
    cleaned_choice = normalize_input(choice)
    if not cleaned_choice.isdigit():  # [КРИТЕРИЙ 5] Условный оператор if
        print(Fore.RED + "❌ Нужно ввести число." + Style.RESET_ALL)
        return
    choice_num = int(cleaned_choice)
    if choice_num < 1 or choice_num > len(map_list):
        print(Fore.RED + "❌ Неверный номер." + Style.RESET_ALL)
        return
    map_name = map_list[choice_num - 1]
    print(Fore.GREEN + f"\n✅ Выбрана карта: {map_name}" + Style.RESET_ALL)
    show_image(map_images.get(map_name, "map_default.jpg"))
    print(Fore.YELLOW + "\n🏆 ТОП-3 ГЕРОЯ (кого брать):" + Style.RESET_ALL)
    for i, (hero, reason) in enumerate(maps_db[map_name]["топ"], 1):
        formatted_hero = format_hero_name(hero)
        print(f"  {i}. {formatted_hero} — {reason}")
        save_to_history(formatted_hero)
    print(Fore.RED + f"\n🚫 АНТИ-ПИК (кого НЕ брать на '{map_name}'):" + Style.RESET_ALL)
    for hero in maps_db[map_name]["анти"]:
        print(f"  • {hero}")

def func2_counter_pick():
    """Функция 2: Подбор контр-героя против противника."""
    print(Fore.MAGENTA + "\n⚔  ГЕРОИ ПРОТИВНИКА:" + Style.RESET_ALL)
    heroes = list(counter_picks.keys())
    for i, name in enumerate(heroes, 1):
        print(f"  {i}. {name}")
    choice = input("\nВведи номер героя противника: ")
    cleaned_choice = normalize_input(choice)
    if not cleaned_choice.isdigit():
        print(Fore.RED + "❌ Нужно ввести число." + Style.RESET_ALL)
        return
    choice_num = int(cleaned_choice)
    if choice_num < 1 or choice_num > len(heroes):
        print(Fore.RED + "❌ Неверный номер." + Style.RESET_ALL)
        return
    enemy = heroes[choice_num - 1]
    counter = counter_picks[enemy]
    show_image(hero_images.get(enemy, "hero_default.jpg"))
    print(Fore.GREEN + f"\n🎯 ПРОТИВ '{enemy}' БЕРИ: {counter}" + Style.RESET_ALL)
    save_to_history(enemy)

def func3_show_history():
    """Функция 3: История выборов + МНОЖЕСТВА [КРИТЕРИЙ 8]."""
    history = load_history()
    if not history:
        print(Fore.YELLOW + "\n📭 История пуста — ты ещё никого не выбирал." + Style.RESET_ALL)
        return
    unique_heroes = set()  # [КРИТЕРИЙ 8] Использование множества set()
    for record in history:
        unique_heroes.add(record["hero"])
    print(Fore.CYAN + "\n📊 ТВОЯ ИСТОРИЯ ВЫБОРОВ:" + Style.RESET_ALL)
    print(f"  Всего выборов: {len(history)}")
    print(f"  Уникальных героев: {len(unique_heroes)}")
    print("-" * 40)
    recent = history[-10:]
    for i, record in enumerate(recent, 1):
        print(f"  {i}. {record['hero']} (выбран: {record['timestamp']})")
    if len(history) > 10:
        print("  ... (показаны только последние 10)")
    heroes_list = ", ".join(sorted(unique_heroes))  # [КРИТЕРИЙ 7] Обработка строк: join()
    print(Fore.GREEN + f"\n🎮 Твой пул героев: {heroes_list}" + Style.RESET_ALL)

def func4_exit():
    """Функция 4: Выход из программы."""
    print(Fore.YELLOW + "\n👋 Удачи в ранговом режиме! Бот завершает работу." + Style.RESET_ALL)
    return True

def main():
    """Главная функция — [КРИТЕРИЙ 6] цикл while."""
    print(Fore.GREEN + "=" * 50)
    print("   BRAWL META — чат-бот для пика героев")
    print("   Учебный проект. Версия 1.0")
    print("=" * 50 + Style.RESET_ALL)
    show_image("logo.jpg")
    while True:  # [КРИТЕРИЙ 6] Цикл while
        print(Fore.CYAN + "\nЧТО УМЕЕТ ЭТОТ БОТ?" + Style.RESET_ALL)
        print("1. Подобрать пик под карту (Топ-3 + Анти-пик)")
        print("2. Контр-пик против героя")
        print("3. Посмотреть историю выборов")
        print("4. Выйти")
        choice = input("\nТвой выбор (1-4): ")
        cleaned_choice = normalize_input(choice)
        if cleaned_choice == "1":  # [КРИТЕРИЙ 5] Условный оператор if/elif/else
            func1_pick_for_map()
        elif cleaned_choice == "2":
            func2_counter_pick()
        elif cleaned_choice == "3":
            func3_show_history()
        elif cleaned_choice == "4":
            if func4_exit():
                break
        else:
            print(Fore.RED + "❌ Введи число от 1 до 4." + Style.RESET_ALL)

if __name__ == "__main__":
    main()