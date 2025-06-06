# Эти ошибки нужны, чтобы обрабатывать ошибки алхимии и прокидывать кастомные в
# бизнес слой, так как он ничего не должен знать об алхимии


class UserAlreadyExistsError(Exception):
    """Исключение, которое выбрасывается, если пользователь с таким полисом уже существует"""


class DrugAlreadyExistsError(Exception):
    """Исключение, которое выбрасывается, если лекарство с таким полисом уже существует"""


class UserNotFoundError(Exception):
    """Исключение, которое вызывается, когда пользователь не найден"""


class DrugNotFoundError(Exception):
    """Исключение, которое вызывается, когда лекарство не найдено"""
