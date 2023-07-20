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

    def test_user_self_notes_list(self):
        user = self.author
        self.client.force_login(user)
        url = reverse('notes:list',)
        response = self.client.get(url)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_another_user_self_notes_list(self):
        user = self.reader
        self.client.force_login(user)
        url = reverse('notes:list',)
        response = self.client.get(url)
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_authorized_client_has_form_for_add(self):
        user = self.author
        self.client.force_login(user)
        url = reverse('notes:add', None)
        response = self.client.get(url)
        self.assertIn('form', response.context)

    def test_authorized_client_has_form_for_edit(self):
        user = self.author
        self.client.force_login(user)
        url = reverse('notes:edit', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertIn('form', response.context)
