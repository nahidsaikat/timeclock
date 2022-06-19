import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphene_django import DjangoObjectType
from graphql_jwt.decorators import login_required


User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ["email", "username", "password"]


class ViewUserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ["email", "username"]


class UserInput(graphene.InputObjectType):
    id = graphene.ID()
    email = graphene.String(required=True)
    username = graphene.String(required=True)
    password = graphene.String(required=True)


class CreateUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, user_data=None):
        user = User(
            email=user_data.email,
            username=user_data.username,
            password=user_data.password,
        )
        user.save()
        return CreateUser(user=user)


class Query(graphene.ObjectType):
    me = graphene.Field(ViewUserType)

    @staticmethod
    @login_required
    def resolve_me(root, info):
        user = info.context.user
        return user


class Mutation(graphene.ObjectType):
    obtain_token = graphql_jwt.ObtainJSONWebToken.Field()
    # refresh_token = graphql_jwt.Refresh.Field()
    # verify_token = graphql_jwt.Verify.Field()
    create_user = CreateUser.Field()
