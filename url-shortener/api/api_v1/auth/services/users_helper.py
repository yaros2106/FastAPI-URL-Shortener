from abc import ABC, abstractmethod


class AbstractUsersHelper(ABC):
    """
    Что нужно от обертки:
    - получение пароля по username
    - совпадает ли пароль с переданным username
    - проверка существования пользователя
    """

    @abstractmethod
    def get_user_password(
        self,
        username: str,
    ) -> str | None:
        """
        По переданному username находим пароль
        и возвращаем если есть

        :param username: - имя пользователя
        :return: пароль по пользователю, если найден
        """

    @classmethod
    def check_passwords_match(
        cls,
        password1: str,
        password2: str,
    ) -> bool:
        """
        Проверка паролей на совпадение
        """
        return password1 == password2

    def validate_user_password(
        self,
        username: str,
        password: str,
    ) -> bool:
        """
        Проверить, валиден ли пароль

        :param username: - чей пароль проверить
        :param password: - переданный пароль, сверить с тем, что в БД
        :return: True если совпадает, иначе False
        """

        db_password = self.get_user_password(username)
        if db_password is None:
            return False
        return self.check_passwords_match(
            password1=db_password,
            password2=password,
        )

    @abstractmethod
    def user_exists(
        self,
        username: str,
    ) -> bool:
        """
        Проверяет, существует ли пользователь в БД.
        :param username: имя пользователя
        :return: True если пользователь есть, иначе False
        """
