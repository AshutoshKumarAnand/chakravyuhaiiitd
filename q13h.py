

from mine import *
from time import *
import string
# second question
class q13h(QuizHandler):
	def get(self):
		enc_name=self.request.cookies.get('u_name')
		enc_level=self.request.cookies.get('u_level')
		p_id=checker(enc_name)
		if p_id:
			p=Person.get_by_id(int(p_id))
			if(checker(enc_name) and level_checker(enc_level,int(p_id))):
				if(checker(enc_level)[:2]=="12"):
					self.render('q13h.html',error="",Tries=p.Tries)
				else:
					self.redirect("/welcome")
			else:
				self.redirect('/welcome')

		else:
				self.redirect('/welcome')


	def post(self):
		enc=self.request.cookies.get('u_name')
		enc_l=self.request.cookies.get('u_level')
		act=(checker(enc))
		if act:
			p=Person.get_by_id(int(act))
			ans3=self.request.get('ans')
			if((string.lower(ans3)=="apple") and p.Level==12):
			
				p.Level=p.Level+1
				#	p.Check+=1
				p.Completed=int(time())

				p.Tries=0
				p.put()
				enc_level=mixer(str(p.Level)+str(act))
				self.response.headers.add_header('Set-Cookie','u_level=%s ; Path=/' % enc_level)
				self.redirect('/14/q14')
					#p.Check+=1
			else:
			
				
				p.Tries+=1
				p.put()
				if( p.Level==12):
					self.render('q13h.html',error="Incorrect",Tries=p.Tries)
				else:
					self.write("LOL!! , were you just trying to hack!!?")
		else:
			self.redirect('/')	
