from constants import *
from operator import itemgetter
import web
import os
import codecs
import urllib
from models import *

# Form Handlers
LoginForm = web.form.Form(
    web.form.Textbox('ra', web.form.notnull, Class="form-control"),
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

ForgottenForm = web.form.Form(
    web.form.Textbox('email', web.form.notnull, Class="form-control"),
    web.form.Button('Enviar', Class="btn btn-primary"),
)

ConfirmationForm = web.form.Form(
    web.form.Textbox('Codigo de confirmacao', web.form.notnull, Class="form-control"),
    web.form.Button('Submeter', Class="btn btn-primary"),
)

UserForm = web.form.Form(
    web.form.Textbox('RA', web.form.notnull, Class="form-control"),
    web.form.Textbox('Nome', web.form.notnull, Class="form-control"),
    web.form.Password('Current', Class="form-control"),
    web.form.Password('New', Class="form-control"),
    web.form.Password('Repeat', Class="form-control"),
    web.form.Button('Login', Class="btn btn-primary"),
)


semesters = []
teachers = []
subjects = []

def UpdateLists():
    S = sessionmaker(bind=DB)()

    SemestersList = S.query(Semester).order_by(Semester.id)
    TeachersList = S.query(Teacher).order_by(Teacher.name)
    SubjectsList = S.query(Subject).order_by(Subject.code)

    for Line in SemestersList:
        sem = '%s semestre de %s' % (Line.sem, Line.year)
        if (Line.id,sem) not in semesters:
            semesters.insert(-1,(Line.id,sem))

    for Line in TeachersList:
        t = '%s' % (Line.name)
        if (Line.id,t) not in teachers:
            teachers.insert(-1,(Line.id,t))

    for Line in SubjectsList:
        sub = '%s %s' % (Line.code, Line.name)
        if (Line.id,sub) not in subjects:
            subjects.insert(-1,(Line.id,sub))

    sorted(semesters, key=itemgetter(1))
    sorted(teachers, key=itemgetter(1))
    sorted(subjects, key=itemgetter(1))


DeleteTeacher = web.form.Form(
    web.form.Dropdown('Professores', args = teachers),
    web.form.Button('Submeter', Class="btn btn-primary"))

DeleteSemester = web.form.Form(
    web.form.Dropdown('id', args = semesters),
    web.form.Button('Submeter', Class="btn btn-primary"))

DeleteSubject = web.form.Form(
    web.form.Radio('id', args = subjects),
    web.form.Button('Submeter', Class="btn btn-primary"))

AddOffering = web.form.Form(
    web.form.Dropdown('Semestre', args = semesters),
    web.form.Dropdown('Disciplina', args = subjects),
    web.form.Dropdown('Professor', args = teachers),
    web.form.Textbox('Turma', web.form.notnull),
    web.form.Textbox('Matriculados', web.form.notnull),
    web.form.Button('Submeter', Class="btn btn-primary"))

AddSemester = web.form.Form(
    web.form.Dropdown('Semestre', [('1','primeiro'), ('2','segundo')]),
    web.form.Textbox('Ano', web.form.notnull),
    web.form.Button('Submeter', Class="btn btn-primary"))

AddTeacher = web.form.Form(
    web.form.Textbox('Nome', web.form.notnull),
    web.form.Button('Submeter', Class="btn btn-primary"))

AddSubject = web.form.Form(
    web.form.Textbox('Codigo', web.form.notnull),
    web.form.Textbox('Nome', web.form.notnull),
    web.form.Textbox('Creditos', web.form.notnull),
    web.form.Textbox('Ementa', web.form.notnull),
    web.form.Button('Submeter', Class="btn btn-primary"))

RateOffering = web.form.Form(
    web.form.Textbox('Respostas'),
    web.form.Textbox('Coluna11'),
    web.form.Textbox('Coluna12'),
    web.form.Textbox('Coluna13'),
    web.form.Textbox('Coluna14'),
    web.form.Textbox('Coluna15'),
    web.form.Textbox('Coluna16'),
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
