from neomodel import StringProperty, UniqueIdProperty, StructuredRel, ArrayProperty

class SentFromRel(StructuredRel):
    rel_id = UniqueIdProperty()
# endclass

class SentToRel(StructuredRel):
    rel_id = UniqueIdProperty()
# endclass
    

class SentCcRel(StructuredRel):
    rel_id = UniqueIdProperty()
# endclass