from haystack.indexes import *
from haystack import site
from about.models import Member

# Creating Search Index
class MemberIndex(SearchIndex):
	text = CharField(document=True,use_template=True)
	name = CharField(model_attr='name') #name
	email = CharField(model_attr='email')#email
	phone = CharField(model_attr='phone') 
	year = IntegerField(model_attr='year')	
	branch = CharField(model_attr='branch')
	intro = CharField(model_attr='intro') #text
	
#Register search index 
site.register(Member, MemberIndex)

