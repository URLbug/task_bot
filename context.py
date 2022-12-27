from aiogram.dispatcher.filters.state import State, StatesGroup


class Orders(StatesGroup):

    GPS = State()
    contacts = State()

class Order_Redacts_GPS(StatesGroup):

    GPS = State()

class Order_Redacts_Contacts(StatesGroup):

    contacts = State()

class Order_Redacts_Sums_And_Baskets(StatesGroup):

    sums_and_baskets_sums = State()

class Order_Delete(StatesGroup):

    delete = State()