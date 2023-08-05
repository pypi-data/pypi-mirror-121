from typing import Dict

from graphene import ObjectType

from django_koldar_utils.graphql_toolsbox.graphql_types import TGrapheneInputType, TGrapheneType, TDjangoModelType


class GraphQLBuildtimeContext(object):
    """
    Contains all the information available during compile time
    """

    def __init__(self, django_type: TDjangoModelType, graphene_type: TGrapheneType, graphene_input_type: TGrapheneInputType, params: Dict[str, any]):
        self.django_type = django_type
        self.graphene_type = graphene_type
        self.graphene_input_type = graphene_input_type

        self.action_arguments = None
        self.action_return_type = None
        self.action_class_name = None
        self.action_description = None
        self.action_body = None

        self.__internal_data = {}
        self.params = params

    def get_data(self, name: str) -> any:
        return self.__internal_data[name]

    def set_data(self, name: str, value: any):
        self.__internal_data[name] = value


    def get_param(self, name: str) -> any:
        return self.params[name]

    def is_param_present(self, *names: str) -> bool:
        """
        Check if several parameter are present in the param dictionary
        """

        return all(filter(lambda x: x in self.params, names))


class GraphQLRuntimeContext(object):
    """
    Contains all the data that we know in runtime
    """

    def __init__(self, build_context: GraphQLBuildtimeContext, root: any, info: any, *args, **kwargs):
        self.build_context = build_context
        self.root = root
        self.info = info,
        self.args = args
        self.kwargs = kwargs

    def get_input(self, name: str) -> ObjectType:
        """
        Fetch a graphql input parameter from the args and kwargs of the graphql query

        :param name: name of the parameter to fetch
        :return: value of the parameter
        """
        if name in self.kwargs:
            return self.kwargs[name]
        for x in self.args:
            if isinstance(x, tuple) and x[0] == name:
                return x[1]
        raise KeyError(f"Could not found the parameter {name} in the graphql arguments: args={self.args} kwargs={self.kwargs}")
