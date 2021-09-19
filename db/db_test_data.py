from os import environ
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Configuration
DATABASE_USER = environ.get('DATABASE_USER')
if (DATABASE_USER is None):
    DATABASE_USER = "admin"
DATABASE_PASSWORD = environ.get('DATABASE_PASSWORD')
if (DATABASE_PASSWORD is None):
    DATABASE_PASSWORD = "admin"
DATABASE_DB = environ.get('DATABASE_DB')
if (DATABASE_DB is None):
    DATABASE_DB = "visualoffice"
DATABASE_HOST = environ.get('DATABASE_HOST')
if (DATABASE_HOST is None):
    DATABASE_HOST = "localhost"


class Manager(Base):

    __tablename__ = 'managers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    position = Column(String(80))
    age = Column(Integer)
    email = Column(String(40))
    n_subordinate = Column(Integer)
    users = relationship('User', backref='managers')


class User(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    position = Column(String(80))
    age = Column(Integer)
    email = Column(String(40))
    manager_id = Column(Integer, ForeignKey('managers.id'))


def main():
    
    engine = create_engine(f'postgresql+psycopg2://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_DB}')

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    ## Руководители
    # 1
    new_manager = Manager(name='Ответственнов Иван Антидедлайнович', 
                          position="Ведущий руководитель проектов", 
                          age=34, 
                          email = "IOtvetstvennov@example.com", 
                          n_subordinate=2)
    session.add(new_manager)
    # 2 
    new_manager = Manager(name='Хорошов Петр Всесделович', 
                          position="Старший руководитель проектов", 
                          age=32, 
                          email = "PHoroshov@example.com", 
                          n_subordinate=2)
    session.add(new_manager)
    # 3
    new_manager = Manager(name='Среднечков Аркадий Самокакнибудевич', 
                          position="Старший руководитель проектов", 
                          age=40, 
                          email = "ASrednechkov@example.com", 
                          n_subordinate=2)
    session.add(new_manager)
    # 4
    new_manager = Manager(name='Опоздаев Евгений Пробкадорогович', 
                          position="Младший руководитель проектов", 
                          age=26, 
                          email = "EOpozdaevv@example.com", 
                          n_subordinate=2)
    session.add(new_manager)

    ## Сотрудники
    # 1
    new_user = User(name='Трудягаев Олег Всесделавич', 
                    position="Младший инженер", 
                    age=23, 
                    email = "OTrudyagaev@example.com", 
                    manager_id=1)
    session.add(new_user)
    # 2
    new_user = User(name='Жизнь Валентин Занерзулович', 
                    position="Инженер", 
                    age=22, 
                    email = "VZhiznv@example.com", 
                    manager_id=1)
    session.add(new_user)
    # 3
    new_user = User(name='Секретарева Ольга Ожидайтеналинииевна', 
                    position="Младший инженер", 
                    age=25, 
                    email = "OSecretareva@example.com", 
                    manager_id=2)
    session.add(new_user)
    # 4
    new_user = User(name='Карантинов Владислав Безперчатникович', 
                    position="Младший инженер", 
                    age=21, 
                    email = "VKarantinov@example.com", 
                    manager_id=2)
    session.add(new_user)
    # 5
    new_user = User(name='Незнайкина Елена Самотакполучилосевна', 
                    position="Старший инженер", 
                    age=20, 
                    email = "ENeznaikina@example.com", 
                    manager_id=3)
    session.add(new_user)
    # 6
    new_user = User(name='Возможнов Александр Нужнопроверковнич', 
                    position="Старший инженер", 
                    age=30, 
                    email = "AVozmozhnov@example.com", 
                    manager_id=3)
    session.add(new_user)
    # 7
    new_user = User(name='Админов Илья Красноглазович', 
                    position="Ведущий инженер", 
                    age=29, 
                    email = "IAdminov@example.com", 
                    manager_id=4)
    session.add(new_user)
    # 8
    new_user = User(name='Эникеев Антон Перезагрузович', 
                    position="Старший инженер", 
                    age=19, 
                    email = "AEnikeev@example.com", 
                    manager_id=4)
    session.add(new_user)

    session.commit()
    print("Tables with data created")


if __name__ == "__main__":
    main()
