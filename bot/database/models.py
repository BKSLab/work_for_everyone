from peewee import (
    CharField,
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
        return self.region_name
