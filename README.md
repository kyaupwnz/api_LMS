Для запуска проекта:
1. Установите Docker
2. Скачайте проект из репозитория
3. Запустите постгрес: sudo docker run --name db_django -p 5432:5432 -e POSTGRES_PASSWORD=12345 -e POSTGRES_DB=test -e POSTGRES_HOST_AUTH_METHOD=md5 -p 5432:5432 -v /home/kyaupwnz/pg_data:/var/lib/postgresql/data postgres
4. Запустите пайтон: sudo docker run -it --network host -v /home/kyaupwnz/PycharmProjects/drf_domashka_1:/drf_domashka_1 python bash
5. Перейдите в папку проекта
6. Активируйте виртуальное  окружение: source env/bin/activate
7. Установите зависимости: pip install -r requirements.txt
8. Выполните миграции: python3 manage.py migrate
9. Запустите сервер: python3 manage.py runserver
