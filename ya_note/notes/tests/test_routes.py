from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор',)
        cls.reader = User.objects.create(username='Читатель',)
        cls.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=cls.author,
        )

    def test_pages_availability_for_anonymous(self):
        """
        Незарегистрированному пользователю доступны страницы:
        главная, регистрации, входа и выхода учетной записи
        """

        urls = (
            'notes:home',
            'users:login',
            'users:logout',
            'users:signup',
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_detail_availability_for_author(self):
        """
        Страницы отдельной заметки, удаления и редактирования заметки
        доступны только автору заметки.
        Если на эти страницы попытается зайти другой пользователь —
        вернётся ошибка 404.
        """

        users_statuses = (
            (self.author, HTTPStatus.OK),
            (self.reader, HTTPStatus.NOT_FOUND),
        )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in (
                'notes:edit',
                'notes:delete',
                'notes:detail',
            ):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.slug,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)

    def test_redirect_anonymous(self):
        """
        При попытке перейти на страницу
        списка заметок,
        страницу успешного добавления записи,
        страницу добавления заметки,
        отдельной заметки,
        редактирования или удаления заметки
        анонимный пользователь перенаправляется на страницу логина
        """

        login_url = reverse('users:login',)
        for name, args in (
            ('notes:add', None),
            ('notes:list', None),
            ('notes:success', None),
            ('notes:edit', (self.note.slug,)),
            ('notes:delete', (self.note.slug,)),
            ('notes:detail', (self.note.slug,)),
        ):
            with self.subTest(name=name):
                url = reverse(name, args=args)
                redirect_url = f'{login_url}?next={url}'
                response = self.client.get(url)
                self.assertRedirects(response, redirect_url)

    def test_add_success_availability(self):
        """
        Аутентифицированному пользователю доступна
        страница со списком заметок,
        страница успешного добавления заметки,
        страница добавления новой заметки
        """

        user = self.author
        self.client.force_login(user)
        for name in (
            'notes:add',
            'notes:list',
            'notes:success',
        ):
            with self.subTest(name=name):
                url = reverse(name)
                responce = self.client.get(url)
                self.assertEqual(responce.status_code, HTTPStatus.OK)
