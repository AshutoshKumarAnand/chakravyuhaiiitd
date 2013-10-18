

from mine import *
from time import *
import string
# second question
class q16con(QuizHandler):
	def get(self):
		enc_name=self.request.cookies.get('u_name')
		enc_level=self.request.cookies.get('u_level')
		p_id=checker(enc_name)
		if p_id:
			p=Person.get_by_id(int(p_id))
			if(checker(enc_name) and level_checker(enc_level,int(p_id))):
				if(checker(enc_level)[:2]=="15"):
					self.render('connect.html',error="",Tries=p.Tries)
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
			if((string.lower(ans3)=="time") and p.Level==15):
			
				p.Level=p.Level+1
				#p.Check+=1
				p.Completed=int(time())

				p.Tries=0
				p.put()
				enc_level=mixer(str(p.Level)+str(act))
				self.response.headers.add_header('Set-Cookie','u_level=%s ; Path=/' % enc_level)
				self.redirect('/17/q17')
					#p.Check+=1
			else:
			
				
				p.Tries+=1
				p.put()
				if( p.Level==15):
					self.render('connect.html',error="Incorrect",Tries=p.Tries)
				else:
					self.write("Oops, our hack checker either caught u doing something fishy or screwed up, no worries just relogin and play on :)")
		else:
			self.redirect('/')	
