from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.reader = User.objects.create(username='Читатель')
        cls.author = User.objects.create(username='Автор')
        cls.note = Note.objects.create(
            title='Заголовок заметки',
            text='Текст заметки',
            slug='Slug',
            author=cls.author,
        )

    def test_notes_list_for_different_users(self):
        '''
        Отдельная заметка передаётся на страницу со списком заметок
        в списке object_list в словаре context.
        В список заметок одного пользователя
        не попадают заметки другого пользователя.
        '''
        users = (
            (self.author, True),
            (self.reader, False),
        )
        url = reverse('notes:list',)
        for user, value in users:
            self.client.force_login(user)
            with self.subTest(user=user.username, value=value):
                response = self.client.get(url)
                object_list = response.context['object_list']
                self.assertEqual(self.note in object_list, value)

    def test_authorized_client_has_form(self):
        '''На страницы создания и редактирования заметки передаются формы'''
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for page, args in urls:
            self.client.force_login(self.author)
            with self.subTest(page=page):
                url = reverse(page, args=args)
                response = self.client.get(url)
                self.assertIn('form', response.context)
