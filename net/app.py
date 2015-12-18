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
import re

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

    def POSTParse(RawPost):
        """Parse POST Filds into dict."""
        FieldList = [Field.split("=") for Field in RawPost.split("&")]

        try:
            FieldMap = {Q[0]: urllib.unquote(Q[1].replace("+", " ")).
                        decode('utf8') for Q in FieldList}

            return FieldMap
        except:
            return {}

    def IsLogged(Redirect=True):
        """ Define secure (logged in only) area"""
        try:
            if Session.user_id:
                return True
            else:
                if Redirect:
                    raise web.seeother('/login')
                else:
                    return False

        except AttributeError:
            if Redirect:
                raise web.seeother('/login')
            else:
                return False

#recebe dicionário com respostas e atualiza lista de comentários
    def CommitComment(Inst ,Response):
        """Submit a comment to an instance"""


        LocDB = create_engine(UserDB, echo=False)
        LocS = sessionmaker(bind=LocDB)()

        Me = LocS.query(User).filter(User.id == Session.user_id).one()

        LocTeacher = LocS.query(Teacher).filter(
            Teacher.id == Inst.teacher_id).one()
        LocSubject = LocS.query(Subject).filter(
            Subject.id == Inst.subject_id).one()
        LocOffering = LocS.query(Offering).filter(
            Offering.id == Inst.id).one()


        if not Response['text-teacher'] == "":
            NewTeacherComment = TeacherComment(
                text=Response["text-teacher"],
                teacher=LocTeacher,
                user=Me,
                anonymous=False,
                offering=LocOffering)
            LocS.add(NewTeacherComment)

#            NewSubjectComment = SubjectComment(
#                text=Response["text-offering"],
#                subject=LocSubject,
#                user=Me,
#                anonymous=bool("False"))

        if not Response['text-offering'] == "":
            NewOfferingComment = OfferingComment(
                text=Response["text-offering"],
                offering=LocOffering,
                user=Me,
                anonymous=False)
            LocS.add(NewOfferingComment)

        try:
            LocS.commit()
            return False

        except:
            LocS.rollback()
            return True


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
                return Render.register(Form,"",Render)
            else:
                raise web.seeother('/')

        def POST(self):
            Form = RegisterForm()

            if not Form.validates():
                return Render.register(Form,"", Render)

            else:
                S = sessionmaker(bind=DB)()

                Match = re.search(r'[\w.-]+@[\w.-]+.unicamp.br', Form['E-mail'].value)

                check_email = S.query(User).filter(
                    User.email == Form['E-mail'].value)

                check_ra = S.query(Student).filter(
                    Student.ra == Form['RA'].value)


                if Match == None or check_email.count() != 0 or check_ra.count() != 0:
                    return Render.register(Form,"Error", Render)

                NewStudent = Student(
                ra = int(Form['RA'].value),
                name = Form['Nome'].value
                )

                S.add(NewStudent)
                S.commit()

                StudentCall = S.query(Student).filter(
                    Student.ra == int(Form['RA'].value)).one()

                NewUser = User(
                email = Form['E-mail'].value,
                password = Form['Senha'].value,
                confirmed = True,
                student = StudentCall
                )

                S.add(NewUser)
                S.commit()

                UserCall = S.query(User).filter(
                    User.email == Form['E-mail'].value).one()

                Session.user_id = UserCall.id
                raise web.seeother('/')


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

#                UserCall = S.query(User).filter(
#                    User.email == Form['E-mail'].value).one()

#                if UserCall.count():
#                    UserCall = UserCall.one()
#                    if UserCall.password == Form['Senha'].value:
                        # TODO Check confirmation
#                        Session.user_id = UserCall.id
#                        raise web.seeother('/')
#                    else:
#                        return "Meh"

#                else:

#                    Match = re.search(
#                        r'[\w.-]+@[\w.-]+.unicamp.br',
#                        Form['E-mail'].value)

#                    if not Form['E-mail'].value:
#                        return "Meh"

#                    UserCall = User(
#                        email=Form['E-mail'].value,
#                        password=Form['Senha'].value)
                    # student = StudentCall)

                    # TODO Send Mail
                    # web.sendmail(
                    #      'GDA',
                    #      Form['E-mail'].value,
                    #      'subject', 'message')

#                    S.add(UserCall)
#                    S.commit()
#                    UserCall = S.query(User).filter(
#                        User.student == StudentCall).one()

#                    Session.user_id = UserCall.id
#                    return "First, Hi"

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
#            CommitComment(self.TeacherInst, Response)

            return Render.teacherpage(self.TeacherInst, Render)

    class SubjectPage:
        SubjectInst = Subject()

        def GET(self):
            IsLogged()
            return Render.subjectpage(self.SubjectInst, Render)

        def POST(self):
            IsLogged()
            Response = POSTParse(web.data())
#            CommitComment(self.SubjectInst, Response)

            return Render.subjectpage(self.SubjectInst, Render)

    class OfferingPage:
        OfferingInst = Offering()

        def GET(self):
            IsLogged()
            form = RateOffering()
            return Render.offeringpage(self.OfferingInst, Render, form)

        def POST(self):
            IsLogged()
            Response = POSTParse(web.data())
#            CommitComment(self.OfferingInst, Response)
            form = RateOffering()
            #if not form.validates():
            #    return Render.database(Render,form1,form2)
            #else:
            form.validates()
            S = sessionmaker(bind=DB)()
            Rate = OfferingRate(
                            answers=form.d.Respostas,
                            offering_id= self.OfferingInst.id,
                            question1=form.d.Coluna11,
                            question2=form.d.Coluna12,
                            question3=form.d.Coluna13,
                            question4=form.d.Coluna14,
                            question5=form.d.Coluna15,
                            question6=form.d.Coluna16)
            S.add(Rate)
            S.commit()
            #return self.OfferingInst.id
            return Render.offeringpage(self.OfferingInst, Render,form)

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
            auxiliar = POSTParse(web.data())

            LocDB = create_engine(UserDB, echo=False)
            LocS = sessionmaker(bind=LocDB)()

            chaves = []

            #atualizar com range de perguntas (by Raul)
            for var in range(0,13):
                chaves.append(str(float(var)))

            for x in chaves:
                if x not in auxiliar.keys():
                    auxiliar[x] = None

            if 'text-offering' not in auxiliar.keys():
                auxiliar['text-offering'] = None
            if 'text-teacher' not in auxiliar.keys():
                auxiliar['text-teacher'] = None

#            LocTeacher = LocS.query(Teacher).filter(
#                Teacher.id == self.OfferingInst.teacher_id).one()

#            LocSubject = LocS.query(Subject).filter(
#                Subject.id == self.OfferingInst.subject_id).one()

#            LocSemester = LocS.query(Semester).filter(
#                Semester.id == self.OfferingInst.semester_id).one()

            Me = LocS.query(User).filter(User.id == Session.user_id).one()
            LocOffering = LocS.query(Offering).filter(
                Offering.id == self.OfferingInst.id).one()

            CommitComment(self.OfferingInst, auxiliar)

            NewEvaluation = StudentRate(

            question1 = auxiliar['0.0'],
            question2 = auxiliar['1.0'],
            question3 = auxiliar['2.0'],
            question4 = auxiliar['3.0'],
            question5 = auxiliar['4.0'],
            question6 = auxiliar['5.0'],
            question7 = auxiliar['6.0'],
            question8 = auxiliar['7.0'],
            question9 = auxiliar['8.0'],
            question10 = auxiliar['9.0'],
            question11 = auxiliar['10.0'],
            question12 = auxiliar['11.0'],
            question13 = auxiliar['12.0'],

            user = Me,
            offering = LocOffering
            )

            try:
                LocS.add(NewEvaluation)
                LocS.commit()


                if (LocS.query(AnswerSum.offering_id).filter(AnswerSum.offering_id == self.OfferingInst.id).count())==0:
                    NewSum = AnswerSum(
                    q1_sim = 0,
                    q1_nao = 0,
                    q2_correto = 0,
                    q2_antes = 0,
                    q2_depois = 0,
                    q3_adequada = 0,
                    q3_curta = 0,
                    q3_longa = 0,
                    q4_alta = 0,
                    q4_normal = 0,
                    q4_baixa = 0,
                    q5_alta = 0,
                    q5_normal = 0,
                    q5_baixa = 0,
                    q6_alta = 0,
                    q6_normal = 0,
                    q6_baixa = 0,
                    q7_sim = 0,
                    q7_nao = 0,
                    q8_boa = 0,
                    q8_media = 0,
                    q8_ruim = 0,
                    q9_sim = 0,
                    q9_nao = 0,
                    q10_sim = 0,
                    q10_nao = 0,
                    q11_sim = 0,
                    q11_nao = 0,
                    q12_sim = 0,
                    q12_nao = 0,
                    q13_sim = 0,
                    q13_nao = 0,
                    offering = LocOffering
                    )
                    LocS.add(NewSum)
                    LocS.commit()

                elemento = LocS.query(AnswerSum).filter(AnswerSum.offering_id == self.OfferingInst.id).one()

                if auxiliar['0.0'] == ' sim ':
                    elemento.q1_sim += 1
                elif auxiliar['0.0'] == ' não ':
                    elemento.q1_nao += 1

                if auxiliar['1.0'] == ' correto ':
                    elemento.q2_correto += 1
                elif auxiliar['1.0'] == ' antes ':
                    elemento.q2_antes += 1
                elif auxiliar['1.0'] == ' depois ':
                    elemento.q2_depois += 1

                if auxiliar['2.0'] == ' adequada ':
                    elemento.q3_adequada += 1
                elif auxiliar['2.0'] == ' curta ':
                    elemento.q3_curta += 1
                elif auxiliar['2.0'] == ' longa ':
                    elemento.q3_longa += 1

                if auxiliar['3.0'] == ' alta ':
                    elemento.q4_alta += 1
                elif auxiliar['3.0'] == ' normal ':
                    elemento.q4_normal += 1
                elif auxiliar['3.0'] == ' baixa ':
                    elemento.q4_baixa += 1

                if auxiliar['4.0'] == ' alta ':
                    elemento.q5_alta += 1
                elif auxiliar['4.0'] == ' normal ':
                    elemento.q5_normal += 1
                elif auxiliar['4.0'] == ' baixa ':
                    elemento.q5_baixa += 1

                if auxiliar['5.0'] == ' alta ':
                    elemento.q6_alta += 1
                elif auxiliar['5.0'] == ' normal ':
                    elemento.q6_normal += 1
                elif auxiliar['5.0'] == ' baixa ':
                    elemento.q6_baixa += 1

                if auxiliar['6.0'] == ' sim ':
                    elemento.q7_sim += 1
                elif auxiliar['6.0'] == ' não ':
                    elemento.q7_nao += 1

                if auxiliar['7.0'] == ' boa ':
                    elemento.q8_boa += 1
                elif auxiliar['7.0'] == ' média ':
                    elemento.q8_media += 1
                elif auxiliar['7.0'] == ' ruim ':
                    elemento.q8_ruim += 1

                if auxiliar['8.0'] == ' sim ':
                    elemento.q9_sim += 1
                elif auxiliar['8.0'] == ' não ':
                    elemento.q9_nao += 1

                if auxiliar['9.0'] == ' sim ':
                    elemento.q10_sim += 1
                elif auxiliar['9.0'] == ' não ':
                    elemento.q10_nao += 1

                if auxiliar['10.0'] == ' sim ':
                    elemento.q11_sim += 1
                elif auxiliar['10.0'] == ' não ':
                    elemento.q11_nao += 1

                if auxiliar['11.0'] == ' sim ':
                    elemento.q12_sim += 1
                elif auxiliar['11.0'] == ' não ':
                    elemento.q12_nao += 1

                if auxiliar['12.0'] == ' sim ':
                    elemento.q13_sim += 1
                elif auxiliar['12.0'] == ' não ':
                    elemento.q13_nao += 1

                LocS.commit()

                raise web.seeother('/oferecimentos')


            except:
                LocS.rollback()
                return True


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

    class Database:
        def GET(self):
            IsLogged()
            form1 = AddOffering()
            # make sure you create a copy of the form by calling it (line above)
            # Otherwise changes will appear globally
            return Render.database(Render,form1)

        def POST(self):
            form1 = AddOffering()
            #if not form.validates():
            #    return Render.database(Render,form1,form2)
            #else:
            form1.validates()
            S = sessionmaker(bind=DB)()
            Off = Offering(subject_id=form1.d.Disciplina,
                            teacher_id=form1.d.Professor,
                            semester_id=form1.d.Semestre,
                            students = int(form1.d.Matriculados),
                            code = form1.d.Turma)
            S.add(Off)
            S.commit()

            #huebr

            return Render.database(Render,form1)


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
    Map(Database, "/database")

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
