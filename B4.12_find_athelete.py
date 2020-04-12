# испортируем модули стандартнй библиотеки uuid и datetime
import uuid
import datetime

# импортируем библиотеку sqlalchemy и некоторые функции из нее 
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# константа, указывающая способ соединения с базой данных
DB_PATH = "sqlite:///sochi_athletes.sqlite3"
# базовый класс моделей таблиц
Base = declarative_base()


class NewUser(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__ = 'newusers'

    # идентификатор пользователя, первичный ключ
    id = sa.Column(sa.String(36), primary_key=True)
    # имя пользователя
    first_name = sa.Column(sa.Text)
    # фамилия пользователя
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    # адрес электронной почты пользователя
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)


class Atheletes(Base):
    """
    Описывает структуру таблицу log для хранения времени последней активности пользователя
    """
    # задаем название таблицы
    __tablename__ = 'athelete'

    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate= sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Integer)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
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
    gender = input("Ваш пол:")
    email = input("Мне еще понадобится адрес твоей электронной почты: ")
    birthdate = input("Дата рождения:")
    height = input("Рост:")
    # генерируем идентификатор пользователя и сохраняем его строковое представление
    user_id = str(uuid.uuid4())
    # создаем нового пользователя
    user = NewUser(
        id=user_id,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        email=email,
        birthdate=birthdate,
        height=height
    )
    # возвращаем созданного пользователя
    return user


def find(name, session):
    """
    Производит поиск пользователя в таблице user по заданному name
    """
    # находим все записи в таблице User, у которых поле User.id совпадает с парарметром name
    print("Ищем данные пользователя", name)
    person = session.query(NewUser).filter(NewUser.first_name == name).first()
    person_birthdate = datetime.date(*map(int, person.birthdate.split("-")))
    print("Дата рождения", name,":", person_birthdate)
    person_heigh = person.height
    print("Рост", name,":",person_heigh)


    atheletes_list = session.query(Atheletes).filter(Atheletes.birthdate >= person_birthdate).order_by(Atheletes.birthdate).first()

    print("Похожий по дате рождения атлет:", atheletes_list.name, "Дата рождения:",atheletes_list.birthdate, )

    atheletes_dic= session.query(Atheletes).filter(Atheletes.height >= person_heigh).order_by(Atheletes.height)
    founded_athelete_by_bd = {}
    i=0
    for rows in atheletes_dic:
        if i<2:
            founded_athelete_by_bd[rows.name]=rows.height
            i += 1
        else:
            break
    print("Похожие по росту атлеты:",founded_athelete_by_bd)

    
    return()



def main():
    """
    Осуществляет взаимодействие с пользователем, обрабатывает пользовательский ввод
    """
    session = connect_db()
    # просим пользователя выбрать режим
    print("Подберем похожих атлетов")
    # выбран режим поиска, запускаем его
    name = input("Введи имя пользователя: ")
    # name="Наст"
    # вызываем функцию поиска по имени
    find(name, session)
    # вызываем функцию печати на экран результатов поиска
    # print_users_list(person_birthdate, person_heigh)
    

if __name__ == "__main__":
    main()