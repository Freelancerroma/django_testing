from datetime import date

import pytest
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures('news_list')
def test_news_count(client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = list(response.context['object_list'])
    assert len(object_list) == settings.NEWS_COUNT_ON_HOME_PAGE


@pytest.mark.usefixtures('news_list')
def test_news_sort(client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = list(response.context['object_list'])
    assert isinstance(object_list[0].date, date)
    assert object_list == sorted(
        object_list,
        key=lambda x: x.date,
        reverse=True,
    )


@pytest.mark.usefixtures('comment_list')
def test_comment_sort(client, news_pk):
    url = reverse('news:detail', args=news_pk)
    response = client.get(url)
    news = response.context['news']
    comments_list = list(news.comment_set.all())
    assert isinstance(comments_list[0].created, timezone.datetime)
    assert comments_list == sorted(
        comments_list,
        key=lambda x: x.created,
    )


@pytest.mark.parametrize(
    'user, expected_form',
    (
        (pytest.lazy_fixture('admin_client'), True),
        (pytest.lazy_fixture('client'), False),
    )
)
def test_client_has_form(user, expected_form, news_pk):
    url = reverse('news:detail', args=news_pk)
    response = user.get(url)
    assert ('form' in response.context) == expected_form
