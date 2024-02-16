from peewee import (
    CharField,
    ForeignKeyField,
    IntegerField,
    Model,
    SmallIntegerField,
    SqliteDatabase,
)

db_work_for_everyone = SqliteDatabase('db_for_dev.db')


class Region(Model):
    """Модель для хранения данных регионов."""

    id = IntegerField(primary_key=True)
    region_name = CharField(unique=True, help_text='Название региона')
    region_code = SmallIntegerField(unique=True, help_text='Код региона')
    federal_district_code = SmallIntegerField(
        help_text='Номер федерального округа'
    )

    class Meta:
        database = db_work_for_everyone

    def __str__(self) -> str:
        return f'{self.region_name} с кодом {self.region_code}'


class Applicant(Model):
    """Модель для сохранения данных пользователей."""

    id = IntegerField(primary_key=True)
    name_applicant = CharField(help_text='имя соискателя')
    user_tg_id = IntegerField(help_text='user id в Telegram')
    region = ForeignKeyField(Region, backref='applicants')
    location = CharField(help_text='Наименование населенного пункта.')

    class Meta:
        database = db_work_for_everyone

    def __str__(self) -> str:
        return f'Пользователь {self.name_applicant} с ID: {self.user_tg_id}'


class Vacancy(Model):
    """Модель для хранения данных вакансий."""

    id = IntegerField(primary_key=True)
    applicant_tg_id = IntegerField(help_text='user id в Telegram')
    vacancy_name = CharField()
    social_protected = CharField()
    salary = CharField()
    employer_name = CharField()
    employer_location = CharField()
    employer_email = CharField()
    employer_phone_number = CharField()
    company_code = CharField()
    vacancy_id = CharField()

    class Meta:
        database = db_work_for_everyone

    def __str__(self) -> str:
        return f'{self.vacancy_name} с {self.vacancy_id}'


class Favorites(Model):
    """Модель для хранения данных вакансий в избранном."""

    id = IntegerField(primary_key=True)
    applicant_tg_id = IntegerField(help_text='user id в Telegram')
    vacancy_name = CharField()
    salary = CharField()
    employer_name = CharField()
    employer_location = CharField()
    employer_email = CharField()
    employer_phone_number = CharField()
    company_code = CharField()
    vacancy_id = CharField()

    class Meta:
        database = db_work_for_everyone

    def __str__(self) -> str:
        return f'{self.applicant_tg_id} с {self.vacancy_name}'
