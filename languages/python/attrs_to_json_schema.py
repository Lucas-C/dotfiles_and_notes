from attr._make import _Nothing
NO_ATTR_DEFAULT = _Nothing()

JSON2ATTR_TYPES = {
    'boolean': [bool],
    'array': [list],
    'number': [float, int],
    'string': [str],
}
KNOWN_ATTR_TYPES = set(sum(JSON2ATTR_TYPES.values(), []))

def make_json_schema(attr_class, title, attr_subclasses=None, description=None, schema_url='http://json-schema.org/draft-04/schema#'):
    properties = {}
    required = []
    subclasses_to_define = set()
    for attribute in attr_class.__attrs_attrs__:
        prop = properties[attribute.name] = {}
        if attribute.convert in KNOWN_ATTR_TYPES:
            prop["type"] = next(type for type, validators in JSON2ATTR_TYPES.items() if attribute.convert in validators)
        elif attribute.validator:
            if attribute.validator.type in KNOWN_ATTR_TYPES:
                prop["type"] = next(type for type, validators in JSON2ATTR_TYPES.items() if attribute.validator.type in validators)
            elif attribute.validator.type in attr_subclasses:
                prop = properties[attribute.name] = {"$ref": "#/definitions/" + attribute.validator.type.__name__}
                subclasses_to_define.add(attribute.validator.type)
        if attribute.default == NO_ATTR_DEFAULT:
            required.append(attribute.name)
        else:
            prop["default"] = attribute.default
    schema = {
        "type": "object",
        "properties": properties,
    }
    if schema_url:
        schema["$schema"] = schema_url
    if title:
        schema["title"] = title
    if description:
        schema["description"] = description
    if required:
        schema["required"] = required
    if subclasses_to_define:
        schema["definitions"] = {klass.__name__: make_json_schema(klass, attr_subclasses=attr_subclasses, title=None, schema_url=None)
                                 for klass in subclasses_to_define}
    return schema


import attr, json

@attr.s
class A:
    a1 = attr.ib(default=0, convert=int)

@attr.s
class B:
    b1 = attr.ib(validator=attr.validators.instance_of(float))
    b2 = attr.ib(validator=attr.validators.instance_of(A))

print(json.dumps(make_json_schema(B, title="B", attr_subclasses=[A]), indent=2, sort_keys=True))
