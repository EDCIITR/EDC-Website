#Global constants are defined here including the menu

#menu = ('Home','About','Events','Initiatives','Associates','Resources','Media',)
#menu = {'Home':'/', 'About':'/', 'Events':'/', 'Initiatives':'/', 'Associates':'/', 'Resources':'/', 'Media':'/',}

#---------Menu constants------------------#
from datetime import datetime, timedelta
from django.core.exceptions import ObjectDoesNotExist

#Haystack
from django.template import add_to_builtins
add_to_builtins('haystack.templatetags.highlight')

class Item:
	def __init__(self,name,url):
		self.name = name
		self.url =  url

home = Item('Home','/')
about = Item('About','/about/')
events = Item('Events','/events/')
initiatives = Item('Initiatives','/initiatives/')
associates = Item('Associates','/associates/')
resources = Item('Resources','/resources/')
media = Item('Media','/edc_media/')
join = Item('Recruitments','/join/')

menu = (home,about,events,initiatives,associates,resources,media,join)

#---------------Event menu constants---------------#
intro = Item('Introduction','')
overview = Item('Overview','overview')
timeline = Item('Timeline','timeline')
incentives = Item('Incentives','incentives')
rules = Item('Rules','rules')
faq = Item('FAQ','faq')
contact=Item('Contact','contact')
sponsors = Item('Sponsors','sponsors')
results = Item('Results','results')

events_menu = (intro,overview,timeline,incentives,rules,sponsors,faq,contact,results,)



#------------Homepage constants--------------#
updates_max = 3
events_max = 3 


#------------Team constants--------------#
ranks = {'member':0,'joint_secy':1,'add_secy':2,'secy':3,'web_master':4}

YEAR_CHOICES = (
			(1,'I'),			
			(2,'II'),
			(3,'III'),	
			(4,'IV'),
		)	

RANK_CHOICES = (
			(ranks['member'],'Member'),
			(ranks['joint_secy'],'Joint Secretary'),
			(ranks['add_secy'],'Additional Secretary'),
			(ranks['secy'],'Secretary'),
			(ranks['web_master'],'Web Master'),
		)
	
BRANCH_CHOICES = (
			('CSE','Computer Science and Engineering'),
			('ECE','Electronics & Communications Engineering'),
			('EE','Electrical Engineering'),
			('ME','Mechanical Engineering'),
			('PI','Production and Industrial Engineering'),
			('MM','Metallurgical Engineering'),
			('BT','Biotechnology'),
			('GPT','Geophysical Technology'),
			('GT','Geological Technology'),
			('CE','Civil Engineering'),
			('ARCH','Architecture and Planning'),
			('CH','Chemical Engineering'),
			('MM','Metallurgical Engineering'),
			('MSM','Integrated Applied Mathematics'),
			('MSP','Integrated Physics'),
			('MSC','Integrated Chemistry'),
			('OTHER','Other'),	
		)


#--------------------------Event Constants---------------#
GUEST_SPEAKER=0
GUEST_PANELIST=1

GUEST_CATEGORY_CHOICES = (
				(GUEST_SPEAKER,'Speaker'),
				(GUEST_PANELIST,'Panelist'),
			)



#--------------------------USER Constants---------------#
USER_MEMBER=0
USER_JUDGE=1
USER_MENTOR = 2
USER_ADMIN = 3

USER_CATEGORY_CHOICES = (
				(USER_MEMBER,'Member'),
				(USER_JUDGE,'Judge'),
				(USER_MENTOR,'Mentor'),
				(USER_ADMIN,'Admin'),
			)




#-----------------------Recruitment Constants------------#
SALUTATION_CHOICES = (
				(0,'Mr.'),
				(1,'Ms.'),
)

def is_overlap(ds1,de1,ds2,de2):
	if(de1<ds2):
		return False
	else:
		 if(de2<ds1):
			return False
	return True


#-------------------Values------------#
BIG_INT_MIN = -9223372036854775808
BIG_INT_MAX = 9223372036854775807	
FB_PREFIX = 'http://www.facebook.com/plugins/like.php?href='
EVENT_RECENT_LIMIT = timedelta(days=60)

