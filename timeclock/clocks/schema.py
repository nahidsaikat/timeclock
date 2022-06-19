import datetime
import graphene
import pytz
from graphene.types.generic import GenericScalar
from distutils.util import strtobool
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required

from timeclock.clocks.models import UserClock


class ClockType(DjangoObjectType):
    class Meta:
        model = UserClock
        fields = ("id", "user", "clocked_in", "clocked_out")


class ClockInInput(graphene.InputObjectType):
    id = graphene.ID()
    clocked_in = graphene.String(required=True)


class CreateClockIn(graphene.Mutation):
    class Arguments:
        clock_data = ClockInInput(required=True)

    clocked_in = graphene.DateTime()

    @staticmethod
    @login_required
    def mutate(root, info, clock_data):
        if not bool(strtobool(clock_data.clocked_in)):
            raise Exception("Invalid value for clocked_in")
        if UserClock.objects.filter(user=info.context.user, clocked_out__isnull=True).exists():
            raise Exception("You already have a running clock")

        clock = UserClock(
            user=info.context.user,
            clocked_in=datetime.datetime.now(tz=pytz.utc)
        )
        clock.save()
        return CreateClockIn(clock.clocked_in)


class ClockOutInput(graphene.InputObjectType):
    id = graphene.ID()
    clocked_out = graphene.String(required=True)


class CreateClockOut(graphene.Mutation):
    class Arguments:
        clock_out_data = ClockOutInput(required=True)

    clocked_out = graphene.DateTime()

    @staticmethod
    @login_required
    def mutate(root, info, clock_out_data):
        if not bool(strtobool(clock_out_data.clocked_out)):
            raise Exception("Invalid value for clocked_out")

        queryset = UserClock.objects.filter(user=info.context.user, clocked_out__isnull=True)
        if not queryset.exists():
            raise Exception("You have already clocked out")

        clock = queryset.get()
        clock.clocked_out = datetime.datetime.now(tz=pytz.utc)
        clock.save()

        return CreateClockOut(clock.clocked_out)


class ClockedHourType(graphene.ObjectType):
    today = graphene.Int()
    current_week = graphene.Int()
    current_month = graphene.Int()


class Query(graphene.ObjectType):
    current_clock = graphene.Field(ClockType)
    clocked_hours = GenericScalar()

    @staticmethod
    @login_required
    def resolve_current_clock(root, info):
        user = info.context.user
        clock = UserClock.objects.filter(user=user, clocked_out__isnull=True)
        return clock.first()

    @staticmethod
    @login_required
    def resolve_clocked_hours(root, info):
        user = info.context.user
        today = 0
        for clock in UserClock.objects.filter(user=user, clocked_in__date=datetime.date.today()):
            td = clock.clocked_out - clock.clocked_in
            today += (td.seconds // 3600)

        week = 0
        last_seven = datetime.datetime.today() - datetime.timedelta(days=7)
        for clock in UserClock.objects.filter(user=user, clocked_in__date__gte=last_seven):
            td = clock.clocked_out - clock.clocked_in
            week += (td.seconds // 3600)

        month = 0
        last_thirty = datetime.datetime.today() - datetime.timedelta(days=30)
        for clock in UserClock.objects.filter(user=user, clocked_in__date__gte=last_thirty):
            td = clock.clocked_out - clock.clocked_in
            month += (td.seconds // 3600)

        return {
            "today": today,
            "Current_week": week,
            "current_month": month
        }


class Mutation(graphene.ObjectType):
    clock_in = CreateClockIn.Field()
    clock_out = CreateClockOut.Field()
