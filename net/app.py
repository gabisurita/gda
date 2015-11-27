#!/usr/env/python
# encoding:utf-8

"""GDA Website."""

from constants import *

import web
import os
import codecs
import urllib
from models import *
from forms import *
from setup import *

def Setup():

    # Start DB
    CreateDB()

    # Render the layouts
    Render = web.template.render(BaseDir+'/templates/',
                                 cache=False, globals=globals())

    """Initial server configuration."""

    # initialize the application
    App = web.application(mapping=(), fvars=globals())

    # User session accounts handled by file
    Session = web.session.Session(App, web.session.DiskStore(
        'sessions'), initializer={})

    def Map(Inst, URL, AttMap={}):
        """ Map an object to an URL. """

        globals()[URL] = type(URL, (Inst, object,), AttMap)
        App.add_mapping(URL.lower().replace(
            " ", "_").decode("utf8"), URL)
        App.add_mapping(URL.lower().replace(
            " ", "_").decode("utf8")+"/", URL)

    # Page classes (handlers)
    class LoginPage:
        def GET(self):
            if not IsLogged(Redirect=False):
                Form = LoginForm
                return Render.login(Form, "", Render)
            else:
                raise web.seeother('/')

        def POST(self):
            Form = LoginForm

            if not Form.validates():
                return Render.login(
                    Form, "Ocorreu um erro, tente novamente.", Render)

            else:
                S = sessionmaker(bind=DB)()

                UserCall = S.query(User).filter(
                    User.email == Form['email'].value)

                # Students disabled
#                StudentCall = S.query(Student).filter(
#                    Student.ra == int(Form['RA'].value))

#                if StudentCall.count():
#                    StudentCall = StudentCall.one()
#                    UserCall = S.query(User).filter(
#                        User.student == StudentCall)

#                else:
#                    return Render.login(
#                        Form, "Usuário não cadastrado.", Render)

                if UserCall.count():
                    UserCall = UserCall.one()
                    if UserCall.password == Form['senha'].value:
                        # TODO Check email confirmation
                        Session.user_id = UserCall.id
                        raise web.seeother('/')
                    else:
                        return Render.login(Form, "Senha inválida", Render)
                else:
                    return Render.login(
                        Form, "Usuário não cadastrado.", Render)

    class RegisterPage:
        def GET(self):
            if not IsLogged(Redirect=False):
                Form = RegisterForm()
                return Render.login(Form, Render)
            else:
                raise web.seeother('/')

        def POST(self):
            Form = RegisterForm()

            if not Form.validates():
                return Render.login(Form, Render)

            else:
                S = sessionmaker(bind=DB)()

                # Students disabled
#                StudentCall = S.query(Student).filter(
#                    Student.ra == int(Form['RA'].value))

#                if StudentCall.count():
#                    StudentCall = StudentCall.one()
#                    UserCall = S.query(User).filter(
#                        User.student == StudentCall)

#                else:
#                    StudentCall = Student(
#                        ra = Form['RA'].value, name = Form['Nome'].value)
#                    S.add(StudentCall)

#                    S.commit()

#                    Map(StudentPage, "/estudantes/%s" % str(
#                        StudentCall.ra).zfill(6),
#                        dict(StudentInst = StudentCall))

#                    UserCall = S.query(User).filter(
#                        User.student == StudentCall)

                UserCall = S.query(User).filter(
                    User.email == Form['E-mail'].value).one()

                if UserCall.count():
                    UserCall = UserCall.one()
                    if UserCall.password == Form['Senha'].value:
                        # TODO Check confirmation
                        Session.user_id = UserCall.id
                        raise web.seeother('/')
                    else:
                        return "Meh"

                else:

                    Match = re.search(
                        r'[\w.-]+@[\w.-]+.unicamp.br',
                        Form['E-mail'].value)

                    if not Form['E-mail'].value:
                        return "Meh"

                    UserCall = User(
                        email=Form['E-mail'].value,
                        password=Form['Senha'].value)
                    # student = StudentCall)

                    # TODO Send Mail
                    # web.sendmail(
                    #      'GDA',
                    #      Form['E-mail'].value,
                    #      'subject', 'message')

                    S.add(UserCall)
                    S.commit()
                    UserCall = S.query(User).filter(
                        User.student == StudentCall).one()

                    Session.user_id = UserCall.id
                    return "First, Hi"

    # TODO Destroy Session
    class LogoutPage:
        def GET(self):
            Session.user_id = False
            raise web.seeother('/')

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

        def POST(self):
            IsLogged()
            Response = POSTParse(web.data())
            CommitComment(self.TeacherInst, Response)

            return Render.teacherpage(self.TeacherInst, Render)

    class SubjectPage:
        SubjectInst = Subject()

        def GET(self):
            IsLogged()
            return Render.subjectpage(self.SubjectInst, Render)

        def POST(self):
            IsLogged()
            Response = POSTParse(web.data())
            CommitComment(self.SubjectInst, Response)

            return Render.subjectpage(self.SubjectInst, Render)

    class OfferingPage:
        OfferingInst = Offering()

        def GET(self):
            IsLogged()
            return Render.offeringpage(self.OfferingInst, Render)

        def POST(self):
            IsLogged()
            Response = POSTParse(web.data())
            CommitComment(self.OfferingInst, Response)

            return Render.offeringpage(self.OfferingInst, Render)

    # TODO Unfinished
    class UploadHandler:
        def GET(self):
                web.header("Content-Type", "text/html; charset=utf-8")
                return """
<html><head></head><body>
<form method="POST" enctype="multipart/form-data" action="">
<input type="file" name="myfile" />
<br/>
<input type="submit" />
</form>
</body></html>"""

        def POST(self):
                x = web.input(myfile={})
                filedir = 'uploads' # change this to the directory you want to store the file in.
                if 'myfile' in x: # to check if the file-object is created
                        filepath=x.myfile.filename.replace('\\','/') # replaces the windows-style slashes with linux ones.
                        filename=filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
                        fout = open(filedir +'/'+ filename,'w') # creates the file where the uploaded file should be stored
                        fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
                        fout.close() # closes the file, upload complete.
                raise web.seeother('/upload')

#        OfferingInst = Offering()
#
#        def GET(self):
#            IsLogged()
#            return Render.offeringpage(self.OfferingInst, Render)

#        def POST(self):
#            IsLogged()
#            Response = POSTParse(web.data())
#            CommitComment(self.OfferingInst, Response)
#
#            return Render.offeringpage(self.OfferingInst, Render)
#
#

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
            return POSTParse(web.data())

    class FaqPage:
        def GET(self):
            IsLogged()
            return Render.faq(Render)

    class IndexPage:
        def GET(self):
            IsLogged()
            return Render.index(Render)

    class SemesterPage:
        SemesterInst = Semester()

        def GET(self):
            IsLogged()
            return Render.semesterpage(self.SemesterInst, Render)

    # URL Mappings
    S = sessionmaker(bind=DB)()

    Map(UploadHandler, "/upload")
    Map(IndexPage, "/")
    Map(LoginPage, "/login")
    Map(RegisterPage, "/registrar")
    Map(LogoutPage, "/logout")
    Map(SearchTeacher, "/docentes")
    Map(SearchSubject, "/disciplinas")
    Map(SearchOffering, "/oferecimentos")
    Map(FaqPage, "/faq")

    for Line in S.query(Student):
        Map(StudentPage, Line.EncodeURL(), dict(StudentInst=Line))

    for Line in S.query(Teacher):
        Map(TeacherPage, Line.EncodeURL(), dict(TeacherInst=Line))

    for Line in S.query(Subject):
        Map(SubjectPage, Line.EncodeURL(), dict(SubjectInst=Line))

    for Line in S.query(Offering):
        Map(OfferingPage, Line.EncodeURL(), dict(OfferingInst=Line))
        Map(EvaluatePage, Line.EvaluationURL(), dict(OfferingInst=Line))

    for Line in S.query(Semester):
        Map(SemesterPage, Line.EncodeURL(), dict(SemesterInst=Line))

    # Built-in static handler
    if AppStaticHandler:
        for Dir in StaticDirs:
            try:
                Path = os.path.abspath(__file__) + "/" + Dir
                App.add_mapping("%s/.+" % Dir, Path)
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


# Caller
App, Render = Setup()
WSGI = App.wsgifunc()  # WSGI Ready method.


if __name__ == "__main__":
    App.run()
