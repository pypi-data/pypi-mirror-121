import abc
import inspect
import logging
from typing import Dict, Union, Callable

import graphene
import graphene_django

from django_koldar_utils.graphql_toolsbox import graphql_decorators
from django_koldar_utils.graphql_toolsbox.generator.contexts import GraphQLBuildtimeContext, GraphQLRuntimeContext
from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneInputType, TGrapheneType, TDjangoModelType, \
    TGrapheneQuery, TGrapheneArgument, TGrapheneWholeQueryReturnType


LOG = logging.getLogger(__name__)


class IGraphQLEndpointGenerator(abc.ABC):
    """
    Generate a mutation/query endpoint
    """

    @abc.abstractmethod
    def _generate_action_class_name(self, build_context: GraphQLBuildtimeContext):
        """
        :return: name of the class representing this action
        """
        pass

    def generate(self, django_type: TDjangoModelType, graphene_type: TGrapheneType, graphene_input_type: TGrapheneInputType) -> TGrapheneQuery:
        pass

    @abc.abstractmethod
    def _generate_action_description(self, build_context: GraphQLBuildtimeContext) -> str:
        """
        :return: __doc__ of the class representing this action
        """
        pass

    @abc.abstractmethod
    def _generate_action_arguments(self, build_context: GraphQLBuildtimeContext) -> Dict[str, TGrapheneArgument]:
        """
        :return: list of parameters the class to generate will have. These are the graphql parameter
        """
        pass

    @abc.abstractmethod
    def _generate_action_return_type(self, build_context: GraphQLBuildtimeContext) -> TGrapheneWholeQueryReturnType:
        """
        :return: list of parameters the class to generate will have. These are the graphql parameter
        """
        pass

    @abc.abstractmethod
    def graphql_body_function(self, runtime_context: GraphQLRuntimeContext, *args, **kwargs) -> TGrapheneWholeQueryReturnType:
        pass

    @abc.abstractmethod
    def _compute_graphene_class(self, build_context: GraphQLBuildtimeContext) -> type:
        """
        Function used to generate a class that represents a graphene query
        """
        pass

    def generate(self, django_type: TDjangoModelType, graphene_type: TGrapheneType, graphene_input_type: TGrapheneInputType, **kwargs) -> TGrapheneQuery:
        """
        Allows you to create a graphql endpoint in a easy manner

        :param django_type: type of a model involved in the generation of the graphql action
        :param django_type: type invovled in the generation of the graphql action
        :return: a class representing a callable from graphql
        """
        # @graphql_subquery
        # class Query(graphene_toolbox.ObjectType):
        #     question = graphene_toolbox.Field(
        #         QuestionType,
        #         foo=graphene_toolbox.String(),
        #         bar=graphene_toolbox.Int()
        #     )
        #
        #     def resolve_question(root, info, foo, bar):
        #         # If `foo` or `bar` are declared in the GraphQL query they will be here, else None.
        #         return Question.objects.filter(foo=foo, bar=bar).first()

        build_context = GraphQLBuildtimeContext(
            django_type=django_type,
            graphene_type=graphene_type,
            graphene_input_type=graphene_input_type,
            params=kwargs
        )

        build_context.action_arguments = self._generate_action_arguments(build_context)
        build_context.action_return_type = self._generate_action_return_type(build_context)
        build_context.action_class_name = self._generate_action_class_name(build_context)
        build_context.action_description = self._generate_action_description(build_context)

        assert build_context.action_class_name is not None, "Query class name is None"
        assert all(map(lambda x: x is not None, build_context.action_arguments.keys())), f"Some arguments of {build_context.action_class_name} are None"
        assert build_context.action_return_type is not None, f"return type of {build_context.action_class_name} is None"
        assert build_context.action_description is not None, f"description of {build_context.action_class_name} is None"
        assert (not inspect.isclass(build_context.action_return_type)) or (issubclass(build_context.action_return_type, (graphene.Scalar, graphene.ObjectType, graphene_django.DjangoObjectType))), \
            f"return type \"{build_context.action_return_type}\" of \"{build_context.action_class_name}\" cannot be a type subclass graphene_toolbox.Field, but needs to be a plain ObjectType!"
        assert ((inspect.isclass(build_context.action_return_type)) or (isinstance(build_context.action_return_type, (graphene.List, graphene.Field)))), \
            f"return type \"{build_context.action_return_type}\" of \"{build_context.action_class_name}\" cannot be an instanc deriving graphene_toolbox.Field, but needs to be a plain ObjectType!"

        def perform_query(root, info, *args, **kwargs) -> any:
            nonlocal build_context
            if root is None:
                root = build_context.get_data("query_class")

            runtime_context = GraphQLRuntimeContext(build_context, root, info, *args, **kwargs)
            LOG.info(f"Computing result for graphql query {build_context.action_class_name}...")
            result = self.graphql_body_function(runtime_context, *args, **kwargs)
            return result

        build_context.action_body = perform_query

        result_class = self._compute_graphene_class(build_context)
        return result_class


class AbstractGraphQLMutationGenerator(IGraphQLEndpointGenerator, abc.ABC):
    """
    Generate a query via graphene and automatically registers it with graphql_subquery decorator
    """

    def _compute_graphene_class(self, build_context: GraphQLBuildtimeContext) -> type:
        assert build_context.action_class_name is not None, "mutation class name is none"
        assert all(map(lambda x: x is not None, build_context.action_arguments.keys())), f"argument of {build_context.action_class_name} are none"
        assert build_context.action_return_type is not None, "return type is None. This should not be possible"
        assert "mutate" not in build_context.action_return_type.keys(), f"mutate in return type of class {build_context.action_class_name}"
        assert all(
            map(lambda x: x is not None, build_context.action_return_type.keys())), f"some return value of {build_context.action_class_name} are None"
        assert build_context.action_description is not None, f"description of {build_context.action_class_name} is None"
        assert isinstance(build_context.action_arguments, dict), f"argument is not a dictionary"
        assert isinstance(list(build_context.action_arguments.keys())[0], str), f"argument keys are not strings!"

        mutation_class_meta = type(
            "Arguments",
            (object,),
            build_context.action_arguments
        )

        def mutate(root, info, *args, **kwargs) -> any:
            nonlocal build_context
            if root is None:
                root = mutation_class
            runtime_context = GraphQLRuntimeContext(build_context, root, info, *args, **kwargs)
            LOG.info(f"Computing result for graphql mutation {build_context.action_class_name}...")
            result = self.graphql_body_function(runtime_context, *args, **kwargs)
            return result

        build_context.action_body = mutate

        LOG.info(f"Argument are {build_context.action_arguments}")
        LOG.info(f"Creating mutation={build_context.action_class_name}; arguments keys={','.join(build_context.action_arguments.keys())}; return={', '.join(build_context.action_return_type.keys())}")
        mutation_class = type(
            build_context.action_class_name,
            (graphene.Mutation,),
            {
                "Arguments": mutation_class_meta,
                "__doc__": build_context.action_description,
                **build_context.action_return_type,
                "mutate": mutate
            }
        )
        # Apply decorator to auto detect mutations
        mutation_class = graphql_decorators.graphql_submutation(mutation_class)

        return mutation_class


class AbstractGraphQLQueryGenerator(IGraphQLEndpointGenerator, abc.ABC):
    """
    Generate a query via graphene and automatically registers it with graphql_subquery decorator
    """

    def _compute_graphene_class(self, build_context: GraphQLBuildtimeContext) -> type:
        if isinstance(build_context.action_return_type, graphene.Field):
            # needed otherwise graphene_toolbox.schema will raise an exception
            build_context.action_return_type = build_context.action_return_type.type

        assert build_context.is_param_present("output_name")

        output_name = build_context.get_param("output_name")
        query_class = type(
            build_context.action_class_name,
            (graphene.ObjectType, ),
            {
                "__doc__": build_context.action_description,
                f"resolve_{output_name}": build_context.action_body,
                output_name: graphene.Field(build_context.action_return_type, args=build_context.action_arguments, description=build_context.action_description),
            }
        )
        build_context.set_data("query_class", query_class)
        # Apply decorator to auto detect queries
        decorated_query_class = graphql_decorators.graphql_subquery(query_class)

        return decorated_query_class
