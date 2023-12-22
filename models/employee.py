from neomodel import StringProperty, UniqueIdProperty, RelationshipTo, StructuredNode, RelationshipFrom, IntegerProperty, ArrayProperty
import models.sent_rels as sent_rels

class Employee(StructuredNode):
    uid = UniqueIdProperty()
    emp_name = StringProperty()
    address = StringProperty()
    sent_from = RelationshipTo('EmailMessage', 'SENT_FROM', model=sent_rels.SentFromRel)
    sent_to = RelationshipFrom('EmailMessage', 'SENT_TO', model=sent_rels.SentToRel)
    sent_cc = RelationshipFrom('EmailMessage', 'SENT_CC', model=sent_rels.SentCcRel)
# endclass
    
class EmailMessage(StructuredNode):
    mid = IntegerProperty(unique_index=True)
    sender = StringProperty()
    recipients = ArrayProperty()
    cc = ArrayProperty()
    subject = StringProperty()
    message = StringProperty()
    sent_from = RelationshipFrom('Employee', 'SENT_FROM', model=sent_rels.SentFromRel)
    sent_to = RelationshipTo('Employee', 'SENT_TO', model=sent_rels.SentToRel)
    sent_cc = RelationshipTo('Employee', 'SENT_CC', model=sent_rels.SentCcRel)
    body = StringProperty()
# endclass