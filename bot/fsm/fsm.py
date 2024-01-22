from aiogram.fsm.state import State, StatesGroup


class ApplicantState(StatesGroup):
    federal_district_choice = State()
    region_name_choice = State()
    local_name_input = State()
    verification_data = State()
