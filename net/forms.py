from constants import *

import web
import os
import codecs
import urllib
from models import *

# Form Handlers
LoginForm = web.form.Form(
    web.form.Textbox('email', web.form.notnull, Class="form-control"),
    web.form.Password('senha', web.form.notnull, Class="form-control"),
    web.form.Button('login', Class="btn btn-primary"),
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

S = sessionmaker(bind=DB)()

SemestersList = S.query(Semester) #.order_by(Offering.subject.code)
TeachersList = S.query(Teacher).order_by(Teacher.name)
SubjectsList = S.query(Subject).order_by(Subject.code)

semesters = []
for Line in SemestersList:
    sem = '%s semestre de %s' % (Line.sem, Line.year)
    semesters.insert(-1,(Line.id,sem))

teachers = []
for Line in TeachersList:
    t = '%s' % (Line.name)
    teachers.insert(-1,(Line.id,t))

subjects = []
for Line in SubjectsList:
    sub = '%s %s' % (Line.code, Line.name)
    subjects.insert(-1,(Line.id,sub))

AddSemester = web.form.Form(
    web.form.Dropdown('Semestre', [('1','primeiro'), ('2','segundo')]),
    web.form.Textbox("Ano", Class="form-control"),
    web.form.Button('Submeter', Class="btn btn-primary"))

AddTeacher = web.form.Form(
    web.form.Textbox('Nome'),
    web.form.Button('Submeter', Class="btn btn-primary"))

DeleteTeacher = web.form.Form(
    web.form.Dropdown('Professores', args = teachers),
    web.form.Button('Submeter', Class="btn btn-primary"))

DeleteSemester = web.form.Form(
    web.form.Dropdown('id', args = semesters),
    web.form.Button('Submeter', Class="btn btn-primary"))

DeleteSubject = web.form.Form(
    web.form.Radio('id', args = subjects),
    web.form.Button('Submeter', Class="btn btn-primary"))

#MyForm = web.form.Form(
    #form.Textbox("boe"),
    #form.Textbox("bax",
    #form.notnull,
    #form.regexp('\d+', 'Must be a digit'),
    #form.Validator('Must be more than 5', lambda x:int(x)>5)),
    #form.Textarea('moe'),
    #form.Checkbox('curly'),
    #web.form.Button('Submeter1', Class="btn btn-primary")),
