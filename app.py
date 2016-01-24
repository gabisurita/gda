#!/usr/env/python
# encoding:utf-8

"""GDA Website."""

from __future__ import division
from constants import *

from random import choice

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

    # Initialize mailing features
    web.config.smtp_server = 'smtp.gmail.com'
    web.config.smtp_port = 587
    web.config.smtp_username = 'gda.noreply@gmail.com'
    web.config.smtp_password = 'provasantigas2016'
    web.config.smtp_starttls = True

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
                Render.user_id = Session.user_id
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

    def IsConfirmed(Redirect=True):
        """ Define confirmed area"""

        LocDB = create_engine(UserDB, echo=False)
        LocS = sessionmaker(bind=LocDB)()
        ob = LocS.query(User).filter(Session.user_id == User.id).one()

        try:
            if ob.confirmed == 1:
                return True
            else:
                if Redirect:
                    raise web.seeother('/confirmacao')
                else:
                    return False

        except AttributeError:
            if Redirect:
                raise web.seeother('/confirmacao')
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
    def UpdateOfferingDisplay(Inst):

        LocDB = create_engine(UserDB, echo=False)
        S = sessionmaker(bind=LocDB)()

        sums = []

        for var in range(0,13):
            sums.append(var)

        sums[0] = (Inst.q1_sim + Inst.q1_nao)
        sums[2] = (Inst.q3_curta + Inst.q3_longa + Inst.q3_adequada)
        sums[3] = Inst.q4_alta + Inst.q4_baixa + Inst.q4_normal
        sums[4] = Inst.q5_dificil + Inst.q5_normal + Inst.q5_facil
        sums[5] = Inst.q6_dificil + Inst.q6_normal + Inst.q6_facil
        sums[6] = Inst.q7_sim + Inst.q7_nao
        sums[7] = Inst.q8_boa + Inst.q8_media + Inst.q8_ruim
        sums[8] = Inst.q9_sim + Inst.q9_nao
        sums[9] = Inst.q10_sim + Inst.q10_nao
        sums[10] = Inst.q11_sim + Inst.q11_nao
        sums[11] = Inst.q12_sim + Inst.q12_nao
        sums[12] = Inst.q13_sim + Inst.q13_nao

        line_of_interest = S.query(OfferingDisplay).filter(Inst.offering_id == OfferingDisplay.offering_id).one()

        if sums[0] != 0:
            line_of_interest.q1_resp = u'Sim'
            line_of_interest.q1_porc = int(100*(Inst.q1_sim/sums[0]))
            if Inst.q1_nao > Inst.q1_sim:
                line_of_interest.q1_resp = u'Não'
                line_of_interest.q1_porc = int(100*(Inst.q1_nao/sums[0]))
        else:
            line_of_interest.q1_resp = u''
            line_of_interest.q1_porc = 0

        if sums[2] != 0:
            line_of_interest.q3_porc = int(100*((max(Inst.q3_curta, Inst.q3_longa, Inst.q3_adequada))/sums[2]))
            line_of_interest.q3_resp = u'Adequada'

            if Inst.q3_curta > Inst.q3_longa and Inst.q3_curta > Inst.q3_adequada:
                line_of_interest.q3_resp = u'Curta'
            if Inst.q3_longa > Inst.q3_curta and Inst.q3_longa > Inst.q3_adequada:
                line_of_interest.q3_resp = u'Longa'
        else:
            line_of_interest.q3_resp = u''
            line_of_interest.q3_porc = 0

        if sums[3] != 0:
            line_of_interest.q4_porc = int(100*(max(Inst.q4_alta, Inst.q4_normal, Inst.q4_baixa))/sums[3])
            line_of_interest.q4_resp = u'Normal'

            if Inst.q4_baixa > Inst.q4_alta and Inst.q4_baixa > Inst.q4_normal:
                line_of_interest.q4_resp = u'Baixa'
            if Inst.q4_alta > Inst.q4_baixa and Inst.q4_alta > Inst.q4_normal:
                line_of_interest.q4_resp = u'Alta'
        else:
            line_of_interest.q4_resp = u''
            line_of_interest.q4_porc = 0

        if sums[4] != 0:
            line_of_interest.q5_porc = int(100*(max(Inst.q5_dificil, Inst.q5_normal, Inst.q5_facil))/sums[4])
            line_of_interest.q5_resp = u'Normal'

            if Inst.q5_facil > Inst.q5_dificil and Inst.q5_facil > Inst.q5_normal:
                line_of_interest.q5_resp = u'Fácil'
            if Inst.q5_dificil > Inst.q5_facil and Inst.q5_dificil > Inst.q5_normal:
                line_of_interest.q5_resp = u'Difícil'
        else:
            line_of_interest.q5_resp = u''
            line_of_interest.q5_porc = 0

        if sums[5] != 0:
            line_of_interest.q6_porc = int(100*(max(Inst.q6_dificil, Inst.q6_normal, Inst.q6_facil))/sums[5])
            line_of_interest.q6_resp = u'Normal'

            if Inst.q6_facil > Inst.q6_dificil and Inst.q6_facil > Inst.q6_normal:
                line_of_interest.q6_resp = u'Fácil'
            if Inst.q6_dificil > Inst.q6_facil and Inst.q6_dificil > Inst.q6_normal:
                line_of_interest.q6_resp = u'Difícil'
        else:
            line_of_interest.q6_resp = u''
            line_of_interest.q6_porc = 0

        if sums[6] != 0:
            line_of_interest.q7_resp = u'Sim'
            line_of_interest.q7_porc = int(100*(Inst.q7_sim/sums[6]))
            if Inst.q7_nao > Inst.q7_sim:
                line_of_interest.q7_resp = u'Não'
                line_of_interest.q7_porc = int(100*(Inst.q7_nao/sums[6]))
        else:
            line_of_interest.q7_resp = u''
            line_of_interest.q7_porc = 0

        if sums[7] != 0:
            line_of_interest.q8_porc = int(100*(max(Inst.q8_boa, Inst.q8_media, Inst.q8_ruim))/sums[7])
            line_of_interest.q8_resp = u'Média'

            if Inst.q8_ruim > Inst.q8_boa and Inst.q8_ruim > Inst.q8_media:
                line_of_interest.q8_resp = u'Ruim'
            if Inst.q8_boa > Inst.q8_ruim and Inst.q8_boa > Inst.q8_media:
                line_of_interest.q8_resp = u'Boa'
        else:
            line_of_interest.q8_resp = u''
            line_of_interest.q8_porc = 0

        if sums[8] != 0:
            line_of_interest.q9_resp = u'Sim'
            line_of_interest.q9_porc = int(100*(Inst.q9_sim/sums[8]))
            if Inst.q9_nao > Inst.q9_sim:
                line_of_interest.q9_resp = u'Não'
                line_of_interest.q9_porc = int(100*(Inst.q9_nao/sums[8]))
        else:
            line_of_interest.q9_resp = u''
            line_of_interest.q9_porc = 0

        if sums[9] != 0:
            line_of_interest.q10_resp = u'Sim'
            line_of_interest.q10_porc = int(100*(Inst.q10_sim/sums[9]))
            if (Inst.q10_nao) > (Inst.q10_sim):
                line_of_interest.q10_resp = u'Sim'
                line_of_interest.q10_porc = int(100*(Inst.q10_nao/sums[9]))
        else:
            line_of_interest.q10_resp = u''
            line_of_interest.q10_porc = 0

        if sums[10] != 0:
            line_of_interest.q11_resp = u'Sim'
            line_of_interest.q11_porc = int(100*(Inst.q11_sim/sums[10]))
            if Inst.q11_nao > Inst.q11_sim:
                line_of_interest.q11_resp = u'Não'
                line_of_interest.q11_porc = int(100*(Inst.q11_nao/sums[10]))
        else:
            line_of_interest.q11_resp = u''
            line_of_interest.q11_porc = 0

        if sums[11] != 0:
            line_of_interest.q12_resp = u'Sim'
            line_of_interest.q12_porc = int(100*(Inst.q12_sim/sums[11]))
            if Inst.q12_nao > Inst.q12_sim:
                line_of_interest.q12_resp = u'Não'
                line_of_interest.q12_porc = int(100*(Inst.q12_nao/sums[11]))
        else:
            line_of_interest.q12_resp = u''
            line_of_interest.q12_porc = 0

        if sums[12] != 0:
            line_of_interest.q13_resp = u'Sim'
            line_of_interest.q13_porc = int(100*(Inst.q13_sim/sums[12]))
            if Inst.q13_nao > Inst.q13_sim:
                line_of_interest.q13_resp = u'Não'
                line_of_interest.q13_porc = int(100*(Inst.q13_nao/sums[12]))
        else:
            line_of_interest.q13_resp = u''
            line_of_interest.q13_porc = 0

        S.commit()

#receive the AnswerSum line and update the OfferingDisplay table of that offering
    def UpdateSubjectDisplay(Inst):

        LocDB = create_engine(UserDB, echo=False)
        S = sessionmaker(bind=LocDB)()

        sums = []

        for var in range(0,13):
            sums.append(var)

        sums[0] = (Inst.q1_sim + Inst.q1_nao)
        sums[2] = (Inst.q3_curta + Inst.q3_longa + Inst.q3_adequada)
        sums[3] = Inst.q4_alta + Inst.q4_baixa + Inst.q4_normal
        sums[4] = Inst.q5_dificil + Inst.q5_normal + Inst.q5_facil


        line_of_interest = S.query(SubjectDisplay).filter(Inst.subject_id == SubjectDisplay.subject_id).one()

        if sums[0] != 0:
            line_of_interest.q1_resp = u'Sim'
            line_of_interest.q1_porc = int(100*(Inst.q1_sim/sums[0]))
            if Inst.q1_nao > Inst.q1_sim:
                line_of_interest.q1_resp = u'Não'
                line_of_interest.q1_porc = int(100*(Inst.q1_nao/sums[0]))
        else:
            line_of_interest.q1_resp = u''
            line_of_interest.q1_porc = 0

        if sums[2] != 0:
            line_of_interest.q3_porc = int(100*((max(Inst.q3_curta, Inst.q3_longa, Inst.q3_adequada))/sums[2]))
            line_of_interest.q3_resp = u'Adequada'

            if Inst.q3_curta > Inst.q3_longa and Inst.q3_curta > Inst.q3_adequada:
                line_of_interest.q3_resp = u'Curta'
            if Inst.q3_longa > Inst.q3_curta and Inst.q3_longa > Inst.q3_adequada:
                line_of_interest.q3_resp = u'Longa'
        else:
            line_of_interest.q3_resp = u''
            line_of_interest.q3_porc = 0

        if sums[3] != 0:
            line_of_interest.q4_porc = int(100*(max(Inst.q4_alta, Inst.q4_normal, Inst.q4_baixa))/sums[3])
            line_of_interest.q4_resp = u'Normal'

            if Inst.q4_baixa > Inst.q4_alta and Inst.q4_baixa > Inst.q4_normal:
                line_of_interest.q4_resp = u'Baixa'
            if Inst.q4_alta > Inst.q4_baixa and Inst.q4_alta > Inst.q4_normal:
                line_of_interest.q4_resp = u'Alta'
        else:
            line_of_interest.q4_resp = u''
            line_of_interest.q4_porc = 0

        if sums[4] != 0:
            line_of_interest.q5_porc = int(100*(max(Inst.q5_dificil, Inst.q5_normal, Inst.q5_facil))/sums[4])
            line_of_interest.q5_resp = u'Normal'

            if Inst.q5_facil > Inst.q5_dificil and Inst.q5_facil > Inst.q5_normal:
                line_of_interest.q5_resp = u'Fácil'
            if Inst.q5_dificil > Inst.q5_facil and Inst.q5_dificil > Inst.q5_normal:
                line_of_interest.q5_resp = u'Difícil'
        else:
            line_of_interest.q5_resp = u''
            line_of_interest.q5_porc = 0

        S.commit()


#recebe uma linha de AnswerSumTeacher e atualiza a tabela TeacherDisplay
    def UpdateTeacherDisplay(Inst):

        LocDB = create_engine(UserDB, echo=False)
        S = sessionmaker(bind=LocDB)()

        sums = []

        for var in range(0,13):
            sums.append(var)

        sums[5] = Inst.q6_dificil + Inst.q6_normal + Inst.q6_facil
        sums[6] = Inst.q7_sim + Inst.q7_nao
        sums[7] = Inst.q8_boa + Inst.q8_media + Inst.q8_ruim
        sums[8] = Inst.q9_sim + Inst.q9_nao
        sums[9] = Inst.q10_sim + Inst.q10_nao
        sums[10] = Inst.q11_sim + Inst.q11_nao
        sums[11] = Inst.q12_sim + Inst.q12_nao
        sums[12] = Inst.q13_sim + Inst.q13_nao

        line_of_interest = S.query(TeacherDisplay).filter(Inst.teacher_id == TeacherDisplay.teacher_id).one()

        if sums[5] != 0:
            line_of_interest.q6_porc = int(100*(max(Inst.q6_dificil, Inst.q6_normal, Inst.q6_facil))/sums[5])
            line_of_interest.q6_resp = u'Normal'

            if Inst.q6_facil > Inst.q6_dificil and Inst.q6_facil > Inst.q6_normal:
                line_of_interest.q6_resp = u'Fácil'
            if Inst.q6_dificil > Inst.q6_facil and Inst.q6_dificil > Inst.q6_normal:
                line_of_interest.q6_resp = u'Difícil'
        else:
            line_of_interest.q6_resp = u''
            line_of_interest.q6_porc = 0

        if sums[6] != 0:
            line_of_interest.q7_resp = u'Sim'
            line_of_interest.q7_porc = int(100*(Inst.q7_sim/sums[6]))
            if Inst.q7_nao > Inst.q7_sim:
                line_of_interest.q7_resp = u'Não'
                line_of_interest.q7_porc = int(100*(Inst.q7_nao/sums[6]))
        else:
            line_of_interest.q7_resp = u''
            line_of_interest.q7_porc = 0

        if sums[7] != 0:
            line_of_interest.q8_porc = int(100*(max(Inst.q8_boa, Inst.q8_media, Inst.q8_ruim))/sums[7])
            line_of_interest.q8_resp = u'Média'

            if Inst.q8_ruim > Inst.q8_boa and Inst.q8_ruim > Inst.q8_media:
                line_of_interest.q8_resp = u'Ruim'
            if Inst.q8_boa > Inst.q8_ruim and Inst.q8_boa > Inst.q8_media:
                line_of_interest.q8_resp = u'Boa'
        else:
            line_of_interest.q8_resp = u''
            line_of_interest.q8_porc = 0

        if sums[8] != 0:
            line_of_interest.q9_resp = u'Sim'
            line_of_interest.q9_porc = int(100*(Inst.q9_sim/sums[8]))
            if Inst.q9_nao > Inst.q9_sim:
                line_of_interest.q9_resp = u'Não'
                line_of_interest.q9_porc = int(100*(Inst.q9_nao/sums[8]))
        else:
            line_of_interest.q9_resp = u''
            line_of_interest.q9_porc = 0

        if sums[9] != 0:
            line_of_interest.q10_resp = u'Sim'
            line_of_interest.q10_porc = int(100*(Inst.q10_sim/sums[9]))
            if (Inst.q10_nao) > (Inst.q10_sim):
                line_of_interest.q10_resp = u'Sim'
                line_of_interest.q10_porc = int(100*(Inst.q10_nao/sums[9]))
        else:
            line_of_interest.q10_resp = u''
            line_of_interest.q10_porc = 0

        if sums[10] != 0:
            line_of_interest.q11_resp = u'Sim'
            line_of_interest.q11_porc = int(100*(Inst.q11_sim/sums[10]))
            if Inst.q11_nao > Inst.q11_sim:
                line_of_interest.q11_resp = u'Não'
                line_of_interest.q11_porc = int(100*(Inst.q11_nao/sums[10]))
        else:
            line_of_interest.q11_resp = u''
            line_of_interest.q11_porc = 0

        if sums[11] != 0:
            line_of_interest.q12_resp = u'Sim'
            line_of_interest.q12_porc = int(100*(Inst.q12_sim/sums[11]))
            if Inst.q12_nao > Inst.q12_sim:
                line_of_interest.q12_resp = u'Não'
                line_of_interest.q12_porc = int(100*(Inst.q12_nao/sums[11]))
        else:
            line_of_interest.q12_resp = u''
            line_of_interest.q12_porc = 0

        if sums[12] != 0:
            line_of_interest.q13_resp = u'Sim'
            line_of_interest.q13_porc = int(100*(Inst.q13_sim/sums[12]))
            if Inst.q13_nao > Inst.q13_sim:
                line_of_interest.q13_resp = u'Não'
                line_of_interest.q13_porc = int(100*(Inst.q13_nao/sums[12]))
        else:
            line_of_interest.q13_resp = u''
            line_of_interest.q13_porc = 0

        S.commit()


    def CreateLineAnswerSumTeacher(Inst):
        LocDB = create_engine(UserDB, echo=False)
        LocS = sessionmaker(bind=LocDB)()

        LocTeacher = LocS.query(Teacher).filter(
            Teacher.id == Inst.id).one()

        NewAnswerSumTeacher = AnswerSumTeacher(
        teacher = LocTeacher,
        q6_dificil = 0,
        q6_normal = 0,
        q6_facil = 0,
        q7_sim = 0,
        q7_nao = 0,
        q8_boa = 0,
        q8_media = 0,
        q8_ruim = 0,
        q9_sim = 0,
        q9_nao = 0,
        q10_sim = 0,
        q11_sim = 0,
        q10_nao = 0,
        q11_nao = 0,
        q12_sim = 0,
        q12_nao = 0,
        q13_sim = 0,
        q13_nao = 0
        )
        LocS.add(NewAnswerSumTeacher)
        LocS.commit()

    def CreateLineTeacherDisplay(Inst):
        LocDB = create_engine(UserDB, echo=False)
        LocS = sessionmaker(bind=LocDB)()

        LocTeacher = LocS.query(Teacher).filter(
            Teacher.id == Inst.id).one()

        NewTeacherDisplay = TeacherDisplay(
        q6_resp = u'',
        q6_porc = 0,
        q7_resp = u'',
        q7_porc = 0,
        q8_resp = u'',
        q8_porc = 0,
        q9_resp = u'',
        q9_porc = 0,
        q10_resp = u'',
        q10_porc = 0,
        q11_resp = u'',
        q11_porc = 0,
        q12_resp = u'',
        q12_porc = 0,
        q13_resp = u'',
        q13_porc = 0,
        teacher = LocTeacher
        )
        LocS.add(NewTeacherDisplay)
        LocS.commit()

    def CreateLineSubjectDisplay(Inst):
        LocDB = create_engine(UserDB, echo=False)
        LocS = sessionmaker(bind=LocDB)()

        LocSubject = LocS.query(Subject).filter(
            Subject.id == Inst.id).one()

        NewSubjectDisplay = SubjectDisplay(
            q1_resp = u'',
            q1_porc = 0,
            q2_resp = u'',
            q2_porc = 0,
            q3_resp = u'',
            q3_porc = 0,
            q4_resp = u'',
            q4_porc = 0,
            q5_resp = u'',
            q5_porc =  0,
            subject = LocSubject
        )
        LocS.add(NewSubjectDisplay)
        LocS.commit()


    def CreateLineAnswerSumSubject(Inst):
        LocDB = create_engine(UserDB, echo=False)
        LocS = sessionmaker(bind=LocDB)()

        LocSubject = LocS.query(Subject).filter(
            Subject.id == Inst.id).one()

        NewAnswerSumSubject = AnswerSumSubject(
            subject = LocSubject,
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
            q5_dificil = 0,
            q5_normal = 0,
            q5_facil = 0
        )
        LocS.add(NewAnswerSumSubject)
        LocS.commit()


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

                StudentCall = S.query(Student).filter(
                    Student.ra == Form['ra'].value)
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

                if StudentCall.count():
                    StudentCall = StudentCall.one()
                    UserCall = S.query(User).filter(StudentCall.id == User.student_id).one()
                    if UserCall.password == Form['senha'].value:
                        Session.user_id = UserCall.id
                        if UserCall.confirmed == 1:
                            raise web.seeother('/')
                        else:
                            raise web.seeother('/confirmacao')
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

                check_email = re.search(r'[\w.-]+@[\w.-]+.unicamp.br', Form['E-mail'].value)

                check_RA = re.search(r'[\d]', Form['RA'].value)

                match_email = S.query(User).filter(
                    User.email == Form['E-mail'].value)

                match_ra = S.query(Student).filter(
                    Student.ra == Form['RA'].value)


                if check_email == None:
                    return Render.register(Form,"E-mail inválido! Favor utilizar um E-mail [.unicamp.br]. Por exemplo, o email da DAC no formato a123456@dac.unicamp.br", Render)

                elif check_RA == None:
                    return Render.register(Form,"RA inválido!", Render)

                elif match_email.count() != 0 or match_ra.count() != 0:
                    return Render.register(Form,"Usuário já está cadastrado!", Render)

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
                confirmed = False,
                student = StudentCall
                )

                S.add(NewUser)
                S.commit()

                # Adding confirmation key to table of confirmations
                caracters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                conf_code = ''
                for char in xrange(8):
                        conf_code += choice(caracters)

                web.sendmail('gda.noreply@gmail.com', Form['E-mail'].value, 'Confirmar E-mail - GDA', 'O código de confirmação gerado para seu e-mail foi: '+
                conf_code+'\n \n Para proceder com a confirmação de sua conta e poder avaliar oferecimentos, clique no link abaixo:\n\n faraj7.pythonanywhere.com/')

                NewConfirm = ConfirmationRoll(
                    user = NewUser,
                    activation_code = conf_code
                )
                S.add(NewConfirm)
                S.commit()


                UserCall = S.query(User).filter(
                    User.email == Form['E-mail'].value).one()

                Map(StudentPage, NewStudent.EncodeURL(), dict(StudentInst=NewStudent))

                Session.user_id = UserCall.id
                raise web.seeother('/confirmacao')


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

    class ConfirmationPage:

        def GET(self):
            IsLogged()
            Form = ConfirmationForm
            return Render.confirmationpage(Form, "", Render)

        def POST(self):
            Form = ConfirmationForm
            auxiliar = POSTParse(web.data())

            S = sessionmaker(bind=DB)()
            LocDB = create_engine(UserDB, echo=False)

            if auxiliar.has_key('confirmar'):
                cont = 0
                for Line in S.query(ConfirmationRoll):
                    if auxiliar['conf_code'] == Line.activation_code and Session.user_id == Line.user_id:
                        LocDB.execute(update(User).where(User.id == Line.user_id).values(confirmed=1))
                        LocDB.execute(delete(ConfirmationRoll).where(ConfirmationRoll.id == Line.id))
                        cont = 1
                if cont == 0:
                    return Render.confirmationpage(Form, "Código de confirmação incorreto", Render)
                else:
                    raise web.seeother('/login')
            elif auxiliar.has_key('alterar'):
                check_email = re.search(r'[\w.-]+@[\w.-]+.unicamp.br', auxiliar['email'])

                if check_email == None:
                    return Render.confirmationpage(Form,"E-mail inválido! Favor utilizar um E-mail [.unicamp.br]. Por exemplo, o email da DAC no formato a123456@dac.unicamp.br", Render)
                else:
                    LocDB.execute(update(User).where(User.id == Session.user_id).values(email=auxiliar['email']))
                    conf_code = S.query(ConfirmationRoll).filter(ConfirmationRoll.user_id == Session.user_id).one()
                    adress = S.query(User).filter(User.id == Session.user_id).one()

                    web.sendmail('gda.noreply@gmail.com', str(adress.email) , 'Confirmar E-mail - GDA', 'O código de confirmação gerado para seu e-mail foi: '+
                    str(conf_code.activation_code)+'\n \n Para proceder com a confirmação de sua conta e poder avaliar oferecimentos, clique no link abaixo:\n\n faraj7.pythonanywhere.com/')
                    return Render.confirmationpage(Form,"E-mail alterado com sucesso! Verifique o novo endereço para ativação do registro do GDA", Render)

            elif auxiliar.has_key('reenviar'):
                conf_code = S.query(ConfirmationRoll).filter(ConfirmationRoll.user_id == Session.user_id).one()
                adress = S.query(User).filter(User.id == Session.user_id).one()

                web.sendmail('gda.noreply@gmail.com', str(adress.email) , 'Confirmar E-mail - GDA', 'O código de confirmação gerado para seu e-mail foi: '+
                str(conf_code.activation_code)+'\n \n Para proceder com a confirmação de sua conta e poder avaliar oferecimentos, clique no link abaixo:\n\n faraj7.pythonanywhere.com/')
                return Render.confirmationpage(Form,"E-mail reenviado!", Render)

    class StudentPage:
        StudentInst = Student()

        def GET(self):
            IsLogged()
            IsConfirmed()
            return Render.studentpage(self.StudentInst, Render)

    class TeacherPage:
        TeacherInst = Teacher()

        def GET(self):
            IsLogged()
            IsConfirmed()

            LocDB = create_engine(UserDB, echo=False)
            LocS = sessionmaker(bind=LocDB)()

            if (LocS.query(AnswerSumTeacher).filter(self.TeacherInst.id == AnswerSumTeacher.teacher_id).count())==0:
                CreateLineAnswerSumTeacher(self.TeacherInst)
            if (LocS.query(TeacherDisplay).filter(self.TeacherInst.id == TeacherDisplay.teacher_id).count())==0:
                CreateLineTeacherDisplay(self.TeacherInst)


            return Render.teacherpage(self.TeacherInst, Render)

        def POST(self):
            IsLogged()
            IsConfirmed()
            Response = POSTParse(web.data())
#            CommitComment(self.TeacherInst, Response)

            return Render.teacherpage(self.TeacherInst, Render)

    class SubjectPage:
        SubjectInst = Subject()

        def GET(self):
            IsLogged()
            IsConfirmed()
            return Render.subjectpage(self.SubjectInst, Render)

        def POST(self):
            IsLogged()
            IsConfirmed()
            Response = POSTParse(web.data())
#            CommitComment(self.SubjectInst, Response)

            return Render.subjectpage(self.SubjectInst, Render)

    class OfferingPage:
        OfferingInst = Offering()

        def GET(self):
            IsLogged()
            IsConfirmed()
            form = RateOffering()

            already_evaluated = False
            LocDB = create_engine(UserDB, echo=False)
            LocS = sessionmaker(bind=LocDB)()
            manobra = LocS.query(StudentRate).filter(
                StudentRate.user_id == Session.user_id).filter(
                StudentRate.offering_id == self.OfferingInst.id)

            LocOffering = LocS.query(Offering).filter(
                Offering.id == self.OfferingInst.id).one()

            if manobra.count() != 0:
                already_evaluated = True

            #modificar o template para usar a variável "already_evaluated" (By Raul)
            return Render.offeringpage(self.OfferingInst, Render, form, already_evaluated)

        def POST(self):
            IsLogged()
            IsConfirmed()
        #    Response = POSTParse(web.data())
#            CommitComment(self.OfferingInst, Response)
        #    form = RateOffering()
            #if not form.validates():
            #    return Render.database(Render,form1,form2)
            #else:
        #    form.validates()
        #    S = sessionmaker(bind=DB)()
        #    Rate = OfferingRate(
        #                    answers=form.d.Respostas,
        #                    offering_id= self.OfferingInst.id,
        #                    question1=form.d.Coluna11,
        #                    question2=form.d.Coluna12,
        #                    question3=form.d.Coluna13,
        #                    question4=form.d.Coluna14,
        #                    question5=form.d.Coluna15,
        #                    question6=form.d.Coluna16)
        #    S.add(Rate)
        #    S.commit()
            #return self.OfferingInst.id

            #deixar as duas linhas abaixo apenas quando formos inserir novas avaliações oficiais
            semestre = S.query(Semester).filter(Semester.id == self.OfferingInst.semester_id).one()
            return web.seeother(semestre.EncodeURL())

            # deixar a parte de baixo no curso normal do site
            #return Render.offeringpage(self.OfferingInst, Render,form, False)



    # TODO Unfinished
    '''
    class UploadHandler:
        def GET(self):
                web.header("Content-Type", "text/html; charset=utf-8")
                return
    <html><head></head><body>
    <form method="POST" enctype="multipart/form-data" action="">
    <input type="file" name="myfile" />
    <br/>
    <input type="submit" />
    </form>
    </body></html>


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
#            IsConfirmed()
#            return Render.offeringpage(self.OfferingInst, Render)

#        def POST(self):
#            IsLogged()
#            Response = POSTParse(web.data())
#            CommitComment(self.OfferingInst, Response)
#
#            return Render.offeringpage(self.OfferingInst, Render)
#
#
'''
    class SearchTeacher:
        def GET(self):
            IsLogged()
            IsConfirmed()

            return Render.searchteacher(Render)

    class SearchSubject:
        def GET(self):
            IsLogged()
            IsConfirmed()

            return Render.searchsubject(Render)

    class SearchOffering:
        def GET(self):
            IsLogged()
            IsConfirmed()

            return Render.searchoffering(Render)

    class EvaluatePage:
        OfferingInst = Offering()

        def GET(self):
            IsLogged()
            IsConfirmed()

            return Render.evaluatepage(self.OfferingInst, Render)

        def POST(self):
            IsLogged()
            IsConfirmed()
            auxiliar = POSTParse(web.data())

            LocDB = create_engine(UserDB, echo=False)
            LocS = sessionmaker(bind=LocDB)()

            already_evaluated = LocS.query(StudentRate).filter(
                StudentRate.user_id == Session.user_id).filter(
                StudentRate.offering_id == self.OfferingInst.id).count()

            if already_evaluated:
                IsLogged()
                IsConfirmed()
                return Render.evaluatepage(self.OfferingInst, Render)

            else:
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

                elemento = LocS.query(AnswerSum).filter(AnswerSum.offering_id == self.OfferingInst.id).one()
                professor = LocS.query(AnswerSumTeacher).filter(AnswerSumTeacher.teacher_id == self.OfferingInst.teacher_id).one()
                disciplina = LocS.query(AnswerSumSubject).filter(AnswerSumSubject.subject_id == self.OfferingInst.subject_id).one()

                if auxiliar['0.0'] == u' sim ':
                    elemento.q1_sim += 1
                    disciplina.q1_sim += 1
                elif auxiliar['0.0'] == u' não ':
                    elemento.q1_nao += 1
                    disciplina.q1_nao += 1

                if auxiliar['1.0'] == u' correto ':
                    elemento.q2_correto += 1
                elif auxiliar['1.0'] == u' antes ':
                    elemento.q2_antes += 1
                elif auxiliar['1.0'] == u' depois ':
                    elemento.q2_depois += 1

                if auxiliar['2.0'] == u' adequada ':
                    elemento.q3_adequada += 1
                    disciplina.q3_adequada += 1
                elif auxiliar['2.0'] == u' curta ':
                    elemento.q3_curta += 1
                    disciplina.q3_curta += 1
                elif auxiliar['2.0'] == u' longa ':
                    elemento.q3_longa += 1
                    disciplina.q3_longa += 1

                if auxiliar['3.0'] == u' alta ':
                    elemento.q4_alta += 1
                    disciplina.q4_alta += 1
                elif auxiliar['3.0'] == u' normal ':
                    elemento.q4_normal += 1
                    disciplina.q4_normal += 1
                elif auxiliar['3.0'] == u' baixa ':
                    elemento.q4_baixa += 1
                    disciplina.q4_baixa += 1

                if auxiliar['4.0'] == u' dificil ':
                    elemento.q5_dificil += 1
                    disciplina.q5_dificil += 1
                elif auxiliar['4.0'] == u' normal ':
                    elemento.q5_normal += 1
                    disciplina.q5_normal += 1
                elif auxiliar['4.0'] == u' facil ':
                    elemento.q5_facil += 1
                    disciplina.q5_facil += 1

                if auxiliar['5.0'] == u' dificil ':
                    elemento.q6_dificil += 1
                    professor.q6_dificil += 1
                elif auxiliar['5.0'] == u' normal ':
                    elemento.q6_normal += 1
                    professor.q6_normal += 1
                elif auxiliar['5.0'] == u' facil ':
                    elemento.q6_facil += 1
                    professor.q6_facil += 1

                if auxiliar['6.0'] == u' sim ':
                    elemento.q7_sim += 1
                    professor.q7_sim += 1
                elif auxiliar['6.0'] == u' não ':
                    elemento.q7_nao += 1
                    professor.q7_nao += 1

                if auxiliar['7.0'] == u' boa ':
                    elemento.q8_boa += 1
                    professor.q8_boa += 1
                elif auxiliar['7.0'] == u' média ':
                    elemento.q8_media += 1
                    professor.q8_media += 1
                elif auxiliar['7.0'] == u' ruim ':
                    elemento.q8_ruim += 1
                    professor.q8_ruim += 1

                if auxiliar['8.0'] == u' sim ':
                    elemento.q9_sim += 1
                    professor.q9_sim += 1
                elif auxiliar['8.0'] == u' não ':
                    elemento.q9_nao += 1
                    professor.q9_nao += 1

                if auxiliar['9.0'] == u' sim ':
                    elemento.q10_sim += 1
                    professor.q10_sim += 1
                elif auxiliar['9.0'] == u' não ':
                    elemento.q10_nao += 1
                    professor.q10_nao += 1

                if auxiliar['10.0'] == u' sim ':
                    elemento.q11_sim += 1
                    professor.q11_sim += 1
                elif auxiliar['10.0'] == u' não ':
                    elemento.q11_nao += 1
                    professor.q11_nao += 1

                if auxiliar['11.0'] == u' sim ':
                    elemento.q12_sim += 1
                    professor.q12_sim += 1
                elif auxiliar['11.0'] == u' não ':
                    elemento.q12_nao += 1
                    professor.q12_nao += 1

                if auxiliar['12.0'] == u' sim ':
                    elemento.q13_sim += 1
                    professor.q13_sim += 1
                elif auxiliar['12.0'] == u' não ':
                    elemento.q13_nao += 1
                    professor.q13_nao += 1

                LocS.commit()

                UpdateOfferingDisplay(elemento)
                UpdateTeacherDisplay(professor)
                UpdateSubjectDisplay(disciplina)

                raise web.seeother(self.OfferingInst.EncodeURL())
    #            try:
    #
    #
    #            except:
    #                LocS.rollback()
    #                return True

    '''
    class FaqPage:
        def GET(self):
            IsLogged()
            IsConfirmed()

            return Render.faq(Render)


            LocDB = create_engine(UserDB, echo=False)
            S = sessionmaker(bind=LocDB)()

            for Line in S.query(Subject):
                if (S.query(AnswerSumSubject).filter(Line.id == AnswerSumSubject.subject_id).count())==0:
                    CreateLineAnswerSumSubject(Line)
                if (S.query(SubjectDisplay).filter(Line.id == SubjectDisplay.subject_id).count())==0:
                    CreateLineSubjectDisplay(Line)

            for Line in S.query(Teacher):
                if (S.query(AnswerSumTeacher).filter(Line.id == AnswerSumTeacher.teacher_id).count())==0:
                    CreateLineAnswerSumTeacher(Line)
                if (S.query(TeacherDisplay).filter(Line.id == TeacherDisplay.teacher_id).count())==0:
                    CreateLineTeacherDisplay(Line)

            for Line in S.query(Offering):
                if ((S.query(OfferingDisplay).filter(OfferingDisplay.offering_id == Line.id)).count()) == 0:
                    LocOffering = S.query(Offering).filter(
                        Offering.id == Line.id).one()
                    NewDisplay=OfferingDisplay(
                    q1_resp = u'',
                    q1_porc = 0,
                    q2_resp = u'',
                    q2_porc = 0,
                    q3_resp = u'',
                    q3_porc = 0,
                    q4_resp = u'',
                    q4_porc = 0,
                    q5_resp = u'',
                    q5_porc = 0,
                    q6_resp = u'',
                    q6_porc = 0,
                    q7_resp = u'',
                    q7_porc = 0,
                    q8_resp = u'',
                    q8_porc = 0,
                    q9_resp = u'',
                    q9_porc = 0,
                    q10_resp = u'',
                    q10_porc = 0,
                    q11_resp = u'',
                    q11_porc = 0,
                    q12_resp = u'',
                    q12_porc = 0,
                    q13_resp = u'',
                    q13_porc = 0,
                    offering = LocOffering
                    )

                    S.add(NewDisplay)
                    S.commit()

                if (S.query(AnswerSum.offering_id).filter(AnswerSum.offering_id == Line.id).count())==0:
                    LocOffering = S.query(Offering).filter(
                        Offering.id == Line.id).one()
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
                    q5_dificil = 0,
                    q5_normal = 0,
                    q5_facil = 0,
                    q6_dificil = 0,
                    q6_normal = 0,
                    q6_facil = 0,
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
                    S.add(NewSum)
                    S.commit()
                '''

    class IndexPage:
        def GET(self):
            IsLogged()
            IsConfirmed()
            return Render.index(Render)

#    class ContactPage:
#        def GET(self):
#            IsLogged()
#            return Render.contact(Render)

    class AboutPage:
        def GET(self):
            IsLogged()
            IsConfirmed()
            return Render.about(Render)

    class StatsPage:
        def GET(self):
            IsLogged()
            IsConfirmed()
            return Render.stats(Render)

    class SemesterPage:
        SemesterInst = Semester()

        def GET(self):
            IsLogged()
            IsConfirmed()
            return Render.semesterpage(self.SemesterInst, Render)

    class ForgottenPassword:
        def GET(self):
            Form = ForgottenForm
            return Render.forgottenpassword(Form, "", Render)

        def POST(self):
            auxiliar = POSTParse(web.data())
            Form = ForgottenForm

            S = sessionmaker(bind=DB)()
            LocDB = create_engine(UserDB, echo=False)

            if S.query(User).filter(auxiliar['email'] == User.email).count() == 1:
                caracters = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
                newpass = ''
                for char in xrange(8):
                        newpass += choice(caracters)

                web.sendmail('gda.noreply@gmail.com', auxiliar['email'], 'Recuperar Senha - GDA', 'Sua nova senha é: '+
                newpass+'\n \n Caso ache necessário, você pode mudar sua senha na página de alteração de dados cadatrais do GDA.')

                stmt = update(User).where(auxiliar['email'] == User.email).values(password=newpass)
                LocDB.execute(stmt)

            else:
                return Render.forgottenpassword(Form, "Não existe usuário cadastrado com o e-mail fornecido", Render)
    '''
    class Database:
        def GET(self):
            IsLogged()
            IsConfirmed()
            UpdateLists()
            form1 = AddSemester()
            form2 = AddOffering()
            form3 = AddTeacher()
            form4 = AddSubject()
            # make sure you create a copy of the form by calling it (line above)
            # Otherwise changes will appear globally
            return Render.database(Render,form1, form2, form3, form4)

        def POST(self):
            form1 = AddSemester()
            form2 = AddOffering()
            form3 = AddTeacher()
            form4 = AddSubject()

            S = sessionmaker(bind=DB)()

            if form1.validates():
                Sem = Semester(
                    year = form1.d.Ano,
                    sem = form1.d.Semestre[0]
                )
                S.add(Sem)
                S.commit()

            elif form2.validates():
                Off = Offering(subject_id=form2.d.Disciplina,
                                teacher_id=form2.d.Professor,
                                semester_id=form2.d.Semestre,
                                students = int(form2.d.Matriculados),
                                code = form2.d.Turma)
                S.add(Off)
                S.commit()

                Offnovelty = S.query(Offering).filter(Offering.id == Off.id).one()

                if ((S.query(OfferingDisplay).filter(OfferingDisplay.offering_id == Offnovelty.id)).count()) == 0:
                    LocOffering = S.query(Offering).filter(
                        Offering.id == Offnovelty.id).one()
                    NewDisplay=OfferingDisplay(
                    q1_resp = u'',
                    q1_porc = 0,
                    q2_resp = u'',
                    q2_porc = 0,
                    q3_resp = u'',
                    q3_porc = 0,
                    q4_resp = u'',
                    q4_porc = 0,
                    q5_resp = u'',
                    q5_porc = 0,
                    q6_resp = u'',
                    q6_porc = 0,
                    q7_resp = u'',
                    q7_porc = 0,
                    q8_resp = u'',
                    q8_porc = 0,
                    q9_resp = u'',
                    q9_porc = 0,
                    q10_resp = u'',
                    q10_porc = 0,
                    q11_resp = u'',
                    q11_porc = 0,
                    q12_resp = u'',
                    q12_porc = 0,
                    q13_resp = u'',
                    q13_porc = 0,
                    offering = LocOffering
                    )

                    S.add(NewDisplay)
                    S.commit()

                if (S.query(AnswerSum).filter(AnswerSum.offering_id == Offnovelty.id).count())==0:
                    LocOffering = S.query(Offering).filter(
                        Offering.id == Offnovelty.id).one()
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
                    q5_dificil = 0,
                    q5_normal = 0,
                    q5_facil = 0,
                    q6_dificil = 0,
                    q6_normal = 0,
                    q6_facil = 0,
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
                    S.add(NewSum)
                    S.commit()

            elif form4.validates():
                Subj = Subject(
                    code = form4.d.Codigo,
                    name = form4.d.Nome,
                    credits = int(form4.d.Creditos),
                    summary = form4.d.Ementa
                )
                S.add(Subj)
                S.commit()

                Subjnovelty = S.query(Subject).filter(Subject.id == Subj.id).one()

                if (S.query(AnswerSumSubject).filter(Subjnovelty.id == AnswerSumSubject.subject_id).count())==0:
                    CreateLineAnswerSumSubject(Subjnovelty)
                if (S.query(SubjectDisplay).filter(Subjnovelty.id == SubjectDisplay.subject_id).count())==0:
                    CreateLineSubjectDisplay(Subjnovelty)

            elif form3.validates():
                Teac = Teacher(
                    name = form3.d.Nome
                )
                S.add(Teac)
                S.commit()

                Teachernovelty = S.query(Teacher).filter(Teacher.id == Teac.id).one()

                if (S.query(AnswerSumTeacher).filter(Teachernovelty.id == AnswerSumTeacher.teacher_id).count())==0:
                    CreateLineAnswerSumTeacher(Teachernovelty)
                if (S.query(TeacherDisplay).filter(Teachernovelty.id == TeacherDisplay.teacher_id).count())==0:
                    CreateLineTeacherDisplay(Teachernovelty)

            raise web.seeother('/database')
            '''

    # URL Mappings
    S = sessionmaker(bind=DB)()

    Map(IndexPage, "/")
    Map(AboutPage, "/sobre")
    Map(StatsPage, "/estatisticas")
    Map(LoginPage, "/login")
    Map(RegisterPage, "/registrar")
    Map(LogoutPage, "/logout")
    Map(SearchTeacher, "/docentes")
    Map(SearchSubject, "/disciplinas")
    Map(SearchOffering, "/oferecimentos")
    Map(ForgottenPassword, "/esqueci")
    Map(ConfirmationPage, "/confirmacao")

    #Map(ContactPage, "/contato")
    #Map(FaqPage, "/faq")
    #Map(Database, "/database")
    #Map(UploadHandler, "/upload")

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
