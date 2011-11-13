from haystack.indexes import *
from haystack import site
from events.models import Event, Guest

# Creating Search Index
class EventIndex(SearchIndex):
	text = CharField(document=True,use_template=True)
	name = CharField(model_attr='name')
	date_event = DateTimeField(model_attr='date_event')
	venue = CharField(model_attr='venue')
	intro = CharField(model_attr='intro')
	overview = CharField(model_attr='overview') 	
	result = CharField(model_attr='result')
	category = CharField(model_attr='category')
	coordinator = CharField(model_attr='coordinator')
	

class GuestIndex(SearchIndex):
	text = CharField(document=True,use_template=True)
	name = CharField(model_attr='name')
	organisation = CharField(model_attr='organisation')
	designation = CharField(model_attr='designation')
	details = CharField(model_attr='details')
	
#Register search index 
site.register(Event,EventIndex)
site.register(Guest,GuestIndex)

