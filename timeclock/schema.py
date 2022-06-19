import graphene

import timeclock.clocks.schema
import timeclock.auth.schema


class Query(
    timeclock.auth.schema.Query,
    timeclock.clocks.schema.Query,
    graphene.ObjectType
):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


class Mutation(
    timeclock.auth.schema.Mutation,
    timeclock.clocks.schema.Mutation,
    graphene.ObjectType
):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
