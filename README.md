## Проект «Django testing»  
***
### Описание:
Проект «Django testing» предназначен для написания тестов на Unitets и Pytest для готовых проектов ya_note и ya_news.
***
### Системные требования:
Python 3.9 или выше.
***
### Установка:

1. Склонируйте репозиторий по ссылке:
```
git clone git@github.com:Freelancerroma/django_testing.git
```
2. Установите и активируйте виртуальное окружение:
```
python -m venv venv
```
```
source venv/Scripts/activate
```
3. Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
4. Перейдите в директории ya_news и ya_note и выполните миграции:
```
python manage.py makemigrations
```
```
python manage.py migrate
```
5. Запустите скрипт для `run_tests.sh` из корневой директории проекта:
```
bash run_tests.sh
```
***
### Инструменты и стек:
- Python
- HTML
- CSS
- Django
- Bootstrap
- Unittest
- Pytest
