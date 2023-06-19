from apscheduler.schedulers.background import BackgroundScheduler  # для удаления данных из БД через интервалы\
from crop.models import Data
import os
from cropbgsite.settings import MEDIA_ROOT


def delete_data_from_DB():
    '''
    функция очищает базу данных Data через определенные интервалы
    :return:
    '''
    def myfunc():
        # Удаление всех объектов из модели
        Data.objects.all().delete()

        # удаление файлов из папки user_files. получает путь к папке user_files
        def delete_folder_contents(folder_path):
            # Удаление всех файлов и папок внутри указанной папки (не удаляет саму папку)
            if len(os.listdir(folder_path)) > 0:
                for filename in os.listdir(folder_path):
                    file_path = os.path.join(folder_path, filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                    elif os.path.isdir(file_path):
                        delete_folder_contents(file_path)
                        os.rmdir(file_path)
            else:
                pass

        #передаем путь к нашему медиа руту user_files
        delete_folder_contents(MEDIA_ROOT)

        #принутем нам что все ок
        print("База данных очищена")

    #вызываем функцию фоновую
    scheduler = BackgroundScheduler()

    #добавляем задачу, указываем параметры, стартуем
    scheduler.add_job(myfunc, 'interval', hours=12) #minutes=<int>, seconds=<int>, hours=<int>
    scheduler.start()