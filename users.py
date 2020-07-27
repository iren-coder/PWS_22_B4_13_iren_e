# В этом файле users.py находятся оба модуля (и регистрация новых пользователей, и find_athlete).
# В базе данных sochi_athletes.sqlite3 в таблице user создан 1 человек (я). Поэтому сравнение атлетов по росту и 
# и дате рождения происходит с 1 человеком, id = 1. При проверке, ВЫ можете добавить сколь угодно
# пользователей и провести сравнение с ними. У меня всё работало. )))) Хорошего дня!


import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# Импортируем библиотеку для работы с датами
from datetime import datetime, timedelta

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'user'
    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    # Пол пользователя
    gender = sa.Column(sa.Text)
    # Дата рождения пользователя
    birthdate = sa.Column(sa.Text)
    # Рост пользователя
    height = sa.Column(sa.FLOAT)

class Athelete(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'athelete'
    # идентификатор атлета, первичный ключ
    id = sa.Column(sa.Integer, primary_key=True)
    # возраст атлета
    age = sa.Column(sa.Integer)
    # Дата рождения атлета
    birthdate = sa.Column(sa.Text)
    # Пол атлета
    gender = sa.Column(sa.Text)
    # Рост атлета
    height = sa.Column(sa.FLOAT)
    # Имя атлета
    name = sa.Column(sa.Text)
    # Вес атлета
    weight = sa.Column(sa.Integer)
    # Золотые медали
    gold_medals = sa.Column(sa.Integer)
    # Серебряные медали
    silver_medals = sa.Column(sa.Integer)
    # Бронзовые медали
    bronze_medals = sa.Column(sa.Integer)
    # Всего медалей
    total_medals = sa.Column(sa.Integer)
    # Вид спорта
    sport = sa.Column(sa.Text)
    # Страна
    country = sa.Column(sa.Text)


def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()


def request_data():
    """
    Запрашивает у пользователя данные и добавляет их в список users
    """
    # выводим приветствие
    print("Привет! Я запишу твои данные!")
    # запрашиваем у пользователя данные
    first_name = input("Введи своё имя: ")
    last_name = input("А теперь фамилию: ")
    email = input("Адрес твоей электронной почты: ")
    gender = input("Укажите Ваш пол (Male/Female): ")
    birthdate = input("Введите Вашу дату рождения в формате YYYY-MM-DD: ")
    height = input("Введите свой рост в формате meters.centimeters (метры.сантиметры), например 1.88: ")
    # генерируем идентификатор пользователя и сохраняем его строковое представление
    # user_id = str(uuid.uuid4())
    # создаем нового пользователя
    user = User(
        first_name=first_name,
        last_name=last_name,
        email=email,
        gender=gender,
        birthdate=birthdate,
        height=height
    )
    # возвращаем созданного пользователя
    return user


def find(name, session):
    """
    Производит поиск атлета в таблице user по имени name
    """
    # находим все записи в таблице User, у которых поле User.first_name совпадает с параметром name
    query = session.query(User).filter(User.first_name == name)
    # считаем количество записей в таблице с помощью метода .count()
    users_cnt = query.count()
    # составляем список идентификаторов всех найденных пользователей
    user_ids = [user.id for user in query.all()]
    # возвращаем кортеж количество найденных пользователей, список идентификаторов
    return (users_cnt, user_ids)

def find_athlete_by_date(user_id, session):
    """
    Поиск атлета ближайшего по дате рождения к выбранному пользователю
    """
    # находим все записи в таблице User, у которых поле User.id совпадает с параметром user_id введенным пользователем
    query_user = session.query(User).filter(User.id == user_id)
    # Считываем колличество найденных записей
    users_cnt = query_user.count()

    # Если запись найдена ищем атлета, если нет выводим инфоримацию о том, что такого ползователя нет в базе
    if users_cnt == 1:
        # Получаем дату рождения введенного пользователя
        user_birth_date = [user.birthdate for user in query_user]

        # Находим все записи в таблице athelete
        query_athlete = session.query(Athelete)
        # Выбираем даты рождения всех атлетов
        athlete_birth_date = [athlete.birthdate for athlete in query_athlete.all()]

        # Переводим дату рождения пользователя в формат datetime
        u_year = 0
        u_month = 0
        u_day = 0

        for user_date in user_birth_date:
            # Разделяем дату рождения пользователя на список split user date вида ['YYYY', 'MM', 'DD']
            split_user_date = user_date.split("-")
            u_year = int(split_user_date[0])
            u_month = int(split_user_date[1])
            u_day = int(split_user_date[2])

        user_date_of_birth = datetime(u_year, u_month, u_day)
        print("\nДата рождения пользователя с ID = {}:".format(user_id),
              user_date_of_birth.strftime("%Y-%m-%d"))

        # Разделяем даты рождения атлетов и переводим в нужный формат
        athlete_date_of_birth = []

        for athlete_date in athlete_birth_date:
            split_athlete_date = athlete_date.split("-")
            a_year = int(split_athlete_date[0])
            a_month = int(split_athlete_date[1])
            a_day = int(split_athlete_date[2])

            athlete_date_of_birth.append(datetime(a_year, a_month, a_day))

        # Разница между датой рождения пользователя и атлетов
        difference = []
        for date in athlete_date_of_birth:
            dif = date - user_date_of_birth
            difference.append(int(dif.days))

        # Индекс минимальной разницы
        index_min_dif = difference.index(min(difference, key=abs)) + 1

        # Выводим информацию о найденном атлете
        for athlete in query_athlete:
            if athlete.id == index_min_dif:
                print("Атлет с ближайше датой рождения.\n"
                      "ID: {}\n"
                      "Имя: {}\n"
                      "Дата рождения: {}".format(athlete.id, athlete.name, athlete.birthdate))
                print("Разница между датами в днях: {}".format(abs(min(difference, key=abs))))

    else:
        print("Ближайший по дате рождения атлет не может быть найден, "
              "т.к. пользователя с введенным идентификатором нет в базе.")

def find_athlete_by_height(user_id, session):
    """
    Поиск атлета ближайшего по росту к выбранному пользователю
    """
    # находим все записи в таблице User, у которых поле User.id совпадает с параметром user_id введенным пользователем
    query_user = session.query(User).filter(User.id == user_id)
    # Подсчитываем колличество найденных записей
    users_cnt = query_user.count()

    # Если запись найдена ищем атлета, если нет выводим инфоримацию о том, что такого ползователя нет в базе
    if users_cnt == 1:
        # Получаем рост введенного пользователя
        user_height = [user.height for user in query_user]
        print("\nРост выбранного пользователя:", user_height[0])

        # Находим все записи в таблице athelete
        query_athlete = session.query(Athelete)
        # Выбираем параметры роста всех атлетов
        athlete_height = [athlete.height for athlete in query_athlete.all()]

        # Список для вычисленной разницы в росте атлета и пользователя
        difference = []
        # Спсиок id атлетов для которых вычислена разница в росте с пользователем
        dif_id_athletes = []
        # Счетчик для добавления id атлетов, у которых есть данные о росте, в список dif_id_athletes
        cnt = 0

        for height in athlete_height:
            # Если есть данные о росте атлета
            if height:
                # Заполняем список разниц в росте
                difference.append(abs(height - user_height[0]))
                # Заполняем список id
                dif_id_athletes.append(cnt)
            cnt += 1

        # Индекс id нужного атлета в списке dif_id_athletes
        idx_id = difference.index(min(difference, key=abs)) + 1

        for athlete in query_athlete:
            if athlete.id == dif_id_athletes[idx_id]:
                print("Атлет с ближайшим ростом.\n"
                      "ID: {}\n"
                      "Имя: {}\n"
                      "Рост: {}".format(athlete.id, athlete.name, athlete.height))
                print("Разница в росте - {} м".format(min(difference, key=abs)))

    else:
        print("Ближайший по росту атлет не может быть найден, "
              "так как пользователя с введенным идентификатором нет в базе.")


def print_users_list(cnt, user_ids):
    """
    Выводит на экран количество найденных пользователей и их идентификаторы
    Если передан пустой список идентификаторов, выводит сообщение о том, что пользователей не найдено.
    """
    # проверяем на пустоту список идентификаторов
    if user_ids:
        # если список не пуст, распечатываем количество найденных пользователей
        print("Найдено пользователей: ", cnt)
        print("Список идентификаторов найденных пользователей")
        # проходимся по каждому идентификатору
        for user_id in user_ids:
            # выводим на экран идентификатор — время_последней_активности
            print("ID: {}".format(user_id))
    else:
        # если список оказался пустым, выводим сообщение об этом
        print("Пользователей с таким именем нет.")


def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # просим пользователя выбрать режим
    mode = input("Выбери режим.\n1 - найти пользователя по имени\n2 - ввести данные нового пользователя\n"
                 "3 – найти двух атлетов: ближайшего по дате рождения к данному пользователю "
                 "и ближайшего по росту к данному пользователю\n")
    # проверяем режим
    if mode == "1":
        # выбран режим поиска, запускаем его
        name = input("Введи имя пользователя для поиска: ")
        # вызываем функцию поиска по имени
        users_cnt, user_ids = find(name, session)
        # вызываем функцию печати на экран результатов поиска
        print_users_list(users_cnt, user_ids)
    elif mode == "2":
        # запрашиваем данные пользоватлея
        user = request_data()
        # добавляем нового пользователя в сессию
        session.add(user)
        # сохраняем все изменения, накопленные в сессии
        session.commit()
        print("Спасибо, данные сохранены!")
    elif mode == "3":
        user_id = input("Введите идентификатор пользователя: ")
        find_athlete_by_date(user_id, session)
        find_athlete_by_height(user_id, session)
    else:
        print("Некорректный режим:(")


if __name__ == "__main__":
    main()