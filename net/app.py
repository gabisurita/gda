#!/usr/env/python
#encoding:utf-8
"""GDA Website."""

import web
import os
import codecs
#import markdown
import urllib
from models import *
from config import *

os.chdir(BaseDir)  
web.config.debug = False  

BaseTitle = "GDA"

def Setup():
  # Render the layouts
  Render = web.template.render('templates/', globals=globals(), cache=False)

  # initialize the application
  App = web.application(mapping=(), fvars=globals())
  
  # User session accounts handled by file  
  Session = web.session.Session(App, web.session.DiskStore('sessions'), initializer={})
  
  # Define "Log in only" Area 
  def IsLogged():
    try:
      if Session.user_id:  
        return True
    except AttributeError:
      raise web.seeother('/login')

  # Form Handdlers  
  LoginForm = web.form.Form(
    web.form.Textbox('RA', web.form.notnull, Class="form-control"),
    web.form.Password('Senha', web.form.notnull, Class="form-control"),
    web.form.Button('Login', Class="btn btn-primary"),
  )
  
  RegisterForm = web.form.Form(
    web.form.Textbox('RA', web.form.notnull, Class="form-control"),
    web.form.Textbox('Nome', web.form.notnull, Class="form-control"),
    web.form.Textbox('E-mail', web.form.notnull, Class="form-control"),
    web.form.Password('Senha', web.form.notnull, Class="form-control"),
    web.form.Button('Login', Class="btn btn-primary"),
  )

  SearchForm = web.form.Form(
    web.form.Textbox('Busca', Class="form-control"),
  )
  
  
  # Page classes (handlers)
  class LoginPage:  
    def GET(self):
      Form = LoginForm
      return Render.login(Form, "", Render)
      
    def POST(self):
      Form = LoginForm
      
      if not Form.validates(): 
        return Render.login(Form, "Ocorreu um erro, tente novamente.", Render)
      
      else:
        S = sessionmaker(bind=DB)()
        StudentCall = S.query(Student).filter(Student.ra == int(Form['RA'].value))
        
        if StudentCall.count():
          StudentCall = StudentCall.one()
          UserCall = S.query(User).filter(User.student == StudentCall)
        else:
          return Render.login(Form, "Usuário não cadastrado.", Render)
          
        if UserCall.count():
          UserCall = UserCall.one()
          if UserCall.password == Form['Senha'].value:
#          if Caller.confirmed == Form['Senha']:
            Session.user_id = UserCall.id
            raise web.seeother('/')
          else:
            return Render.login(Form, "Senha inválida", Render)
        else:
          return Render.login(Form, "Usuário não cadastrado.", Render)


  class RegisterPage:   
    def GET(self):
      Form = RegisterForm()
      return Render.login(Form, Render)
      
    def POST(self):
      Form = RegisterForm()
      
      if not Form.validates(): 
        return Render.login(Form, Render)
      
      else:             
        S = sessionmaker(bind=DB)()
        StudentCall = S.query(Student).filter(Student.ra == int(Form['RA'].value))
        
        if StudentCall.count():
          StudentCall = StudentCall.one()
          UserCall = S.query(User).filter(User.student == StudentCall)
        else:
          StudentCall = Student(ra = Form['RA'].value, name = Form['Nome'].value)
          S.add(StudentCall)
          # mail()
          S.commit()          
          Map(StudentPage, "/estudantes/%s" % str(StudentCall.ra).zfill(6), dict(StudentInst = StudentCall))
          UserCall = S.query(User).filter(User.student == StudentCall)
        
        if UserCall.count():
          UserCall = UserCall.one()
          if UserCall.password == Form['Senha'].value:
#          if Caller.confirmed == Form['Senha']:
            Session.user_id = UserCall.id
            raise web.seeother('/')
          else:
            return "Meh"
        
        else:
          
          Match = re.search(r'[\w.-]+@[\w.-]+.unicamp.br', Form['E-mail'].value)
          
          if not Form['E-mail'].value:
            return "Meh"
            
          UserCall = User(email = Form['E-mail'].value, password = Form['Senha'].value, student = StudentCall)
#          web.sendmail('GDA', Form['E-mail'].value, 'subject', 'message')
          
          S.add(UserCall)
          S.commit()
          UserCall = S.query(User).filter(User.student == StudentCall).one()      
          Session.user_id = UserCall.id
          return "First, Hi"

    
  class StudentPage:
    StudentInst = Student()
    
    def GET(self):
      IsLogged()
      return Render.studentpage(self.StudentInst, Render)
        

  class TeacherPage:
    TeacherInst = Teacher()
    
    def GET(self):
      IsLogged()
      return Render.teacherpage(self.TeacherInst, Render)

  
  class SubjectPage:
    SubjectInst = Subject()
    
    def GET(self):
      IsLogged()
      return Render.subjectpage(self.SubjectInst, Render)


  class OfferingPage:
    OfferingInst = Offering()
    
    def GET(self):
      IsLogged()
      return Render.offeringpage(self.OfferingInst, Render)

  
  class SearchTeacher:
    def GET(self):
      IsLogged()
      return Render.searchteacher(Render)


  class SearchSubject:  
    def GET(self):
      IsLogged()
      return Render.searchsubject(Render)


  class SearchOffering:
    def GET(self):
      IsLogged()
      return Render.searchoffering(Render)

  
  class EvaluatePage:
    OfferingInst = Offering()
    
    def GET(self):
      IsLogged()
      return Render.evaluatepage(self.OfferingInst, Render)

    def POST(self):
      IsLogged()
      Questions = [Field.split("=") for Field in web.data().split("&")]
      return Questions


  class IndexPage:
    def GET(self):
      IsLogged()
      return Render.index(Render)



  # URL Mappings     
  S = sessionmaker(bind=DB)()
  
  def Map(Inst, URL, AttMap = {}):
    """ Map an object to an URL. """
    
    globals()[URL] = type(URL, (Inst, object,), AttMap)
    App.add_mapping(URL.lower().replace(" ","_").decode("utf8"), URL)
    App.add_mapping(URL.lower().replace(" ","_").decode("utf8")+"/", URL)



  Map(IndexPage, "/")
  Map(LoginPage, "/login")
  Map(RegisterPage, "/registrar")
  Map(SearchTeacher, "/docentes")  
  Map(SearchSubject, "/disciplinas")
  Map(SearchOffering, "/oferecimentos")
  
  
  for Line in S.query(Student):
    Map(StudentPage, Line.EncodeURL(), dict(StudentInst = Line))
  
  for Line in S.query(Teacher):
    Map(TeacherPage, Line.EncodeURL(), dict(TeacherInst = Line))

  for Line in S.query(Subject):
    Map(SubjectPage, Line.EncodeURL(), dict(SubjectInst = Line))

  for Line in S.query(Offering):
    Map(OfferingPage, Line.EncodeURL(), dict(OfferingInst = Line))
    Map(EvaluatePage, Line.EvaluationURL(), dict(OfferingInst = Line))
    
       

  # Built-in static handler 
  if AppStaticHandler:
    for Dir in StaticDirs:
      try:
        App.add_mapping("%s/.+" % Dir, Dir)
      except AttributeError:
        pass


  # Test for custom 404
  def notfound():
    return web.notfound(Render.notfound())
  try:  
    App.notfound = notfound
  except: 
    pass
        
  return App, Render



App, Render = Setup()
WSGI = App.wsgifunc() # WSGI Ready method.
 
if __name__ == "__main__": 
  App.run()  

