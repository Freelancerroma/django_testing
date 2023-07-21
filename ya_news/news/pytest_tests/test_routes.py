from http import HTTPStatus

from django.urls import reverse

import pytest
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:home', None),
        ('news:detail', pytest.lazy_fixture('news_pk')),
        ('users:login', None),
        ('users:logout', None),
        ('users:signup', None),
    )
)
@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(client, name, args,):
    '''
    Анонимному пользователю доступны страницы:
    главная, отдельной новости, регистрация, вход и выход из учетной записи
    '''

    url = reverse(name, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:delete', pytest.lazy_fixture('comment_pk')),
        ('news:edit', pytest.lazy_fixture('comment_pk')),
    )
)
@pytest.mark.django_db
def test_redirects_for_anonymous_user(client, name, args,):
    '''
    Анонимный пользователь перенаправляется на страницу авторизации
    при переходе на страницы редактирования и удаления комментария
    '''

    login_url = reverse('users:login')
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


@pytest.mark.parametrize(
    'parametrized_client, expected_status',
    (
        (pytest.lazy_fixture('admin_client'), HTTPStatus.NOT_FOUND),
        (pytest.lazy_fixture('author_client'), HTTPStatus.OK),
    )
)
@pytest.mark.parametrize(
    'name',
    (
        ('news:delete'),
        ('news:edit'),
    )
)
def test_pages_availability_for_different_users(
    parametrized_client,
    expected_status,
    name,
    comment_pk,
):
    '''
    Авторизованный пользователь не может переходить
    на страницы удаления и изменения чужих комментариев.
    Автору доступны страницы удаления и редактирования комментария.
    '''

    url = reverse(name, args=comment_pk)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status
