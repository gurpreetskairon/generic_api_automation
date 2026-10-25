from abc import ABC, abstractmethod


class RoutesDefinition(ABC):
    @abstractmethod
    def create_routes_def(self, arg):
        pass


class Routes(ABC):
    @abstractmethod
    def create_routes_def_obj(self) -> RoutesDefinition:
        pass

    def create_routes_def(self, arg=None):
        routes_def_obj = self.create_routes_def_obj()
        return routes_def_obj.create_routes_def(arg)
