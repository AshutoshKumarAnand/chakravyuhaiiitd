

from mine import *
from time import *
import string



class q13c(QuizHandler):
	def get(self):
		enc_name=self.request.cookies.get('u_name')
		enc_level=self.request.cookies.get('u_level')
		p_id=checker(enc_name)
		if p_id:
			p=Person.get_by_id(int(p_id))
			if(checker(enc_name) and level_checker(enc_level,int(p_id))):
				if(checker(enc_level)[:2]=="12"):
					self.render("q13c.html")
				else:
					self.redirect("/welcome")
			else:
				self.redirect('/welcome')

		else:
				self.redirect('/welcome')


		
