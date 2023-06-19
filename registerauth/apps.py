from django.apps import AppConfig


class RegisterauthConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Поле default_auto_field определяет тип автоинкрементного поля, используемого для моделей в приложении.
    # Здесь указано, что будет использоваться BigAutoField, который поддерживает автоинкрементные значения большого размера

    name = 'registerauth'
    # Поле name указывает имя приложения. Здесь указано имя "registerauth", которое соответствует имени директории вашего приложения.