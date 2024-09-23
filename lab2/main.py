import sys

from swiplserver import PrologMQI

knowlege_base = "../lab1/part1.pl"

BROTHERHOOD_KNIGHT = ["братство стали", "a"]
VAULT_DWELLER = ["житель убежища", "b"]
RAIDER = ["рейдер", "c"]
MINUTEMAN = ["минитмен", "d"]
REQUEST_1 = "я хочу дружить с"
REQUEST_2 = "я хочу воевать с"
REQUEST_3 = "я хочу пойти в"

# Приветствовать пользователя, спрашивать его имя
def acquaintance():
    user_name = input("Введите имя: ")
    print(
        "Привет, "
        + user_name
        + "я помогу тебе в следующих вопросах: "
          "\n с кем ты можешь дружить, на кого нападать, а на кого не стоит, в каком месте тебя ждет опасность")


# Узнать фракцию
def fraction():
    print("тебе доступны следующие фракции:\na) Братство Стали\nb) Житель убежища\nc) Рейдер\nd) Минитмен")
    user_fraction = input("твой выбор: ").lower()
    return user_fraction


# Задает вопрос пользователю. Выделяет запрос и ключевое слово
def question():
    while True:
        print("\n=======================================================\n")
        print("Тебе могут встретиться такие персонажи: "
              "\nгуль, братство стали, житель убежища, рейдер, минитмен, супермутант, собака, коготь смерти. "
              "\nТакже ты можешь отправиться в следующие локации:"
              "\nубежище 13, бункер братства стали, лагерь рейдеров, собор, "
              "некрополь, автозаправочная станция, деревня, пустошь"
              "\nчто тебя интересует?"
              "\nтебе доступны следующие запросы:\n"
              + REQUEST_1 + " <название фракции в ИП>\n"
              + REQUEST_2 + " <название фракции в ИП>\n"
              + REQUEST_3 + " <название локации в ИП>")

        user_request = input("ваш запрос: ")
        if user_request == "exit":
            print("пока")
            sys.exit(0)
        if REQUEST_1 in user_request or REQUEST_2 in user_request or REQUEST_3 in user_request:
            key_word = (
                user_request
                .replace(REQUEST_1, "")
                .replace(REQUEST_2, "")
                .replace(REQUEST_3, "")
                .replace(" ", "")
            )
            user_request = user_request.replace(key_word, "")
            break
        else:
            print("Запрос не распознан")
    return user_request, key_word


# Отправка запроса в интерпретатор пролога
def request(user_request, key_word, user_fraction):

    # Перевод ключевого слова
    match key_word:
        case "гуль":
            key_word = "ghoul"
        case "братство стали":
            key_word = "brotherhood_knight"
        case "житель убежища":
            key_word = "vault_dweller"
        case "рейдер":
            key_word = "raider"
        case "минитмен":
            key_word = "minuteman"
        case "супермутант":
            key_word = "super_mutant"
        case "собака":
            key_word = "dog"
        case "коготь смерти":
            key_word = "deathclaw"
        case "убежище 13":
            key_word = "vault_13"
        case "бункер братства стали":
            key_word = "brotherhood_bunker"
        case "лагерь рейдеров":
            key_word = "raider_camp"
        case "собор":
            key_word = "cathedral"
        case "некрополь":
            key_word = "necropolis"
        case "автозаправочная станция":
            key_word = "gas_station"
        case "деревня":
            key_word = "village"
        case "пустошь":
            key_word = "wasteland"

    # Перевод типа запроса
    if REQUEST_1 in user_request:
        user_request = "ally"
    elif REQUEST_2 in user_request:
        user_request = "enemy"
    elif REQUEST_3 in user_request:
        user_request = "safe_location"

    # Перевод фракции пользователя
    if user_fraction in BROTHERHOOD_KNIGHT:
        user_fraction = "brotherhood_knight"
    elif user_fraction in VAULT_DWELLER:
        user_fraction = "vault_dweller"
    elif user_fraction in MINUTEMAN:
        user_fraction = "minuteman"
    elif user_fraction in RAIDER:
        user_fraction = "raider"

    prolog_request = user_request + "(" + user_fraction + ", " + key_word + ")."
    # print(prolog_request)

    # Создание соединения с Prolog
    with PrologMQI() as mqi:
        with mqi.create_thread() as prolog_thread:

            # Инициализируем нашу базу знаний
            prolog_thread.query(f"consult('{knowlege_base}').")

            response = prolog_thread.query(prolog_request)

            # Обработка ответа
            if response:
                if user_request == "ally":
                    print("С этим персонажем вы можете подружиться")
                if user_request == "enemy":
                    print("Это твой враг, стоит его убить")
                if user_request == "safe_location":
                    print("Это место безопасно для тебя, исследуй его")
            elif not response:
                if user_request == "ally":
                    print("С этим персонажем не получится подружиться, он твой враг!")
                if user_request == "enemy":
                    print("Этот персонаж тебе не враг, и лучше этого не менять")
                if user_request == "safe_location":
                    print("Это место опасно, там могут встретиться враги")
            else:
                return



if __name__ == "__main__":
    acquaintance()

    user_fraction = ""

    while True:
        user_fraction = fraction()
        if user_fraction in BROTHERHOOD_KNIGHT:
            print("Фракция братства стали топит за прогресс")
            break
        elif user_fraction in VAULT_DWELLER:
            print("Жители убежищ пережили войну в бункере и спят там уже сотни лет")
            break
        elif user_fraction in RAIDER:
            print("Рейдеры были воспитаны пустошью, жестокие и кровожадные")
            break
        elif user_fraction in MINUTEMAN:
            print("Минитмены пытаются возродить великую нацию")
            break
        else:
            print("Я не знаком с такой фракцией, либо ты допустил ошибку")

    while True:
        user_request, key_word = question()

        request(user_request, key_word, user_fraction)

