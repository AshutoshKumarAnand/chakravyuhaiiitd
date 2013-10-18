

from mine import *
from time import *

# second question
class q5(QuizHandler):
	def get(self):
		enc_name=self.request.cookies.get('u_name')
		enc_level=self.request.cookies.get('u_level')
		p_id=checker(enc_name)
		if p_id:
			p=Person.get_by_id(int(p_id))
			if(checker(enc_name) and level_checker(enc_level,int(p_id))):
				if(checker(enc_level)[0]=="4"):
					self.render('q5.html',error="",Tries=0)
				else:
					self.redirect("/welcome")
			else:
				self.redirect('/welcome')

		else:
				self.redirect('/welcome')


	def post(self):
		enc=self.request.cookies.get('u_name')
		enc_l=self.request.cookies.get('u_level')
		act=int(checker(enc))
		p=Person.get_by_id(act)
		ans3=self.request.get('ans')
		if((ans3=="Zhoudaguan" or ans3=="zhoudaguan") and p.Level==4 ):
			
			p.Level=p.Level+1
			#	p.Check+=1
			p.Completed=int(time())

			p.Tries=0
			p.put()
			enc_level=mixer(str(p.Level)+str(act))
			self.response.headers.add_header('Set-Cookie','u_level=%s ; Path=/' % enc_level)
			self.redirect('/')
				#p.Check+=1
		else:
			
				
			p.Tries+=1
			p.put()
			if(p.Tries<=5 and p.Level==4):
				self.render('q5.html',error="Incorrect",Tries=p.Tries)
			else:
				self.write("LOL!! , were you just trying to hack!!?")
			
