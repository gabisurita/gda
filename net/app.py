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

#receive the AnswerSum line and update the OfferingDisplay table of that offering
    def UpdateDisplayOffering(Inst):

        LocDB = create_engine(UserDB, echo=False)
        S = sessionmaker(bind=LocDB)()

        sums = []

        for var in range(0,13):
            sums.append(var)

        sums[0] = (Inst.q1_sim + Inst.q1_nao)
        sums[2] = (Inst.q3_curta + Inst.q3_longa + Inst.q3_adequada)
        sums[3] = Inst.q4_alta + Inst.q4_baixa + Inst.q4_normal
        sums[4] = Inst.q5_alta + Inst.q5_normal + Inst.q5_baixa
        sums[5] = Inst.q6_alta + Inst.q6_normal + Inst.q6_baixa
        sums[6] = Inst.q7_sim + Inst.q7_nao
        sums[7] = Inst.q8_boa + Inst.q8_media + Inst.q8_ruim
        sums[8] = Inst.q9_sim + Inst.q9_nao
        sums[9] = Inst.q10_sim + Inst.q10_nao
        sums[10] = Inst.q11_sim + Inst.q11_nao
        sums[11] = Inst.q12_sim + Inst.q12_nao
        sums[12] = Inst.q13_sim + Inst.q13_nao

        line_of_interest = S.query(OfferingDisplay).filter(Inst.offering_id == OfferingDisplay.offering_id).one()

        if sums[0] != 0:
            line_of_interest.q1_resp = 'Sim'
            line_of_interest.q1_porc = int(100*(Inst.q1_sim/sums[0]))
            if Inst.q1_nao > Inst.q1_sim:
                line_of_interest.q1_resp = 'Não'
                line_of_interest.q1_porc = int(100*(Inst.q1_nao/sums[0]))
        else:
            line_of_interest.q1_resp = '-'
            line_of_interest.q1_porc = 0

        if sums[2] != 0:
            line_of_interest.q3_porc = int(100*((max(Inst.q3_curta, Inst.q3_longa, Inst.q3_adequada))/sums[2]))
            line_of_interest.q3_resp = 'Adequada'

            if Inst.q3_curta > Inst.q3_longa and Inst.q3_curta > Inst.q3_adequada:
                line_of_interest.q3_resp = 'Curta'
            if Inst.q3_longa > Inst.q3_curta and Inst.q3_longa > Inst.q3_adequada:
                line_of_interest.q3_resp = 'Longa'
        else:
            line_of_interest.q3_resp = '-'
            line_of_interest.q3_porc = 0

        if sums[3] != 0:
            line_of_interest.q4_porc = int(100*(max(Inst.q4_alta, Inst.q4_normal, Inst.q4_baixa))/sums[3])
            line_of_interest.q4_resp = 'Normal'

            if Inst.q4_baixa > Inst.q4_alta and Inst.q4_baixa > Inst.q4_normal:
                line_of_interest.q4_resp = 'Baixa'
            if Inst.q4_alta > Inst.q4_baixa and Inst.q4_alta > Inst.q4_normal:
                line_of_interest.q4_resp = 'Alta'
        else:
            line_of_interest.q4_resp = '-'
            line_of_interest.q4_porc = 0

        if sums[4] != 0:
            line_of_interest.q5_porc = int(100*(max(Inst.q5_alta, Inst.q5_normal, Inst.q5_baixa))/sums[4])
            line_of_interest.q5_resp = 'Normal'

            if Inst.q5_baixa > Inst.q5_alta and Inst.q5_baixa > Inst.q5_normal:
                line_of_interest.q5_resp = 'Baixa'
            if Inst.q5_alta > Inst.q5_baixa and Inst.q5_alta > Inst.q5_normal:
                line_of_interest.q5_resp = 'Alta'
        else:
            line_of_interest.q5_resp = '-'
            line_of_interest.q5_porc = 0

        if sums[5] != 0:
            line_of_interest.q6_porc = int(100*(max(Inst.q6_alta, Inst.q6_normal, Inst.q6_baixa))/sums[5])
            line_of_interest.q6_resp = 'Normal'

            if Inst.q6_baixa > Inst.q6_alta and Inst.q6_baixa > Inst.q6_normal:
                line_of_interest.q6_resp = 'Baixa'
            if Inst.q6_alta > Inst.q6_baixa and Inst.q6_alta > Inst.q6_normal:
                line_of_interest.q6_resp = 'Alta'
        else:
            line_of_interest.q6_resp = '-'
            line_of_interest.q6_porc = 0

        if sums[6] != 0:
            line_of_interest.q7_resp = 'Sim'
            line_of_interest.q7_porc = int(100*(Inst.q7_sim/sums[6]))
            if Inst.q7_nao > Inst.q7_sim:
                line_of_interest.q7_resp = 'Não'
                line_of_interest.q7_porc = int(100*(Inst.q7_nao/sums[6]))
        else:
            line_of_interest.q7_resp = '-'
            line_of_interest.q7_porc = 0

        if sums[7] != 0:
            line_of_interest.q8_porc = int(100*(max(Inst.q8_boa, Inst.q8_media, Inst.q8_ruim))/sums[7])
            line_of_interest.q8_resp = 'Média'

            if Inst.q8_ruim > Inst.q8_boa and Inst.q8_ruim > Inst.q8_media:
                line_of_interest.q8_resp = 'Ruim'
            if Inst.q8_boa > Inst.q8_ruim and Inst.q8_boa > Inst.q8_media:
                line_of_interest.q8_resp = 'Boa'
        else:
            line_of_interest.q8_resp = '-'
            line_of_interest.q8_porc = 0

        if sums[8] != 0:
            line_of_interest.q9_resp = 'Sim'
            line_of_interest.q9_porc = int(100*(Inst.q9_sim/sums[8]))
            if Inst.q9_nao > Inst.q9_sim:
                line_of_interest.q9_resp = 'Não'
                line_of_interest.q9_porc = int(100*(Inst.q9_nao/sums[8]))
        else:
            line_of_interest.q9_resp = '-'
            line_of_interest.q9_porc = 0

        if sums[9] != 0:
            line_of_interest.q10_resp = 'Sim'
            line_of_interest.q10_porc = int(100*(Inst.q10_sim/sums[9]))
            if (Inst.q10_nao) > (Inst.q10_sim):
                line_of_interest.q10_resp = 'Sim'
                line_of_interest.q10_porc = int(100*(Inst.q10_nao/sums[9]))
        else:
            line_of_interest.q10_resp = '-'
            line_of_interest.q10_porc = 0

        if sums[10] != 0:
            line_of_interest.q11_resp = 'Sim'
            line_of_interest.q11_porc = int(100*(Inst.q11_sim/sums[10]))
            if Inst.q11_nao > Inst.q11_sim:
                line_of_interest.q11_resp = 'Não'
                line_of_interest.q11_porc = int(100*(Inst.q11_nao/sums[10]))
        else:
            line_of_interest.q11_resp = '-'
            line_of_interest.q11_porc = 0

        if sums[11] != 0:
            line_of_interest.q12_resp = 'Sim'
            line_of_interest.q12_porc = int(100*(Inst.q12_sim/sums[11]))
            if Inst.q12_nao > Inst.q12_sim:
                line_of_interest.q12_resp = 'Não'
                line_of_interest.q12_porc = int(100*(Inst.q12_nao/sums[11]))
        else:
            line_of_interest.q12_resp = '-'
            line_of_interest.q12_porc = 0

        if sums[12] != 0:
            line_of_interest.q13_resp = 'Sim'
            line_of_interest.q13_porc = int(100*(Inst.q13_sim/sums[12]))
            if Inst.q13_nao > Inst.q13_sim:
                line_of_interest.q13_resp = 'Não'
                line_of_interest.q13_porc = int(100*(Inst.q13_nao/sums[12]))
        else:
            line_of_interest.q13_resp = '-'
            line_of_interest.q13_porc = 0

        S.commit()

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

            already_evaluated = False
            LocDB = create_engine(UserDB, echo=False)
            LocS = sessionmaker(bind=LocDB)()
            manobra = LocS.query(StudentRate).filter(
                StudentRate.user_id == Session.user_id).filter(
                StudentRate.offering_id == self.OfferingInst.id)

            if manobra.count() != 0:
                already_evaluated = True

            #modificar o template para usar a variável "already_evaluated" (By Raul)
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

            if ((LocS.query(OfferingDisplay).filter(OfferingDisplay.offering_id == self.OfferingInst.id)).count()) == 0:
                NewDisplay=OfferingDisplay(
                q1_resp = '-',
                q1_porc = 101,
                q2_resp = '-',
                q2_porc = 101,
                q3_resp = '-',
                q3_porc = 101,
                q4_resp = '-',
                q4_porc = 101,
                q5_resp = '-',
                q5_porc = 101,
                q6_resp = '-',
                q6_porc = 101,
                q7_resp = '-',
                q7_porc = 101,
                q8_resp = '-',
                q8_porc = 101,
                q9_resp = '-',
                q9_porc = 101,
                q10_resp = '-',
                q10_porc = 101,
                q11_resp = '-',
                q11_porc = 101,
                q12_resp = '-',
                q12_porc = 101,
                q13_resp = '-',
                q13_porc = 101,
                offering = LocOffering
                )

                LocS.add(NewDisplay)
                LocS.commit()

            elemento = LocS.query(AnswerSum).filter(AnswerSum.offering_id == self.OfferingInst.id).one()

            if auxiliar['0.0'] == u' sim ':
                elemento.q1_sim += 1
            elif auxiliar['0.0'] == u' não ':
                elemento.q1_nao += 1

            if auxiliar['1.0'] == u' correto ':
                elemento.q2_correto += 1
            elif auxiliar['1.0'] == u' antes ':
                elemento.q2_antes += 1
            elif auxiliar['1.0'] == u' depois ':
                elemento.q2_depois += 1

            if auxiliar['2.0'] == u' adequada ':
                elemento.q3_adequada += 1
            elif auxiliar['2.0'] == u' curta ':
                elemento.q3_curta += 1
            elif auxiliar['2.0'] == u' longa ':
                elemento.q3_longa += 1

            if auxiliar['3.0'] == u' alta ':
                elemento.q4_alta += 1
            elif auxiliar['3.0'] == u' normal ':
                elemento.q4_normal += 1
            elif auxiliar['3.0'] == u' baixa ':
                elemento.q4_baixa += 1

            if auxiliar['4.0'] == u' alta ':
                elemento.q5_alta += 1
            elif auxiliar['4.0'] == u' normal ':
                elemento.q5_normal += 1
            elif auxiliar['4.0'] == u' baixa ':
                elemento.q5_baixa += 1

            if auxiliar['5.0'] == u' alta ':
                elemento.q6_alta += 1
            elif auxiliar['5.0'] == u' normal ':
                elemento.q6_normal += 1
            elif auxiliar['5.0'] == u' baixa ':
                elemento.q6_baixa += 1

            if auxiliar['6.0'] == u' sim ':
                elemento.q7_sim += 1
            elif auxiliar['6.0'] == u' não ':
                elemento.q7_nao += 1

            if auxiliar['7.0'] == u' boa ':
                elemento.q8_boa += 1
            elif auxiliar['7.0'] == u' média ':
                elemento.q8_media += 1
            elif auxiliar['7.0'] == u' ruim ':
                elemento.q8_ruim += 1

            if auxiliar['8.0'] == u' sim ':
                elemento.q9_sim += 1
            elif auxiliar['8.0'] == u' não ':
                elemento.q9_nao += 1

            if auxiliar['9.0'] == u' sim ':
                elemento.q10_sim += 1
            elif auxiliar['9.0'] == u' não ':
                elemento.q10_nao += 1

            if auxiliar['10.0'] == u' sim ':
                elemento.q11_sim += 1
            elif auxiliar['10.0'] == u' não ':
                elemento.q11_nao += 1

            if auxiliar['11.0'] == u' sim ':
                elemento.q12_sim += 1
            elif auxiliar['11.0'] == u' não ':
                elemento.q12_nao += 1

            if auxiliar['12.0'] == u' sim ':
                elemento.q13_sim += 1
            elif auxiliar['12.0'] == u' não ':
                elemento.q13_nao += 1

            LocS.commit()

            UpdateDisplayOffering(elemento)
            raise web.seeother('/oferecimentos')
#            try:
#
#
#            except:
#                LocS.rollback()
#                return True


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
