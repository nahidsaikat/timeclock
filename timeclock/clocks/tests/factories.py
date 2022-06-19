from datetime import datetime, timedelta
import factory
import pytz as pytz
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from faker import Factory

from timeclock.clocks.models import UserClock

User = get_user_model()
faker = Factory.create()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'user%d' % n)
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    password = factory.Sequence(lambda n: 'password%d' % n)


class UserClockFactory(DjangoModelFactory):
    class Meta:
        model = UserClock

    user = factory.SubFactory(UserFactory)
    clocked_in = factory.LazyAttribute(lambda _: datetime.now(tz=pytz.utc)-timedelta(hours=5))
    clocked_out = factory.LazyAttribute(lambda _: datetime.now(tz=pytz.utc))
