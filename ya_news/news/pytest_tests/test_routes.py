from http import HTTPStatus

import pytest
from django.urls import reverse
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
def test_pages_availability_for_anonymous_user(client, name, args):
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
def test_pages_availability_for_auth_user(author_client, name, args):
    url = reverse(name, args=args)
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:delete', pytest.lazy_fixture('comment_pk')),
        ('news:edit', pytest.lazy_fixture('comment_pk')),
    )
)
@pytest.mark.django_db
def test_redirects_for_anonymous_user(client, name, args):
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
    comment_pk
):
    url = reverse(name, args=comment_pk)
    response = parametrized_client.get(url)
    assert response.status_code == expected_status
