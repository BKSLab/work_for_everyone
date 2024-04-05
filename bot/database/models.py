from environs import Env
from peewee import (
    AutoField,
    BigIntegerField,
    CharField,
    ForeignKeyField,
    Model,
    PostgresqlDatabase,
    SmallIntegerField,
    TextField,
)

env = Env()
env.read_env()

db_work_for_everyone = PostgresqlDatabase(
    database=env('DB_NAME'),
    host=env('DB_HOST'),
    user=env('POSTGRES_USER'),
    password=env('POSTGRES_PASSWORD'),
)


class BaseModel(Model):
    """Базовый клас определяющий БД."""

    class Meta:
        database = db_work_for_everyone


class Region(BaseModel):
    """Модель для хранения данных регионов."""

    id = AutoField(primary_key=True)
    region_name = CharField(unique=True, help_text='Название региона')
    region_code = SmallIntegerField(unique=True, help_text='Код региона')
    federal_district_code = SmallIntegerField(
        help_text='Номер федерального округа'
    )

    def __str__(self) -> str:
        return f'{self.region_name} с кодом {self.region_code}'


class Applicant(BaseModel):
    """Модель для сохранения данных пользователей."""

    id = AutoField(primary_key=True)
    name_applicant = CharField(help_text='имя соискателя')
    user_tg_id = BigIntegerField(help_text='user id в Telegram')
    region = ForeignKeyField(Region, backref='applicants')
    location = CharField(help_text='Наименование населенного пункта.')

    def __str__(self) -> str:
        return f'Пользователь {self.name_applicant} с ID: {self.user_tg_id}'


class Vacancy(BaseModel):
    """Модель для хранения данных вакансий."""

    id = AutoField(primary_key=True)
    applicant_tg_id = BigIntegerField(help_text='user id в Telegram')
    vacancy_name = CharField()
    social_protected = TextField()
    salary = CharField()
    employer_name = CharField()
    employer_location = TextField()
    employer_email = CharField()
    employer_phone_number = CharField()
    company_code = CharField()
    vacancy_id = CharField()

    def __str__(self) -> str:
        return f'{self.vacancy_name} с {self.vacancy_id}'


class Favorites(BaseModel):
    """Модель для хранения данных вакансий в избранном."""

    id = AutoField(primary_key=True)
    applicant_tg_id = BigIntegerField(help_text='user id в Telegram')
    vacancy_name = CharField()
    salary = CharField()
    employer_name = CharField()
    employer_location = TextField()
    employer_email = CharField()
    employer_phone_number = CharField()
    company_code = CharField()
    vacancy_id = CharField()

    def __str__(self) -> str:
        return f'{self.applicant_tg_id} с {self.vacancy_name}'
