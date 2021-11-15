import json
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.inspection import inspect


class DbModelRelationshipSerializer(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in tuple(x for x in dir(obj) if not x.startswith('_') and x != 'metadata'):
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:

                    # next lines were added to serialize relationship attributes of db models
                    if field in tuple(attr_data[0] for attr_data in inspect(obj.__class__).relationships.items()):

                        serialized_data = []
                        for row in data:
                            relationship_obj_data = {}
                            for attr in tuple(x for x in dir(row) if not x.startswith('_') and x != 'metadata'):
                                obj_field_data = row.__getattribute__(attr)
                                try:
                                    json.dumps(obj_field_data)
                                    relationship_obj_data[attr] = obj_field_data
                                except TypeError:
                                    pass
                            serialized_data.append(relationship_obj_data)
                        fields[field] = serialized_data

            return fields

        return json.JSONEncoder.default(self, obj)
