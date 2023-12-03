from neomodel import StringProperty, UniqueIdProperty, RelationshipTo, StructuredNode

class Employee(StructuredNode):
    uid = UniqueIdProperty()
    emp_name = StringProperty()
# endclass