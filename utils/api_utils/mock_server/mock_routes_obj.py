import mock_routes_definition as mock_routes_def

from .base import Routes, RoutesDefinition


class WekaContractDetailsRoutes(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.WekaContractDetailsDefinition()


class MSDProviderInquire(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.MSDProviderInquireDefinition()


class MSDRegistration(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.MSDRegistrationDefinition()


class MSDLinkAccounts(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.MSDLinkAccountsDefinition()


class MSDCheckConnectivity(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.MSDCheckConnectivityDefinition()


class Publish(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.PublishDefinition()


class PublishMember(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.PublishMemberDefinition()


class MBIEGetEntities(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.MBIEGetEntitiesDefinition()


class MBIEGetWatchList(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.MBIEGetWatchListDefinition()


class MBIEAppendWatchList(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.MBIEAppendWatchListDefinition()


class MBIEDeleteWatchList(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.MBIEDeleteWatchListDefinition()


class MBIESendNotification(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.MBIESendNotificationDefinition()


class InternalInquireParticipant(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.InternalInquireParticipantDefinition()


class InternalInquireClients(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.InternalInquireClientsDefinition()


class MSDPublishEmployerEvent(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.MSDPublishEmployerEventDefinition()


class EmployerEventsConsumeSep(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.EmployerEventsConsumeSepDefinition()


class EmployerEventsDeleteSep(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.EmployerEventsDeleteSepDefinition()


class EmployerEventsUnlockSep(Routes):
    def create_routes_def_obj(self) -> RoutesDefinition:
        return mock_routes_def.EmployerEventsUnlockSepDefinition()
