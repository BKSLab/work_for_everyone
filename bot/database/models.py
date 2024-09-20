from peewee import (
    AutoField,
    CharField,
    ForeignKeyField,
    Model,
    PostgresqlDatabase,
    TextField,
)


from config_data.config import load_config


config = load_config()


db_work_for_everyone = PostgresqlDatabase(
    database=config.db.name,
    host=config.db.host,
    user=config.db.user,
    password=config.db.password,
)


class BaseModel(Model):
    """Базовая модель для хранения данных о пользователях и регионах."""

    class Meta:
        database = db_work_for_everyone


class VacancyBaseModel(Model):
    """Базовая модель для хранения данных о вакансиях."""

    id = AutoField(primary_key=True)
    vacancy_name = TextField(help_text='Название вакансии (должности)')
    salary = TextField(help_text='Размер заработной платы')
    vacancy_source = CharField(help_text='Источник публикации вакансии')
    vacancy_url = TextField(help_text='url страницы вакансии')
    employer_name = TextField(help_text='Наименование работодателя')
    employer_location = TextField(help_text='Наименование населенного пункта')
    employer_phone_number = TextField(help_text='Номер телефона работодателя')
    company_code = TextField(help_text='id работодателя на сайте с вакансиями')
    vacancy_id = TextField(help_text='id вакансии на сайте с вакансиями')

    class Meta:
        database = db_work_for_everyone

    def __str__(self) -> str:
        return f'{self.vacancy_name} с id {self.vacancy_id}'


class Vacancy(VacancyBaseModel):
    """Модель для хранения данных вакансий."""

    applicant_tg_id = CharField(help_text='user id в Telegram')

    class Meta:
        table_name = 'vacancy'

    def __str__(self) -> str:
        return f'{self.vacancy_name} с id {self.vacancy_id}'


class VacancyMSK(VacancyBaseModel):
    """Модель для хранения данных вакансий в Москве."""

    class Meta:
        table_name = 'vacancy_msk'

    def __str__(self) -> str:
        return f'{self.vacancy_name} с id {self.vacancy_id}'


class VacancySPB(VacancyBaseModel):
    """Модель для хранения данных вакансий в Санкт-Петербурге."""

    class Meta:
        table_name = 'vacancy_spb'

    def __str__(self) -> str:
        return f'{self.vacancy_name} с id {self.vacancy_id}'


class Favorites(VacancyBaseModel):
    """Модель для хранения данных вакансий в избранном."""

    applicant_tg_id = CharField(help_text='user id в Telegram')

    class Meta:
        table_name = 'favorites'

    def __str__(self) -> str:
        return f'{self.vacancy_name} с id {self.vacancy_id}'


class Region(BaseModel):
    """Модель для хранения данных регионов."""

    id = AutoField(primary_key=True)
    region_name = CharField(unique=True, help_text='Наименование региона')
    region_code = CharField(
        unique=True, help_text='Код региона на сайте "Работа России"'
    )
    region_code_hh = CharField(help_text='Код региона на сайте hh.ru')
    federal_district_code = CharField(help_text='Номер федерального округа')

    def __str__(self) -> str:
        return (
            f'{self.region_name}. Код на сайте "Работа России":'
            f'{self.region_code}. Код на сайте hh.ru: {self.region_code_hh}'
        )


class Applicant(BaseModel):
    """Модель для сохранения данных пользователей."""

    id = AutoField(primary_key=True)
    name_applicant = CharField(help_text='имя соискателя')
    user_tg_id = CharField(help_text='user id в Telegram')
    region = ForeignKeyField(Region, backref='applicants')
    location = CharField(help_text='Наименование населенного пункта.')

    def __str__(self) -> str:
        return f'Пользователь {self.name_applicant} с ID: {self.user_tg_id}'
