import random
import sys
import json
import time
import os
from datetime import datetime

# =============================================================
#    🌟 БИЛД СТУДИИ МУХАММАДА МАЖИДОВА // АБСОЛЮТНАЯ ЗАЩИТА 🌟
#    ☭ СССР | 🇩🇪 ГЕРМАНИЯ | 🇯🇵 ЯПОНИЯ | 🇬🇧 ВЕЛИКОБРИТАНИЯ
#    👥 КЛАНЫ ДО 50 ЧЕЛОВЕК // КЛАНОВЫЕ БОИ И РЕЙТИНГ
#    🔧 МЕХАНИКИ WoT/WT/TB: ПРОБИТИЕ, РИКОШЕТЫ, КРИТЫ, СНАРЯДЫ
#    👑 АДМИНУ ОТКРЫТЫ ВСЕ ВОЗМОЖНОСТИ (МОДЕРАТОРСКАЯ ПАНЕЛЬ)
# =============================================================

# -------------------- ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ --------------------
player_name = ""
player_country = "СССР"
coins = 200
energy = 100
current_level = 1
cups = 0
bimbersk = 0
title = ""
titles = []

promocode_uses_left = 500
player_class = "ТАНК"
admin_power = False
is_moderator = False
has_helper_privilege = False
has_titan_tank = False

current_platoon = []
my_friends = []

has_mushroom = False
immortality_active = False
immortality_start_time = 0
IMMORTALITY_DURATION = 60

last_bonus_date = ""

approved_admin_helpers = []
approved_mod_helpers = []

boss_150_defeated = False
boss_500_defeated = False

# ---------- КЛАНЫ ----------
clan_name = ""
clan_role = ""
clan_balance = 0
clan_members = []
clan_rating = 0
clan_boss_defeated = False
all_clans = {}

# ---------- МЕХАНИКИ WoT/WT/TB ----------
experience = 0
crew_skills = {"наводчик": 0, "механик": 0, "заряжающий": 0}
modules = {
    "орудие": 1,
    "броня": 1,
    "двигатель": 1,
    "радио": 1
}
ammo_type = "Бронебойный"
scrap = 0

# 500 титулов
ADJECTIVES = [
    "Храбрый", "Могучий", "Бесстрашный", "Смелый", "Отважный",
    "Сильный", "Мудрый", "Быстрый", "Ловкий", "Умелый",
    "Грозный", "Неустрашимый", "Железный", "Стальной", "Огненный",
    "Ледяной", "Громовой", "Молниеносный", "Тихий", "Яркий",
    "Тёмный", "Светлый", "Древний", "Молодой", "Вечный"
]
NOUNS = [
    "Воин", "Танкист", "Лётчик", "Снайпер", "Разведчик",
    "Штурмовик", "Защитник", "Победитель", "Герой", "Легенда",
    "Миф", "Титан", "Гигант", "Волк", "Орёл",
    "Сокол", "Беркут", "Медведь", "Дракон", "Феникс",
    "Самурай", "Рыцарь", "Варвар", "Космонавт", "Пилот"
]
ALL_TITLES = [f"{adj} {noun}" for adj in ADJECTIVES for noun in NOUNS]

COUNTRY_TECH = {
    "СССР": {
        "ТАНК": "Тяжелый Т-34 Квант (СССР) ☭",
        "САМОЛЕТ": "Истребитель Як-Сверхзвуковой (СССР) ☭",
        "РОБОТ": "Боевой робот 'Молот' (СССР) ☭",
        "ЗЕНИТКА": "Зенитная установка ЗСУ-23-4 (СССР) ☭",
        "hp_bonus": 150,
        "dmg_bonus": 5
    },
    "ГЕРМАНИЯ": {
        "ТАНК": "Тяжелый Тигр-Модерн (Германия) 🇩🇪",
        "САМОЛЕТ": "Штурмовик Мессершмитт-Альфа (Германия) 🇩🇪",
        "РОБОТ": "Робот-панцер (Германия) 🇩🇪",
        "ЗЕНИТКА": "Зенитка Flakpanzer Gepard (Германия) 🇩🇪",
        "hp_bonus": 80,
        "dmg_bonus": 25
    },
    "ЯПОНИЯ": {
        "ТАНК": "Шагающий танк Самурай-Квант (Япония) 🇯🇵",
        "САМОЛЕТ": "Истребитель Зеро-Нео (Япония) 🇯🇵",
        "РОБОТ": "Робот-меха (Япония) 🇯🇵",
        "ЗЕНИТКА": "Зенитная установка Type 87 (Япония) 🇯🇵",
        "hp_bonus": 50,
        "dmg_bonus": 15
    },
    "ВЕЛИКОБРИТАНИЯ": {
        "ТАНК": "Черчилль-Модерн (Великобритания) 🇬🇧",
        "САМОЛЕТ": "Спитфайр-Нео (Великобритания) 🇬🇧",
        "РОБОТ": "Робот-сентинел (Великобритания) 🇬🇧",
        "ЗЕНИТКА": "Зенитка Falcon (Великобритания) 🇬🇧",
        "hp_bonus": 120,
        "dmg_bonus": 20
    }
}

# -------------------- ФУНКЦИИ СОХРАНЕНИЯ / ЗАГРУЗКИ --------------------
def save_game():
    global player_name, player_country, coins, energy, current_level, cups, player_class, admin_power, bimbersk
    global promocode_uses_left, has_mushroom, immortality_active, is_moderator, has_helper_privilege
    global current_platoon, my_friends, last_bonus_date, approved_admin_helpers, approved_mod_helpers
    global title, titles, boss_150_defeated, boss_500_defeated, has_titan_tank
    global clan_name, clan_role, clan_balance, clan_members, clan_rating, clan_boss_defeated, all_clans
    global experience, crew_skills, modules, ammo_type, scrap

    save_data = {
        "player_name": player_name,
        "player_country": player_country,
        "coins": coins,
        "energy": energy,
        "current_level": current_level,
        "cups": cups,
        "player_class": player_class,
        "admin_power": admin_power,
        "bimbersk": bimbersk,
        "promocode_uses_left": promocode_uses_left,
        "has_mushroom": has_mushroom,
        "immortality_active": immortality_active,
        "is_moderator": is_moderator,
        "has_helper_privilege": has_helper_privilege,
        "current_platoon": current_platoon,
        "my_friends": my_friends,
        "last_bonus_date": last_bonus_date,
        "approved_admin_helpers": approved_admin_helpers,
        "approved_mod_helpers": approved_mod_helpers,
        "title": title,
        "titles": titles,
        "boss_150_defeated": boss_150_defeated,
        "boss_500_defeated": boss_500_defeated,
        "has_titan_tank": has_titan_tank,
        "clan_name": clan_name,
        "clan_role": clan_role,
        "clan_balance": clan_balance,
        "clan_members": clan_members,
        "clan_rating": clan_rating,
        "clan_boss_defeated": clan_boss_defeated,
        "all_clans": all_clans,
        "experience": experience,
        "crew_skills": crew_skills,
        "modules": modules,
        "ammo_type": ammo_type,
        "scrap": scrap
    }
    try:
        with open("savegame.json", "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

def load_game():
    global player_name, player_country, coins, energy, current_level, cups, player_class, admin_power, bimbersk
    global promocode_uses_left, has_mushroom, immortality_active, is_moderator, has_helper_privilege
    global current_platoon, my_friends, last_bonus_date, approved_admin_helpers, approved_mod_helpers
    global title, titles, boss_150_defeated, boss_500_defeated, has_titan_tank
    global clan_name, clan_role, clan_balance, clan_members, clan_rating, clan_boss_defeated, all_clans
    global experience, crew_skills, modules, ammo_type, scrap

    try:
        with open("savegame.json", "r", encoding="utf-8") as f:
            save_data = json.load(f)
            player_name = save_data.get("player_name", player_name)
            player_country = save_data.get("player_country", player_country)
            coins = save_data.get("coins", coins)
            energy = save_data.get("energy", energy)
            current_level = save_data.get("current_level", current_level)
            cups = save_data.get("cups", cups)
            player_class = save_data.get("player_class", player_class)
            admin_power = save_data.get("admin_power", admin_power)
            bimbersk = save_data.get("bimbersk", bimbersk)
            promocode_uses_left = save_data.get("promocode_uses_left", promocode_uses_left)
            has_mushroom = save_data.get("has_mushroom", has_mushroom)
            immortality_active = save_data.get("immortality_active", immortality_active)
            is_moderator = save_data.get("is_moderator", is_moderator)
            has_helper_privilege = save_data.get("has_helper_privilege", has_helper_privilege)
            current_platoon = save_data.get("current_platoon", current_platoon)
            my_friends = save_data.get("my_friends", my_friends)
            last_bonus_date = save_data.get("last_bonus_date", last_bonus_date)
            approved_admin_helpers = save_data.get("approved_admin_helpers", approved_admin_helpers)
            approved_mod_helpers = save_data.get("approved_mod_helpers", approved_mod_helpers)
            title = save_data.get("title", title)
            titles = save_data.get("titles", titles)
            boss_150_defeated = save_data.get("boss_150_defeated", boss_150_defeated)
            boss_500_defeated = save_data.get("boss_500_defeated", boss_500_defeated)
            has_titan_tank = save_data.get("has_titan_tank", has_titan_tank)
            clan_name = save_data.get("clan_name", clan_name)
            clan_role = save_data.get("clan_role", clan_role)
            clan_balance = save_data.get("clan_balance", clan_balance)
            clan_members = save_data.get("clan_members", clan_members)
            clan_rating = save_data.get("clan_rating", clan_rating)
            clan_boss_defeated = save_data.get("clan_boss_defeated", clan_boss_defeated)
            all_clans = save_data.get("all_clans", all_clans)
            experience = save_data.get("experience", experience)
            crew_skills = save_data.get("crew_skills", crew_skills)
            modules = save_data.get("modules", modules)
            ammo_type = save_data.get("ammo_type", ammo_type)
            scrap = save_data.get("scrap", scrap)
    except Exception:
        pass

    # Если админ, то автоматически даём ему модераторские права
    if admin_power:
        is_moderator = True

load_game()

# -------------------- ПРОВЕРКА ПРИВИЛЕГИЙ --------------------
def update_helper_privilege():
    global has_helper_privilege, player_name
    has_helper_privilege = (player_name.upper() in [n.upper() for n in approved_admin_helpers] or
                            player_name.upper() in [n.upper() for n in approved_mod_helpers])

# -------------------- ФУНКЦИИ ИГРЫ --------------------
def draw_dynamic_wallpaper():
    print("\n" + "=" * 65)
    if player_country == "СССР":
        flag = "☭"
    elif player_country == "ГЕРМАНИЯ":
        flag = "🇩🇪"
    elif player_country == "ЯПОНИЯ":
        flag = "🇯🇵"
    else:
        flag = "🇬🇧"
    print(f" {flag}  ⭐  [ ВОЕННЫЙ СЕКТОР ФРАКЦИИ: {player_country} ]  ⭐  {flag} ")
    print("=" * 65)

def get_tech_name(country=None, pclass=None):
    if country is None:
        country = player_country
    if pclass is None:
        pclass = player_class
    if admin_power:
        return "★ СУПЕР-ТАНК 'ТИТАН-АДМИН' (УЛЬТИМАТИВНЫЙ) ★"
    if has_titan_tank:
        return "⚡ ЛЕГЕНДАРНЫЙ ТИТАН-ТАНК ⚡"
    return COUNTRY_TECH[country].get(pclass, f"Машина {country}")

def get_max_hp(country=None, pclass=None, titan=False):
    if country is None:
        country = player_country
    if pclass is None:
        pclass = player_class
    if immortality_active:
        return 999999999
    if admin_power:
        return 1000000000000000
    if pclass == "ТАНК":
        bonus = COUNTRY_TECH[country].get("hp_bonus", 0)
    elif pclass == "САМОЛЕТ":
        bonus = COUNTRY_TECH[country].get("hp_bonus", 0) // 2
    elif pclass == "РОБОТ":
        bonus = COUNTRY_TECH[country].get("hp_bonus", 0) * 2
    elif pclass == "ЗЕНИТКА":
        bonus = COUNTRY_TECH[country].get("hp_bonus", 0)
    else:
        bonus = 0
    bonus += modules["броня"] * 10
    if titan or has_titan_tank:
        bonus += 50
    return 100 + bonus

def get_damage(country=None, pclass=None, titan=False):
    if country is None:
        country = player_country
    if pclass is None:
        pclass = player_class
    if immortality_active:
        return 999999999
    if admin_power:
        return 1000000000
    if pclass == "ТАНК":
        bonus = COUNTRY_TECH[country].get("dmg_bonus", 0)
        base = 25
    elif pclass == "САМОЛЕТ":
        bonus = COUNTRY_TECH[country].get("dmg_bonus", 0) * 2
        base = 30
    elif pclass == "РОБОТ":
        bonus = COUNTRY_TECH[country].get("dmg_bonus", 0) // 2
        base = 20
    elif pclass == "ЗЕНИТКА":
        bonus = COUNTRY_TECH[country].get("dmg_bonus", 0) * 3
        base = 35
    else:
        bonus = 0
        base = 25
    bonus += modules["орудие"] * 5
    if titan or has_titan_tank:
        bonus += 10
    return base + bonus

def give_new_title():
    global title, titles
    available = [t for t in ALL_TITLES if t not in titles]
    if available:
        new_title = random.choice(available)
        titles.append(new_title)
        title = new_title
        print(f" 🏅 ПОЛУЧЕН НОВЫЙ ТИТУЛ: {new_title}!")
        return True
    return False

def reset_profile():
    global player_name, player_country, coins, energy, current_level, cups, bimbersk
    global admin_power, is_moderator, has_helper_privilege, has_mushroom, immortality_active
    global current_platoon, title, titles, boss_150_defeated, boss_500_defeated, has_titan_tank
    global clan_name, clan_role, clan_balance, clan_members, clan_rating, clan_boss_defeated
    global experience, crew_skills, modules, ammo_type, scrap
    player_name = ""
    player_country = "СССР"
    coins = 200
    energy = 100
    current_level = 1
    cups = 0
    bimbersk = 0
    admin_power = False
    is_moderator = False
    has_helper_privilege = False
    has_mushroom = False
    immortality_active = False
    current_platoon = []
    title = ""
    titles = []
    boss_150_defeated = False
    boss_500_defeated = False
    has_titan_tank = False
    clan_name = ""
    clan_role = ""
    clan_balance = 0
    clan_members = []
    clan_rating = 0
    clan_boss_defeated = False
    experience = 0
    crew_skills = {"наводчик": 0, "механик": 0, "заряжающий": 0}
    modules = {"орудие": 1, "броня": 1, "двигатель": 1, "радио": 1}
    ammo_type = "Бронебойный"
    scrap = 0
    save_game()
    print(" 👤 Вы вышли из профиля. Для входа введите новый ник.")

def delete_profile():
    confirm = input(" ⚠️ ВЫ УВЕРЕНЫ, ЧТО ХОТИТЕ УДАЛИТЬ ПРОФИЛЬ? (да/нет): ").strip().lower()
    if confirm == "да":
        try:
            os.remove("savegame.json")
            print(" 🗑️ Профиль успешно удалён. Игра будет перезапущена.")
            sys.exit(0)
        except Exception as e:
            print(f" ❌ Ошибка удаления: {e}")
    else:
        print(" ❌ Удаление отменено.")

# -------------------- ФУНКЦИИ КЛАНОВ --------------------
def create_clan(clan_name_new):
    global clan_name, clan_role, clan_balance, clan_members, clan_rating, all_clans, coins
    if clan_name:
        print(" ❌ Вы уже состоите в клане! Покините его сначала.")
        return False
    if clan_name_new in all_clans:
        print(" ❌ Клан с таким именем уже существует!")
        return False
    if coins < 1000:
        print(" ❌ Не хватает 1000 монет для создания клана!")
        return False
    coins -= 1000
    clan_name = clan_name_new
    clan_role = "лидер"
    clan_members = [player_name]
    clan_balance = 0
    clan_rating = 0
    all_clans[clan_name] = {
        "leader": player_name,
        "members": [player_name],
        "balance": 0,
        "rating": 0
    }
    print(f" ✅ Клан '{clan_name}' создан! Вы стали лидером.")
    save_game()
    return True

def join_clan(clan_name_target):
    global clan_name, clan_role, clan_members, clan_balance, clan_rating, all_clans
    if clan_name:
        print(" ❌ Вы уже в клане!")
        return
    if clan_name_target not in all_clans:
        print(" ❌ Клана с таким именем не существует!")
        return
    if len(all_clans[clan_name_target]["members"]) >= 50:
        print(" ❌ В клане уже 50 участников, место занято!")
        return
    clan_name = clan_name_target
    clan_role = "рядовой"
    clan_members = all_clans[clan_name_target]["members"]
    all_clans[clan_name_target]["members"].append(player_name)
    clan_balance = all_clans[clan_name]["balance"]
    clan_rating = all_clans[clan_name]["rating"]
    print(f" ✅ Вы вступили в клан '{clan_name}'!")
    save_game()

def leave_clan():
    global clan_name, clan_role, clan_members, clan_balance, clan_rating, all_clans
    if not clan_name:
        print(" ❌ Вы не состоите в клане!")
        return
    if clan_role == "лидер":
        print(" ❌ Лидер не может покинуть клан! Передайте лидерство или распустите клан.")
        return
    all_clans[clan_name]["members"].remove(player_name)
    clan_members = all_clans[clan_name]["members"]
    clan_name = ""
    clan_role = ""
    clan_balance = 0
    clan_rating = 0
    print(" ✅ Вы покинули клан.")
    save_game()

def disband_clan():
    global clan_name, clan_role, clan_members, clan_balance, clan_rating, all_clans
    if not clan_name:
        print(" ❌ Вы не в клане!")
        return
    if clan_role != "лидер":
        print(" ❌ Только лидер может распустить клан!")
        return
    confirm = input(f" ⚠️ Точно распустить клан '{clan_name}'? (да/нет): ").strip().lower()
    if confirm == "да":
        del all_clans[clan_name]
        clan_name = ""
        clan_role = ""
        clan_members = []
        clan_balance = 0
        clan_rating = 0
        print(" ✅ Клан распущен.")
        save_game()
    else:
        print(" ❌ Отмена.")

def clan_boss_fight():
    global clan_name, clan_members, clan_balance, clan_rating, clan_boss_defeated, coins, cups, energy, all_clans
    if not clan_name:
        print(" ❌ Вы не в клане!")
        return
    if clan_boss_defeated:
        print(" ❌ Сегодня клановый босс уже побеждён! Приходите завтра.")
        return
    if energy < 30:
        print(" ❌ У вас недостаточно энергии для кланового боя (нужно 30).")
        return
    energy -= 30
    members_count = len(clan_members)
    boss_hp = 500 + members_count * 100
    boss_damage = 20 + members_count * 5
    print(f"\n🔥 КЛАНОВЫЙ БОСС (участников: {members_count})")
    print(f"❤️ HP босса: {boss_hp}, ⚔️ Урон босса: {boss_damage}")
    total_damage = 0
    for member in clan_members:
        dmg = random.randint(15, 35) + (10 if member == player_name else 0)
        total_damage += dmg
        print(f"  - {member} нанёс {dmg} урона.")
    if total_damage >= boss_hp:
        print(" 🎉 КЛАНОВЫЙ БОСС ПОВЕРЖЕН!")
        clan_boss_defeated = True
        reward_coins = 300 + members_count * 50
        reward_cups = 50 + members_count * 10
        clan_balance += reward_coins // 2
        coins += reward_coins // 2
        cups += reward_cups
        clan_rating += 100
        print(f" 💰 Каждый получил {reward_coins//2} монет и {reward_cups} кубков.")
        print(f" 🏆 Рейтинг клана увеличен на 100.")
        all_clans[clan_name]["balance"] = clan_balance
        all_clans[clan_name]["rating"] = clan_rating
        save_game()
    else:
        print(" 💀 БОСС ВЫЖИЛ! Попробуйте ещё раз завтра.")

def show_clan_info():
    global clan_name, clan_role, clan_members, clan_balance, clan_rating, all_clans
    if not clan_name:
        print(" ❌ Вы не в клане!")
        return
    print(f"\n🏰 КЛАН: {clan_name}")
    print(f"   Лидер: {all_clans[clan_name]['leader']}")
    print(f"   Ваша роль: {clan_role}")
    print(f"   Участников: {len(clan_members)}/50")
    print(f"   Казна: {clan_balance} монет")
    print(f"   Рейтинг: {clan_rating}")
    print(f"\n👥 УЧАСТНИКИ:")
    for i, member in enumerate(clan_members, 1):
        print(f"   {i}. {member} {'⭐' if member == all_clans[clan_name]['leader'] else ''}")

def show_clan_ranking():
    if not all_clans:
        print(" ❌ Нет зарегистрированных кланов.")
        return
    print("\n🏆 РЕЙТИНГ КЛАНОВ:")
    sorted_clans = sorted(all_clans.items(), key=lambda x: x[1]['rating'], reverse=True)
    for i, (name, data) in enumerate(sorted_clans, 1):
        print(f"   {i}. {name} — рейтинг: {data['rating']}, участников: {len(data['members'])}")

# -------------------- НАЧАЛЬНАЯ РЕГИСТРАЦИЯ --------------------
if not player_name:
    print("\n🌍 ЗАПУСК СИСТЕМЫ ИДЕНТИФИКАЦИИ СТУДИИ.")
    raw_name = input(" Введите ваш никнейм пилота взвода: ").strip()

    if not raw_name:
        player_name = "Пилот_Альфа"
        admin_power = False
        is_moderator = False
    else:
        if raw_name.upper() == "MUHAMMAD":
            password = input(" 🔒 Введите секретный ключ Мухаммада: ").strip()
            if password == "2026":
                player_name = "MUHAMMAD"
                admin_power = True
                is_moderator = True
                print(" 🎉 ДОСТУП ПРЕДОСТАВЛЕН! Приветствуем, Верховный Разработчик!")
            else:
                print(" ❌ НЕВЕРНЫЙ КЛЮЧ! АДМИНКА ЗАБЛОКИРОВАНА!")
                player_name = "Гость_Братан"
                admin_power = False
                is_moderator = False
        else:
            player_name = raw_name
            admin_power = False
            if player_name.upper() in ["АБУБАКР", "ABUBAKR"]:
                is_moderator = True
                print(" 🛡️ ВАМ ПРИСВОЕН СТАТУС МОДЕРАТОРА!")
            else:
                is_moderator = False

    if player_name.upper() not in [n.upper() for n in my_friends]:
        my_friends.append(player_name)
        print(f" 👤 Игрок {player_name} зарегистрирован в системе.")

    print("\n🌍 ВЫБЕРИТЕ ВАШУ ВОЕННУЮ ДЕРЖАВУ:")
    print(" 1. ☭ СССР\n 2. 🇩🇪 ГЕРМАНИЯ\n 3. 🇯🇵 ЯПОНИЯ\n 4. 🇬🇧 ВЕЛИКОБРИТАНИЯ")
    country_choice = input(" Введите номер страны (1-4): ").strip()
    if country_choice == '2':
        player_country = "ГЕРМАНИЯ"
    elif country_choice == '3':
        player_country = "ЯПОНИЯ"
    elif country_choice == '4':
        player_country = "ВЕЛИКОБРИТАНИЯ"
    else:
        player_country = "СССР"

    if player_name.upper() not in [n.upper() for n in current_platoon]:
        current_platoon.append(player_name)

    if not titles:
        give_new_title()

    update_helper_privilege()
    save_game()

# -------------------- ОСНОВНОЙ ИГРОВОЙ ЦИКЛ --------------------
while True:
    save_game()
    draw_dynamic_wallpaper()

    if admin_power:
        print(f" 👑  [ СТАТУС: ВЕРХОВНЫЙ РАЗРАБОТЧИК ] Ник: {player_name.upper()} [⭐ VIP] 👑")
    elif is_moderator:
        print(f" 🛡️  [ СТАТУС: МОДЕРАТОР ] Ник: {player_name.upper()} [⚡]")
    else:
        print(f"   ИГРОК: {player_name.upper()} // ЧЕСТНЫЙ БАЛАНС")

    if has_helper_privilege:
        print("   🤝 ПРИВИЛЕГИЯ ХЕЛПЕР (бонусы активны)")

    if title:
        print(f"   🏅 ТЕКУЩИЙ ТИТУЛ: {title}")

    if has_titan_tank:
        print("   ⚡ [ТИТАН-ТАНК АКТИВИРОВАН] ⚡")

    if clan_name:
        print(f"   🏰 КЛАН: {clan_name} (роль: {clan_role})")

    print(f"   🌍 РОДНАЯ СТРАНА: {player_country} | 👥 ВЗВОД: {', '.join(current_platoon)} [{len(current_platoon)}/10]")
    print("-" * 65)
    print(f" 💰  МОНЕТЫ: {coins} 🟡 | 🏆 КУБКИ БП: {cups} | 💎 БИМБЕРСК: {bimbersk}")
    print(f" 🔋  ЗАПАС ЭНЕРГИИ БАЗЫ: {energy}/100 🔌")
    print(f" ⭐  ОПЫТ: {experience} | 🧩 Обломков: {scrap}")
    print(f" 🧨  ТИП СНАРЯДА: {ammo_type}")
    print(f" 🌍  АКТИВНЫЙ ФРОНТ:    {player_class}")
    print(f" 🦾  МОДИФИКАЦИЯ ТЕХНИКИ: {get_tech_name()}")
    print(f" ❤️  ПРОЧНОСТЬ ОБШИВКИ: {get_max_hp()} HP | ⚔️ УРОН ОРУДИЯ: {get_damage()}")
    print(f" 📊  УРОВЕНЬ: {current_level} / 2000")
    if immortality_active:
        remaining = max(0, int(IMMORTALITY_DURATION - (time.time() - immortality_start_time)))
        print(f" 🍄 БЕССМЕРТИЕ АКТИВНО! Осталось: {remaining} сек.")
    if has_mushroom:
        print(" 🍄 У вас есть легендарный грибок почек (активируйте перед боем)")

    print("-" * 65)
    print(" 1. ⚔️  НАЧАТЬ МИССИЮ ВЗВОДОМ (В БОЙ!)")
    print(" 2. 🔄  СМЕНА КЛАССА ТЕХНИКИ (ТАНКИ / САМОЛЕТЫ / РОБОТЫ / ЗЕНИТКИ)")
    print(" 3. 🌍  ИЗМЕНИТЬ ВОЕННУЮ ДЕРЖАВУ (СССР / ГЕРМАНИЯ / ЯПОНИЯ / ВЕЛИКОБРИТАНИЯ)")
    print(" 4. 🏆  БОЕВОЙ ПРОПУСК (ПОЛУЧИТЬ ТИТАН-ТАНК)")
    print(" 5. 🎒  ШКОЛЬНЫЕ МИССИИ ЗНАНИЙ")
    print(" 6. 🎟️  ТЕРМИНАЛ ПРОМОКОДОВ")
    print(" 7. 🍄  АКТИВИРОВАТЬ ГРИБОК (если есть)")
    print(" 8. 👥  ДРУЗЬЯ И ПРИГЛАШЕНИЕ ВО ВЗВОД (ДО 10 ЧЕЛОВЕК)")
    print(" 9. 🛒  МАГАЗИН")
    print(" 10. 📈 ПРОКАЧКА (опыт / уровень)")
    print(" 11. 🎁 ЕЖЕДНЕВНЫЙ БОНУС")
    print(" 12. 🎟️ СТАТЬ МОДЕРАТОРОМ (секретный промокод)")
    if is_moderator or admin_power:
        print(" 13. 🛡️ МОДЕРАТОРСКАЯ ПАНЕЛЬ")
    print(" 14. 🚪  ВЫЙТИ ИЗ ИГРЫ")
    print(" 15. 👤  ПРОФИЛЬ (титулы, статистика, выход/удаление)")
    print(" 16. 🏰 КЛАНЫ (создать, вступить, босс, рейтинг)")
    print("-" * 65)

    # ========== ИСПРАВЛЕННЫЙ БЛОК ВВОДА ==========
    raw_in = input(" Введите номер действия (1-16) и нажмите Enter: ").strip()
    digits = ''.join(filter(str.isdigit, raw_in))
    if not digits:
        print("❌ Введите номер действия цифрами!")
        input("Нажмите Enter...")
        continue
    # Проверяем допустимость
    if len(digits) == 1:
        choice = int(digits)
        if choice < 1 or choice > 9:
            print("❌ Номер действия должен быть от 1 до 9 или 16!")
            input("Нажмите Enter...")
            continue
    elif len(digits) == 2 and digits == "16":
        choice = 16
    else:
        print("❌ Некорректный ввод! Допустимы только 1-9 или 16.")
        input("Нажмите Enter...")
        continue
    # =============================================

    if choice == 14:
        print("\n🚪 Выход из игры. До встречи, брат!")
        save_game()
        break

    # -------------------- ОБРАБОТКА ДЕЙСТВИЙ --------------------
    if choice == 1:
        if energy < 20 and not admin_power:
            print("\n❌ Энергия исчерпана!")
            input("\nНажмите Enter...")
            continue
        if not admin_power:
            energy -= 20

        print(f"\n⚔️  ВЗВОД ДЕРЖАВЫ {player_country} ВЫДВИНУЛСЯ В БОЙ!")
        print(f"💥 Сражение ведётся на технике: {get_tech_name()}")
        print(f"🧨 Выбранный снаряд: {ammo_type}")

        if immortality_active:
            elapsed = time.time() - immortality_start_time
            if elapsed < IMMORTALITY_DURATION:
                print(f"🍄 ВЫ БЕССМЕРТНЫ! Осталось {int(IMMORTALITY_DURATION - elapsed)} сек.")
            else:
                print("⏳ Эффект грибка истёк.")
                immortality_active = False

        # --- СИСТЕМА БОЯ С ПРОБИТИЕМ (WoT/WT/TB) ---
        enemy_hp = 100 + random.randint(0, 50)
        enemy_armor = random.choice(["лоб", "борт", "корма"])
        enemy_angle = random.uniform(0.8, 1.2)
        enemy_class = random.choice(["ТАНК", "САМОЛЕТ", "РОБОТ", "ЗЕНИТКА"])
        print(f"👾 Враг: {enemy_class}, HP: {enemy_hp}, броня: {enemy_armor}")

        hit_sector = random.choice(["лоб", "борт", "корма"])
        armor_multiplier = {"лоб": 1.0, "борт": 0.7, "корма": 0.5}[hit_sector]
        effective_armor = enemy_hp * armor_multiplier * enemy_angle

        base_damage = get_damage()
        ammo_multiplier = {"Бронебойный": 1.0, "Кумулятивный": 0.8, "ОФ": 1.3}[ammo_type]
        penetration = random.uniform(0.7, 1.3) * base_damage * ammo_multiplier

        if penetration > effective_armor:
            damage = int(penetration * random.uniform(0.8, 1.2))
            enemy_hp -= damage
            print(f"✅ Попадание! Урон: {damage}")
            if random.random() < 0.15:
                crit = random.choice(["двигатель", "гусеница", "боеукладка"])
                if crit == "двигатель":
                    print("🔥 Критическое попадание: двигатель повреждён! Скорость снижена.")
                elif crit == "гусеница":
                    print("⚙️ Критическое попадание: гусеница сбита! Машина обездвижена.")
                else:
                    print("💥 Критическое попадание: боеукладка! Взрыв!")
                    enemy_hp -= int(enemy_hp * 0.5)
        else:
            print("💢 Рикошет! Снаряд не пробил броню.")
            enemy_hp -= int(base_damage * 0.1)

        if enemy_hp > 0:
            enemy_damage = random.randint(5, 20)
            print(f"💢 Враг нанёс {enemy_damage} урона.")
        else:
            print("🎉 Враг уничтожен!")

        # Награды
        exp_gain = 20 + random.randint(0, 30)
        coins_gain = 100 + random.randint(0, 50)
        scrap_gain = random.randint(0, 5)
        experience += exp_gain
        coins += coins_gain
        scrap += scrap_gain
        cups += 10
        current_level += 1

        # Боссы
        if current_level == 150 and not boss_150_defeated:
            print(" 💀 ВСТРЕЧАЙТЕ БОССА: МИСТЕР БЛИВИС! (уровень 150)")
            coins += 1000
            cups += 500
            current_level += 5
            boss_150_defeated = True
            if "Победитель Мистера Бливиса" not in titles:
                titles.append("Победитель Мистера Бливиса")
                title = "Победитель Мистера Бливиса"
                print(" 🏅 ПОЛУЧЕН ТИТУЛ: Победитель Мистера Бливиса!")
            print(" 🎉 ВЫ ОДОЛЕЛИ МИСТЕРА БЛИВИСА! +1000 монет, +500 кубков, +5 уровней!")

        if current_level == 500 and not boss_500_defeated:
            print(" 💀 ВСТРЕЧАЙТЕ БОССА: ДИРЕКТОР БОЛИВИЗ! (уровень 500)")
            coins += 5000
            cups += 2000
            current_level += 10
            boss_500_defeated = True
            if "Первоклассник" not in titles:
                titles.append("Первоклассник")
                title = "Первоклассник"
                print(" 🏅 ПОЛУЧЕН ТИТУЛ: ПЕРВОКЛАССНИК!")
            print(" 🎉 ВЫ ОДОЛЕЛИ ДИРЕКТОРА БОЛИВИЗА! +5000 монет, +2000 кубков, +10 уровней!")

        if len(titles) < 500:
            give_new_title()

        if immortality_active:
            immortality_active = False
            print("🍄 Грибок перестал действовать после завершения миссии.")

        print(f"📈 Получено: {exp_gain} опыта, {coins_gain} монет, {scrap_gain} обломков.")
        input("\nБоевая миссия успешно завершена! Нажмите Enter...")

    elif choice == 2:
        print("\n🔄 1. ТАНКИ | 2. САМОЛЕТЫ | 3. РОБОТЫ | 4. ЗЕНИТКИ")
        c_front = input(" Введите номер фронта: ").strip()
        if c_front == '1':
            player_class = "ТАНК"
        elif c_front == '2':
            player_class = "САМОЛЕТ"
        elif c_front == '3':
            player_class = "РОБОТ"
        elif c_front == '4':
            player_class = "ЗЕНИТКА"
        else:
            print(" ❌ Неверный выбор, оставлен текущий класс.")

    elif choice == 3:
        print("\n🌍 СМЕНА ГОСУДАРСТВЕННОГО СЕКТОРА:")
        print(" 1. ☭ СССР\n 2. 🇩🇪 ГЕРМАНИЯ\n 3. 🇯🇵 ЯПОНИЯ\n 4. 🇬🇧 ВЕЛИКОБРИТАНИЯ")
        c_choice = input(" Выберите новую страну (1-4): ").strip()
        if c_choice == '2':
            player_country = "ГЕРМАНИЯ"
        elif c_choice == '3':
            player_country = "ЯПОНИЯ"
        elif c_choice == '4':
            player_country = "ВЕЛИКОБРИТАНИЯ"
        else:
            player_country = "СССР"
        print(f"🛰️ Фракция успешно изменена на {player_country}!")
        input("\nНажмите Enter...")

    elif choice == 4:
        print("\n🏆 БОЕВОЙ ПРОПУСК")
        if has_titan_tank:
            print(" ❌ У вас уже есть Титан-танк! Вы не можете получить его снова.")
        else:
            has_titan_tank = True
            print(" 🚀 ПОЗДРАВЛЯЕМ! ВЫ ПОЛУЧИЛИ ЛЕГЕНДАРНЫЙ ТИТАН-ТАНК!")
            print(" ⚡ Теперь ваша техника усилена (+50 HP, +10 урона).")
            coins += 500
            cups += 50
            print(" 💰 Дополнительно вы получили 500 монет и 50 кубков!")
        input("\nНажмите Enter...")

    elif choice == 5:
        print("\n🎒 ШКОЛЬНЫЕ МИССИИ ЗНАНИЙ")
        print(" 📚 Здесь будут задания по математике, физике и истории.")
        print(" 🎯 За выполнение даются монеты и опыт.")
        print(" ⏳ Функция в разработке...")
        input("\nНажмите Enter...")

    elif choice == 6:
        print("\n 🎟️ ТЕРМИНАЛ АКТИВАЦИИ ПРОМОКОДОВ 🎟️")
        code = input(" Введите код: ").strip().upper()
        if code == "ШКОЛА_УРА":
            if promocode_uses_left > 0:
                promocode_uses_left -= 1
                coins += 50000
                print(" 🟡 Код выполнен успешно! +50 000 монет.")
            else:
                print(" ❌ Все активации промокода уже использованы!")
        else:
            print(" ❌ Неверный промокод.")
        input("\nНажмите Enter...")

    elif choice == 7:
        if not has_mushroom:
            print("❌ У вас нет грибка! Купите в магазине.")
        elif immortality_active:
            print("⏳ Грибок уже активен! Нельзя использовать новый до окончания текущего боя.")
        else:
            has_mushroom = False
            immortality_active = True
            immortality_start_time = time.time()
            print("🍄 ВЫ АКТИВИРОВАЛИ ГРИБОК! БЕССМЕРТИЕ НА 60 СЕКУНД В ЭТОМ БОЮ!")
        input("Нажмите Enter...")

    elif choice == 8:
        print("\n👥 ДРУЗЬЯ И ВЗВОД")
        print(" 1. ПРИГЛАСИТЬ ДРУГА ВО ВЗВОД (по нику)")
        print(" 2. ПОСМОТРЕТЬ СПИСОК ВСЕХ ЗАРЕГИСТРИРОВАННЫХ ИГРОКОВ")
        print(" 3. РАСПУСТИТЬ ВЗВОД")
        sub = input("Выберите действие: ").strip()
        if sub == '1':
            if len(current_platoon) >= 10:
                print(" ❌ Лимит взвода 10/10 игроков исчерпан!")
            else:
                friend_name = input(" Введите ник друга для приглашения: ").strip()
                if friend_name.upper() in [n.upper() for n in my_friends]:
                    if friend_name.upper() not in [n.upper() for n in current_platoon]:
                        current_platoon.append(friend_name)
                        print(f" ✅ {friend_name} добавлен во взвод!")
                    else:
                        print(" ❌ Этот игрок уже во взводе!")
                else:
                    print(" ❌ Игрок не зарегистрирован в системе.")
        elif sub == '2':
            print("\n📋 ВСЕ ЗАРЕГИСТРИРОВАННЫЕ ИГРОКИ:")
            for i, name in enumerate(my_friends, 1):
                status = " [Во взводе]" if name.upper() in [n.upper() for n in current_platoon] else ""
                print(f" {i}. {name}{status}")
        elif sub == '3':
            current_platoon = [player_name]
            print(" ✅ Взвод распущен. Вы остались в одиночестве.")
        input("\nНажмите Enter...")

    elif choice == 9:
        print("\n🛒 МАГАЗИН")
        print(" 1. Улучшить орудие (урон +5) – 500 монет + 10 обломков")
        print(" 2. Улучшить броню (HP +20) – 400 монет + 8 обломков")
        print(" 3. Купить энергетик (+50 энергии) – 200 монет")
        print(" 4. 🍄 ЛЕГЕНДАРНЫЙ ГРИБОК ПОЧЕК (бессмертие 60 сек) – 5000 монет")
        print(" 5. 💣 Сменить тип снаряда (Бронебойный/Кумулятивный/ОФ)")
        print(" 6. Назад")
        shop = input("Выберите товар: ").strip()
        if shop == '1':
            if coins >= 500 and scrap >= 10:
                coins -= 500
                scrap -= 10
                modules["орудие"] += 1
                print("✅ Орудие улучшено! Урон +5.")
            else:
                print("❌ Не хватает монет или обломков!")
        elif shop == '2':
            if coins >= 400 and scrap >= 8:
                coins -= 400
                scrap -= 8
                modules["броня"] += 1
                print("✅ Броня улучшена! HP +20.")
            else:
                print("❌ Не хватает монет или обломков!")
        elif shop == '3':
            if coins >= 200:
                coins -= 200
                energy = min(100, energy + 50)
                print("✅ Энергия восстановлена на 50!")
            else:
                print("❌ Не хватает монет!")
        elif shop == '4':
            if coins >= 5000 and not has_mushroom:
                coins -= 5000
                has_mushroom = True
                print("✅ Вы купили грибок! Используйте через пункт 7.")
            elif has_mushroom:
                print("❌ У вас уже есть грибок!")
            else:
                print("❌ Не хватает монет!")
        elif shop == '5':
            print("\nТипы снарядов:")
            print(" 1. Бронебойный (стандарт)")
            print(" 2. Кумулятивный (высокое пробитие)")
            print(" 3. Осколочно-фугасный (большой урон)")
            ammo_choice = input("Выберите тип: ").strip()
            if ammo_choice == '1':
                ammo_type = "Бронебойный"
            elif ammo_choice == '2':
                ammo_type = "Кумулятивный"
            elif ammo_choice == '3':
                ammo_type = "ОФ"
            else:
                print("Неверный выбор.")
        input("Нажмите Enter...")

    elif choice == 10:
        print("\n📈 ПРОКАЧКА")
        print(" 1. Повысить уровень (требуется 100 монет) – статы +5%")
        print(" 2. Обменять опыт на монеты (1 опыт = 2 монеты)")
        print(" 3. Назад")
        up = input("Действие: ").strip()
        if up == '1':
            if coins >= 100:
                coins -= 100
                current_level += 1
                print("✅ Уровень повышен!")
            else:
                print("❌ Недостаточно монет! Нужно 100.")
        elif up == '2':
            if experience > 0:
                coins += experience * 2
                print(f"💰 Обменяно {experience} опыта на {experience*2} монет.")
                experience = 0
            else:
                print("❌ Нет опыта.")
        input("Нажмите Enter...")

    elif choice == 11:
        print("\n🎁 ЕЖЕДНЕВНЫЙ БОНУС")
        today = datetime.now().strftime("%Y-%m-%d")
        if last_bonus_date == today:
            print("❌ Вы уже получали бонус сегодня! Приходите завтра.")
        else:
            bonus_coins = 200 + random.randint(0, 300)
            bonus_energy = 30
            if has_helper_privilege:
                bonus_coins = int(bonus_coins * 1.2)
                bonus_energy += 10
            if has_titan_tank:
                bonus_coins = int(bonus_coins * 1.1)
            coins += bonus_coins
            energy = min(100, energy + bonus_energy)
            last_bonus_date = today
            print(f"✅ Получено {bonus_coins} монет и {bonus_energy} энергии!")
        input("Нажмите Enter...")

    elif choice == 12:
        print("\n🎟️ СТАТЬ МОДЕРАТОРОМ")
        code = input(" Введите секретный промокод для получения статуса модератора: ").strip().upper()
        if code == "MODERATORJOB" and not is_moderator:
            is_moderator = True
            print(" ✅ ВЫ СТАЛИ МОДЕРАТОРОМ!")
        elif is_moderator:
            print(" ❌ Вы уже модератор!")
        else:
            print(" ❌ Неверный промокод.")
        input("Нажмите Enter...")

    elif choice == 13 and (is_moderator or admin_power):
        print("\n🛡️ МОДЕРАТОРСКАЯ ПАНЕЛЬ")
        print(" 1. Посмотреть список всех игроков (my_friends)")
        print(" 2. Выдать предупреждение (штраф 100 монет) игроку")
        print(" 3. Забанить игрока (удалить его сохранение)")
        print(" 4. Назначить помощника администратора (по нику)")
        print(" 5. Назначить помощника модератора (по нику)")
        print(" 6. Просмотреть списки помощников")
        print(" 7. Назад")
        mod_choice = input("Выберите действие: ").strip()
        if mod_choice == '1':
            print("\n📋 СПИСОК ВСЕХ ИГРОКОВ:")
            for i, name in enumerate(my_friends, 1):
                print(f" {i}. {name}")
        elif mod_choice == '2':
            target = input(" Введите ник игрока для штрафа: ").strip()
            if target.upper() in [n.upper() for n in my_friends]:
                print(f" ⚠️ Игроку {target} выписано предупреждение (штраф 100 монет).")
            else:
                print(" ❌ Игрок не найден.")
        elif mod_choice == '3':
            target = input(" Введите ник игрока для бана: ").strip()
            if target.upper() == player_name.upper():
                print(" ❌ Нельзя забанить самого себя!")
            elif target.upper() in [n.upper() for n in my_friends]:
                my_friends = [n for n in my_friends if n.upper() != target.upper()]
                if target.upper() in [n.upper() for n in current_platoon]:
                    current_platoon = [n for n in current_platoon if n.upper() != target.upper()]
                print(f" 🚫 Игрок {target} забанен и удалён из системы.")
            else:
                print(" ❌ Игрок не найден.")
        elif mod_choice == '4':
            target = input(" Введите ник для назначения помощником администратора: ").strip()
            if target.upper() in [n.upper() for n in my_friends]:
                if target.upper() not in [n.upper() for n in approved_admin_helpers]:
                    approved_admin_helpers.append(target)
                    print(f" ✅ {target} назначен помощником администратора.")
                else:
                    print(" ❌ Уже является помощником администратора.")
            else:
                print(" ❌ Игрок не зарегистрирован.")
        elif mod_choice == '5':
            target = input(" Введите ник для назначения помощником модератора: ").strip()
            if target.upper() in [n.upper() for n in my_friends]:
                if target.upper() not in [n.upper() for n in approved_mod_helpers]:
                    approved_mod_helpers.append(target)
                    print(f" ✅ {target} назначен помощником модератора.")
                else:
                    print(" ❌ Уже является помощником модератора.")
            else:
                print(" ❌ Игрок не зарегистрирован.")
        elif mod_choice == '6':
            print("\n🤝 ПОМОЩНИКИ АДМИНИСТРАТОРА:")
            for h in approved_admin_helpers:
                print(f" - {h}")
            print("\n🤝 ПОМОЩНИКИ МОДЕРАТОРА:")
            for h in approved_mod_helpers:
                print(f" - {h}")
        input("Нажмите Enter...")

    elif choice == 15:
        print("\n👤 ПРОФИЛЬ ИГРОКА")
        print(f"   Ник: {player_name}")
        print(f"   Страна: {player_country}")
        print(f"   Уровень: {current_level} / 2000")
        print(f"   Монеты: {coins}")
        print(f"   Кубки: {cups}")
        print(f"   Энергия: {energy}/100")
        print(f"   Бимберск: {bimbersk}")
        print(f"   Опыт: {experience}")
        print(f"   Обломки: {scrap}")
        print(f"   Тип снаряда: {ammo_type}")
        print(f"   Титулов получено: {len(titles)} / 500")
        print(f"   Титан-танк: {'✅ Есть' if has_titan_tank else '❌ Нет'}")
        if clan_name:
            print(f"   Клан: {clan_name} (роль: {clan_role})")
        else:
            print("   Клан: не состоит")
        print(f"   Класс техники: {player_class}")
        print(f"   Модули: Орудие={modules['орудие']}, Броня={modules['броня']}")
        print("\n🏅 СПИСОК ТИТУЛОВ:")
        if titles:
            for i, t in enumerate(titles, 1):
                print(f"   {i}. {t}")
        else:
            print("   (нет титулов)")
        print("\n 1. Выйти из профиля (сбросить игрока)")
        print(" 2. Удалить профиль (безвозвратно)")
        print(" 3. Назад")
        prof_choice = input("Выберите действие: ").strip()
        if prof_choice == '1':
            reset_profile()
            continue
        elif prof_choice == '2':
            delete_profile()
        else:
            input("Нажмите Enter...")

    elif choice == 16:
        print("\n🏰 КЛАНЫ")
        print(" 1. Показать информацию о моём клане")
        print(" 2. Создать клан (1000 монет)")
        print(" 3. Вступить в клан")
        print(" 4. Покинуть клан (только рядовой)")
        print(" 5. Распустить клан (только лидер)")
        print(" 6. Клановый босс (сражение)")
        print(" 7. Рейтинг кланов")
        print(" 8. Назад")
        clan_choice = input("Выберите действие: ").strip()
        if clan_choice == '1':
            show_clan_info()
        elif clan_choice == '2':
            name = input("Введите название нового клана: ").strip()
            if name:
                create_clan(name)
        elif clan_choice == '3':
            target = input("Введите название клана для вступления: ").strip()
            if target:
                join_clan(target)
        elif clan_choice == '4':
            leave_clan()
        elif clan_choice == '5':
            disband_clan()
        elif clan_choice == '6':
            clan_boss_fight()
        elif clan_choice == '7':
            show_clan_ranking()
        else:
            print("Возврат в главное меню.")
        input("Нажмите Enter...")

    else:
        print("❌ Неверный выбор.")
        input("Нажмите Enter...")