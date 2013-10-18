import webapp2,os,re
from google.appengine.ext import db
import random,hashlib,hmac
import jinja2
from time import *

#loading the template directory

template_dir=os.path.join(os.path.dirname(__file__),'templates')
jinja_env= jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True, extensions=['jinja2.ext.loopcontrols'])

#rendering the html 

# secret for cookie	
SECRET="b!@y@#e#$b$%y%^e^&l&*o*(s()e)_r"
def render_str(template,**params_in_temp):
                t=jinja_env.get_template(template)
                return t.render(params_in_temp)
# hashing
def hash_str(s):
	return hmac.new(SECRET,s).hexdigest() # use bcrypt

# mixing userid with the hash separated by a pipe
def mixer(s):
	return "%s|%s" % (s,hash_str(s)) # use google appengine's session handlers

#authenticity of the cookies 

def checker(h):
	if(h):
		val=h.split('|')[0]
		if(h==mixer(val)):
			return val
		else:
			return None
	else:
		return None



def level_checker(h,p_id):
	if(h):
		val=h.split('|')[0]
		p=Person.get_by_id(p_id)
		if(p.Level<10):
			if(h==mixer(val) and int(val[1:])==p_id ):
				return val
			else:
				return None
		elif(p.Level>=10):
			if(h==mixer(val) and int(val[2:])==p_id ):
				return val
			else:
				return None
	else:
		return None

#the main handler
class QuizHandler(webapp2.RequestHandler):
	
	def render(self,template,**kw):
		self.response.out.write(render_str(template,**kw))
	def write(self,*form,**kw):
		self.response.out.write(*form,**kw)

#database of the person
class Person(db.Model):
	name=db.StringProperty()
	pass_hash=db.StringProperty()
	Level=db.IntegerProperty()
	Completed=db.IntegerProperty()
	Tries=db.IntegerProperty()
	email=db.StringProperty()
	@classmethod
	def by_name(cls,name):
		u=Person.all().filter("name =" ,name).get()
		return u

	@classmethod
	def by_mail(cls,email):
		e=Person.all().filter("email =" ,email).get()
		return e
#Signup form

class Sign(QuizHandler):
	def valid_fname(self,fname):
		if(fname!=""):
			string=re.compile("^[a-zA-Z0-9_\s\d]{2,100}$")
			return string.match(fname)
	
	def valid_cname(self,cname):
		if(cname!=""):
			string=re.compile("^[a-zA-Z0-9_-]{3,100}$")
			return string.match(cname)
	
	def valid_uname(self,uname):
		if(uname!=""):
			string=re.compile("^[a-zA-Z0-9_-]{3,20}$")
			return string.match(uname)
		

	def valid_mail(self,email):
		if(email):
			string=re.compile("^[\S]+@[\S]+\.[\S]+$")
			return string.match(email)
		

	def l_checker(self,u_name,pass1,pass2,email,f_name,c_name):
		if(u_name=="" and email==""  and (f_name=="" and c_name=="")):
			#self.response.out.write("One or Two fields are currently missing")
			self.render('sign.html')
		else:
			if(self.valid_fname(f_name)==None):
				self.render('sign.html',f_name=f_name,c_name=c_name,u_name=u_name,email=email,err_1="Invalid Facebookname")

			if(self.valid_cname(c_name)==None):
				self.render('sign.html',f_name=f_name,c_name=c_name,u_name=u_name,email=email,err_2="Invalid Institution name")

			if(self.valid_uname(u_name)==None):
				self.render('sign.html',f_name=f_name,c_name=c_name,u_name=u_name,email=email,err1="Invalid Username")
			
			elif(pass1!=pass2):
				self.render('sign.html',f_name=f_name,c_name=c_name,u_name=u_name ,email=email ,err3="Passwords Don't match")
		
			elif(len(pass1)<3):
				self.render('sign.html',f_name=f_name,c_name=c_name,u_name=u_name,email=email,err3="Passwords length less than 3 chars")
			elif( self.valid_mail(email)== None):
				self.render('sign.html',f_name=f_name,c_name=c_name,u_name=u_name,email=email,err4="Not a valid email ID")
		
			else:
				
				l=Person.by_name(u_name)
				t=Person.by_mail(email)
				if(l):
					self.render('sign.html',f_name=f_name,c_name=c_name,u_name=u_name,email=email,err1="User already exists")
				elif(t):
					self.render('sign.html',f_name=f_name,c_name=c_name,u_name=u_name,email=email,err4="email already being used")
				else:
					p=Person(email=email,name=u_name,Level=0,Tries=0,pass_hash=(hashlib.sha256(pass2).hexdigest()),Completed=int(time()))
					p.put()
					k=p.key().id()
					enc_uname=mixer(str(k))
					enc_level=mixer(str(p.Level)+str(k))
					self.response.headers.add_header('Set-Cookie','u_name=%s  ; Path=/' % enc_uname)
					self.response.headers.add_header('Set-Cookie','u_level=%s ; Path=/' % enc_level)
					 
					#self.write(self.request.cookies.get('u_level'))
					self.redirect("/welcome")
			#
			#		self.redirect("/")
	
	def get(self):
		self.l_checker("","","","","","")
	def post(self):
		f_name=self.request.get('fname')
		c_name=self.request.get('cname')
		u_name=self.request.get('uname')
		pass1=self.request.get('pass1')
		pass2=self.request.get('pass2')
		email=self.request.get('email')
		self.l_checker(u_name,pass1,pass2,email,f_name,c_name)



class welcome(QuizHandler):
	def front(self):
		enc_uname = self.request.cookies.get('u_name') #getting the value of the cookie which ofcourse is encrypted
		enc_level=self.request.cookies.get('u_level')
		enc_uname2=checker(enc_uname) #authetication
		enc_level2=checker(enc_level)
		if(enc_uname2 and enc_level2): #same as above
			uid=int(checker(enc_uname))
			uname=Person.get_by_id(uid)
			self.render('welcome.html',user_name=uname.name,Level=uname.Level) #render welcome if successful
						
		else:
			self.redirect('/') #else redirect back to the root page (cookie tampering has been done)
	def get(self):
		self.front()	
	


class login(QuizHandler):
#checking the database to see if person exists or not
	def disp(self,uname,passwd):
	
		p=Person.by_name(uname) #the line that actually queries
		
	
		if(p):
			k=p.key().id() #getting the id of the person
			enc_uname=mixer(str(k))
			enc_level=mixer(str(p.Level)+str(k))
			self.response.headers.add_header('Set-Cookie','u_name=%s  ; Path=/' % enc_uname)
			self.response.headers.add_header('Set-Cookie','u_level=%s ; Path=/' % enc_level)
			if p.pass_hash==(hashlib.sha256(passwd).hexdigest()):
				
				self.redirect('/welcome')
			else:
				self.render('front.html',err="Invalid login")
		else:
			self.render('front.html',err="User does not exist")

	def get(self):
		self.render('front.html')
	def post(self):
		uname=self.request.get('uname')
		passwd=self.request.get('passwd')
		self.disp(uname,passwd)
		  





class logout(QuizHandler):
#clearing cookies for the logout operation
	def get(self):
		if(self.request.cookies.get("u_name") and self.request.cookies.get('u_level')):
			self.response.headers.add_header('Set-Cookie','u_name=;Path=/')
			self.response.headers.add_header('Set-Cookie','u_level=;Path=/')
			self.redirect('/')
		else:
			self.write("You are already logged out")


#class Front(QuizHandler):
#	def get(self):
#		self.render("front.html")
	