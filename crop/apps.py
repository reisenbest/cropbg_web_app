from django.apps import AppConfig

class CropConfig(AppConfig):
    # Класс CropConfig представляет конфигурацию для приложения "crop" в Django.

    default_auto_field = 'django.db.models.BigAutoField'
    # Поле default_auto_field определяет тип автоинкрементного поля, используемого для моделей в приложении.
    # Здесь указано, что будет использоваться BigAutoField, который поддерживает автоинкрементные значения большого размера.

    name = 'crop'
    # Поле name указывает имя приложения. Здесь указано имя "crop", которое соответствует имени директории вашего приложения.







