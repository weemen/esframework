import abc
import inspect

from esframework.domain import DomainEvent
from esframework.exceptions import SchemaMapperException


class SchemaMapper(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def map(self, existing_data: dict, current_event_mapping: dict, cleaning: bool):
        """ mapping serialized data to the properties of the event """
        raise NotImplementedError("Schema processors must implement map method")


class WeakSchemaMapper(SchemaMapper):

    def map(self, existing_data: dict, current_event_mapping: dict, cleaning: bool = True) -> dict:
        """ mapping serialized data to the properties of the event """
        new_data = existing_data.copy()
        properties = current_event_mapping

        if cleaning:
            properties = self.fetch_event_properties_from_event(current_event_mapping)

        for property_name, value in existing_data.items():
            if property_name not in properties.keys():
                del(new_data[property_name])
                continue

        for property_name, value in properties.items():
            if property_name not in existing_data.keys():
                new_data[property_name] = value
                continue

            if isinstance(value, dict) and property_name in existing_data:
                new_data[property_name] = self.map(existing_data[property_name], value, cleaning=False)

        return new_data

    def fetch_event_properties_from_event(self, current_event_mapping: dict) -> dict:
        """ returns a dictionary with all the class properties of the event """
        event_properties = dict()

        for key, element in current_event_mapping.items():
            if not self.is_private_property(key):
                continue

            event_properties[self.get_private_property_name(key)] = element

        return event_properties

    def is_private_property(self, property_name: str) -> bool:
        """ return is a certain property is private or not """
        return property_name[-2:] != '__' and \
               property_name[:1] == '_' and \
               '__' in property_name

    def get_private_property_name(self, property_name: str) -> str:
        """ returns a private property name """
        return property_name[property_name.find('__')+2:]


class SchemaMapperFactory(object):

    @staticmethod
    def factory(version_type: str) -> WeakSchemaMapper:
        """ builds a schema wapper and will return it """
        if version_type == 'weak-schema': return WeakSchemaMapper()
        raise SchemaMapperException('Versioning type does not exist')


def event_versioning(versioning_type: str):
    """ this function is here to allow schema mapping with a simple decorator """
    """ this should make the actual implementation for developers a lot easier """
    def event_mapping(deserialize):
        def wrapper(*args):
            mapper = (SchemaMapperFactory.factory(versioning_type),)
            newargs = args+mapper
            return deserialize(*newargs)

        return wrapper

    return event_mapping
