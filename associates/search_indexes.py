from haystack.indexes import *
from haystack import site
from associates.models import Sponsor

# Creating Search Index
class SponsorIndex(SearchIndex):
	text = CharField(document=True,use_template=True)	
	name = CharField(model_attr='name')
	title = CharField(model_attr='title')
	link = CharField(model_attr='link') #URL
	details = CharField(model_attr='details')
	
#Register search index 
site.register(Sponsor, SponsorIndex)

