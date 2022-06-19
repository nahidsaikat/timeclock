from datetime import datetime, timedelta

import pytz
from graphql_jwt.testcases import JSONWebTokenTestCase

from .factories import UserFactory, UserClockFactory
from ..models import UserClock


class UsersTests(JSONWebTokenTestCase):

    def setUp(self):
        self.user = UserFactory.create()
        self.client.authenticate(self.user)

    def test_get_me(self):
        query = """
        query Me {
          me {
            username
            email
          }
        }
        """

        response = self.client.execute(query)

        self.assertEqual(response.data, {'me': {'username': self.user.username, 'email': self.user.email}})

    def test_check_in(self):
        query = """
        mutation ClockIn($clockdata: ClockInInput!) {
          clockIn(clockData: $clockdata) {
            clockedIn
          }
        }
        """

        variable = {
            "clockdata": {
                "clockedIn": "true"
            },
        }

        self.assertEqual(UserClock.objects.count(), 0)
        self.client.execute(query, variable)
        self.assertEqual(UserClock.objects.count(), 1)

    def test_check_out(self):
        UserClockFactory.create(user=self.user, clocked_out=None)
        query = """
        mutation ClockOut($clockOutdata: ClockOutInput!) {
          clockOut(clockOutData: $clockOutdata) {
            clockedOut
          }
        }
        """

        variable = {
            "clockOutdata": {
                "clockedOut": "true"
            }
        }

        self.client.execute(query, variable)
        self.assertIsNotNone(UserClock.objects.get().clocked_in)

    def test_get_current_clock(self):
        user_clock = UserClockFactory.create(user=self.user, clocked_out=None)
        query = """
        query CurrentClock {
          currentClock {
            clockedIn,
            clockedOut
          }
        }
        """

        response = self.client.execute(query)

        self.assertEqual(response.data.get('currentClock').get('clockedIn'), user_clock.clocked_in.isoformat())

    def test_get_clocked_hours(self):
        UserClockFactory.create(user=self.user)
        UserClockFactory.create(user=self.user, clocked_in=datetime.now(tz=pytz.utc)-timedelta(days=5)-timedelta(hours=5),
                                clocked_out=datetime.now(tz=pytz.utc)-timedelta(days=5))
        UserClockFactory.create(user=self.user, clocked_in=datetime.now(tz=pytz.utc)-timedelta(days=10)-timedelta(hours=5),
                                clocked_out=datetime.now(tz=pytz.utc)-timedelta(days=10))
        query = """
        query ClockedHour {
          clockedHours
        }
        """

        response = self.client.execute(query)

        self.assertEqual(response.data, {'clockedHours': {'today': 5, 'Current_week': 10, 'current_month': 15}})
