from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.utils import timezone
from news.models import Comment, News


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def author_client(author, client):
    client.force_login(author)
    return client


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Текст'
    )
    return news


@pytest.fixture
def news_pk(news):
    return news.pk,


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Текст Комментария'
    )
    return comment


@pytest.fixture
def comment_pk(comment):
    return comment.pk,


@pytest.fixture
def news_list():
    news_list = News.objects.bulk_create(
        News(
            title=f'Заголовок {i}',
            text=f'Текст {i}',
            date=datetime.today() - timedelta(days=i),
        )
        for i in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )
    return news_list


@pytest.fixture
def comment_list(news, author):
    for i in range(3):
        comment = Comment.objects.create(
            author=author,
            news=news,
            text=f'Текст комментария {i}',
        )
        comment.created = timezone.now() + timedelta(days=i)
        comment.save()
    return comment_list


@pytest.fixture
def form_data():
    return {'text': 'Новый текст комментария', }
