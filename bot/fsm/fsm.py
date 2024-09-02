from aiogram.fsm.state import State, StatesGroup


class ApplicantState(StatesGroup):
    """
    Определение состояний пользователя при взаимодействии с ботом.
    """

    federal_district_choice = State()
    region_name_choice = State()
    local_name_input = State()
    verification_data = State()
    show_vacancies_mode = State()
    show_vacancies_msk_spb_mode = State()
