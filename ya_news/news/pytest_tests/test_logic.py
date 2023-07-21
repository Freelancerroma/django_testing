from http import HTTPStatus

from django.urls import reverse

import pytest
from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from pytest_django.asserts import assertFormError, assertRedirects

pytestmark = pytest.mark.django_db


def test_anonymous_user_cant_create_comment(client, news_pk, form_data,):
    '''Анонимный пользователь не может отправить комментарий'''

    url = reverse('news:detail', args=news_pk)
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 0


def test_autorized_user_can_create_comment(
    author_client,
    author,
    form_data,
    news,
):
    '''Авторизованный пользователь может отправить комментарий'''

    url = reverse('news:detail', args=[news.pk])
    response = author_client.post(url, data=form_data)
    expected_url = f'{url}#comments'
    assertRedirects(response, expected_url)
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.get()
    assert new_comment.text == form_data['text']
    assert new_comment.author == author
    assert new_comment.news == news


@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_user_cant_use_bad_words(bad_word, author_client, news_pk,):
    '''Нельзя использовать запрещенные слова в комментарии'''

    comments_count = Comment.objects.count()
    bad_words_data = {'text': f'Какой-то текст, {bad_word}, еще текст'}
    url = reverse('news:detail', args=news_pk)
    response = author_client.post(url, data=bad_words_data)
    expected_count = 0
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert comments_count == expected_count


def test_author_can_delete_comment(author_client, comment_pk, news_pk,):
    '''Автор может удалять свои комментарии'''

    url = reverse('news:delete', args=comment_pk)
    response = author_client.post(url)
    news_detail_url = reverse('news:detail', args=news_pk)
    expected_url = f'{news_detail_url}#comments'
    assertRedirects(response, expected_url)
    comments_count = Comment.objects.count()
    expected_count = 0
    assert comments_count == expected_count


def test_author_can_edit_comment(
    author_client,
    comment_pk,
    comment,
    news_pk,
    form_data,
):
    '''Автор может изменять свои комментарии'''

    url = reverse('news:edit', args=comment_pk)
    response = author_client.post(url, data=form_data)
    news_detail_url = reverse('news:detail', args=news_pk)
    expected_url = f'{news_detail_url}#comments'
    assertRedirects(response, expected_url)
    comment.refresh_from_db()
    comments_count = Comment.objects.count()
    expected_count = 1
    assert comments_count == expected_count
    assert comment.text == form_data['text']


def test_user_cant_edit_comment_of_another_user(
    admin_client,
    comment_pk,
    comment,
    form_data,
):
    '''Авторизированный пользователь не может изменять чужие комментарии'''

    url = reverse('news:edit', args=comment_pk)
    comment_old_text = comment.text
    response = admin_client.post(url, data=form_data)
    comment.refresh_from_db()
    comments_count = Comment.objects.count()
    expected_count = 1
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comments_count == expected_count
    assert comment.text == comment_old_text


def test_user_cant_delete_comment_of_another_user(admin_client, comment_pk,):
    '''Авторизированный пользователь не может удалять чужие комментарии'''

    url = reverse('news:delete', args=comment_pk)
    response = admin_client.post(url)
    comments_count = Comment.objects.count()
    expected_count = 1
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comments_count == expected_count
