
from mine import *

from q2 import *

from q3 import *

from q4 import *

from q5 import *

from q6 import *

from q7 import *

from q8a import *

from q8unbk import *

from q9 import *

from q10 import *

from q11 import *

from q12 import *

from q13 import *

from q13b import *

from q13c import *

from q13d import *

from q13e import *

from q13f import *
from q13h import *

from q14 import *

from q15 import *
from q16 import *
from q16sec import *
from q16thir import *
from q16con import *
from q17 import *

from q18 import *

from q19 import *

from q20 import *
from q21 import *

from q21omsk import *

from q21boston import *

from q21bei import *

from q21par import *

from q21lon import *

from q22 import *

from q23 import *
from q24 import *

from q25 import *
from q26 import *
import string
from q27 import *
from team import *

from rules import *
# first question	

class q1(QuizHandler):
	
	def get(self):
		
		# No tampering with the cookie
		
		enc_name=self.request.cookies.get('u_name')
		enc_level=self.request.cookies.get('u_level')
		p_id=(checker(enc_name))   #No escape to level uncleared
		if(p_id):
			p=Person.get_by_id(int(p_id))
			if(p_id and level_checker(enc_level,int(p_id))):
				if(int(checker(enc_level)[0])==0):
					self.render('q1.html',error="",Tries=p.Tries)
				else:
					self.redirect("/welcome")		
			else:
				self.redirect("/welcome")

		else:
			self.redirect("/welcome")



	def post(self):
		
		enc=self.request.cookies.get('u_name')
		
		act=checker(enc)
		if(act):	
			p=Person.get_by_id(int(act))
			ans1=self.request.get('ans')
			if((string.lower(ans1)=="dtiiiahuyvarkahc")and p.Level==0):
				
				p.Level=p.Level+1
				#p.Check+=1
				p.Tries=0
				p.Completed=int(time())
		
				p.put()
				enc_level=mixer(str(p.Level)+str(act))
				self.response.headers.add_header('Set-Cookie','u_level=%s ; Path=/' % enc_level)
				self.redirect('/2/q2')
					
			else:
				p.Tries+=1
				p.put()
				if(p.Level==0):
					self.render('q1.html',error="incorrect answer",Tries=p.Tries)
				else:
					self.write("LOL,yes we got hacked!!")
		else:
			self.redirect('/')	


class Rank(QuizHandler):
	def lister(self):
		people=db.GqlQuery("select * from Person order by Level desc,Completed asc ")
		self.render('rank.html',people=people)
	def get(self):
		self.lister()
		
class SelfRank(QuizHandler):
	def lister(self):
		people=db.GqlQuery("select * from Person order by Level desc,Completed asc ")
		enc_uname = self.request.cookies.get('u_name') #getting the value of the cookie which ofcourse is encrypted
		enc_level=self.request.cookies.get('u_level')
		enc_uname2=checker(enc_uname) #authetication
		enc_level2=checker(enc_level)
		if(enc_uname2 and enc_level2): #same as above
			uid=int(checker(enc_uname))
			uname=Person.get_by_id(uid)
			self.render('selfrank.html',pass_hash=uname.pass_hash,people=people,Level=uname.Level)
		else:
			self.render('rank.html',err="You are not logged in to view the rank")
	def get(self):
		self.lister()


app=webapp2.WSGIApplication([('/',login) , ('/signup',Sign),('/1/q1',q1),('/2/q2',q2),('/3/q3',q3),('/4/q4',q4) ,('/5/q5',q5),('/6/q6',q6),('/7/q7',q7),('/8/8a',q8a),('/8/q8unbk',q8b),('/9/q9',q9),('/10/q10',q10),('/11/q11',q11),('/12/q12',q12),('/13/q13',q13),('/13/q13/yaoming',q13b),('/13/q13/100',q13c),('/13/q13/302',q13d),('/13/q13f',q13f),('/13/423',q13h),('/14/q14',q14),('/15/q15',q15),('/16/q16',q16),('/16/q16ray',q16sec),('/16/q16thir',q16thir),('/16/connect',q16con),('/17/q17',q17),('/18/q18',q18),('/19/q19',q19),('/20/q20',q20),('/21/q21',q21),('/21/q21omsk',q21omsk),('/21/q21boston',q21boston),('/21/q21lon',q21lon),('/21/q21bei',q21bei),('/21/q21par',q21par),('/22/q22',q22),('/23/q23',q23),('/24/q24',q24),('/25/q25',q25),('/26/q26',q26),('/27/q27',q27),('/welcome',welcome),('/ranking',Rank), ('/logout',logout),('/team',Team),("/rules",Rules),("/selfrank",SelfRank)],debug="True")
