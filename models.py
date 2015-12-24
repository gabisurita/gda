#!/usr/env/python
#encoding:utf-8

""" GDA Website Database Models."""

from constants import *

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import desc

DB = create_engine(SystemDB, echo=False)
Base = declarative_base()


class Student(Base):
  __tablename__ = "student"

  id = Column('student_id', Integer, primary_key=True)
  ra = Column('ra', Integer)
  name  = Column('name',  String)

  def EncodeURL(self):
    return "/estudantes/%s" % str(self.ra).zfill(6)


class Teacher(Base):
  __tablename__ = "teacher"

  id = Column('teacher_id', Integer, primary_key=True)
  name = Column('name', String)

  def EncodeURL(self):
    return str("/docentes/%s" % self.name.lower().replace(" ","_").encode('utf8'))



class Subject(Base):
  __tablename__ = "subject"

  id = Column('subject_id', Integer, primary_key=True)
  code = Column('code', String(6), unique=True)
  name = Column('name', String)
  credits  = Column('credits', Integer)
  summary  = Column('summary', String)

  def EncodeURL(self):
    return "/disciplinas/%s" % str(self.code).lower()


class Requirement(Base):
  __tablename__ = "requirement"

  id = Column('requirement_id', Integer, primary_key=True)
  group = Column('group', Integer)
  subject_id = Column(Integer, ForeignKey('subject.subject_id'))
  subject = relationship(Subject)
  code = Column('code', String(6))


class Semester(Base):
  __tablename__ = "semester"

  id = Column('semester_id', Integer, primary_key=True)
  year = Column('year', Integer)
  sem  = Column('sem', Integer)

  def EncodeURL(self):
      return ("/oferecimentos/%ss%s/" % (
            str(self.sem),
            str(self.year)))



class Offering(Base):
  __tablename__ = "offering"

  id = Column('offering_id', Integer, primary_key=True)
  code = Column('code', String(8))
 # slots = Column('slots', Integer)
  students = Column('students', Integer)
  teacher_id = Column(Integer, ForeignKey('teacher.teacher_id'))
  subject_id = Column(Integer, ForeignKey('subject.subject_id'))
  semester_id = Column(Integer, ForeignKey('semester.semester_id'))
  teacher = relationship(Teacher)
  subject = relationship(Subject)
  semester = relationship(Semester)

  def EncodeURL(self):
    return ("/oferecimentos/%ss%s/%s%s" % (
        str(self.semester.sem),
        str(self.semester.year),
        str(self.subject.code),
        str(self.code))).lower()


  def EvaluationURL(self):
    return ("/avaliar/%ss%s/%s%s" % (
        str(self.semester.sem),
        str(self.semester.year),
        str(self.subject.code),
        str(self.code))).lower()




class Enrollment(Base):
  __tablename__ = "enrollment"

  id = Column('enrollment_id', Integer, primary_key=True)
  student_id = Column(Integer, ForeignKey('student.student_id'))
  offering_id = Column(Integer, ForeignKey('offering.offering_id'))
  student = relationship(Student)
  offering = relationship(Offering)


class Rating(Base):
  __tablename__ = "rating"

  id = Column('rating_id', Integer, primary_key=True)
  student_id = Column(Integer, ForeignKey('student.student_id'))
  offering_id = Column(Integer, ForeignKey('offering.offering_id'))
  student = relationship(Student)
  offering = relationship(Offering)


class User(Base):
  __tablename__ = "user"

  id = Column('user_id', Integer, primary_key=True)
  email = Column('email', String, unique=True)
  password = Column('password', String)
  confirmed = Column('confirmed', Boolean)
  student_id = Column(Integer, ForeignKey('student.student_id'))
  student = relationship(Student)


# TODO Add Timestamps

class TeacherComment(Base):
  __tablename__ = "teacher_comments"

  id = Column('teacher_comment_id', Integer, primary_key=True)
  text = Column('text', String)
  anonymous = Column('anonymous', Boolean)
  user_id = Column(Integer, ForeignKey('user.user_id'))
  user = relationship(User)
  teacher_id = Column(Integer, ForeignKey('teacher.teacher_id'))
  teacher = relationship(Teacher)
  offering_id = Column(Integer, ForeignKey('offering.offering_id'))
  offering = relationship(Offering)


class OfferingComment(Base):
  __tablename__ = "offering_comments"

  id = Column('offering_comment_id', Integer, primary_key=True)
  text = Column('text', String)
  anonymous = Column('anonymous', Boolean)
  user_id = Column(Integer, ForeignKey('user.user_id'))
  user = relationship(User)
  offering_id = Column(Integer, ForeignKey('offering.offering_id'))
  offering = relationship(Offering)


class SubjectComment(Base):
  __tablename__ = "subject_comments"

  id = Column('subject_comment_id', Integer, primary_key=True)
  text = Column('text', String)
  anonymous = Column('anonymous', Boolean)
  user_id = Column(Integer, ForeignKey('user.user_id'))
  user = relationship(User)
  subject_id = Column(Integer, ForeignKey('subject.subject_id'))
  subject = relationship(Subject)


# TODO Add type (w. mimes) and Offering/Teacher support

class FileUploads(Base):
  __tablename__ = "file_uploads"

  id = Column('upload_id', Integer, primary_key=True)
  filename = Column('filename', String)
  user_id = Column(Integer, ForeignKey('user.user_id'))
  user = relationship(User)
  subject_id = Column(Integer, ForeignKey('subject.subject_id'))
  subject = relationship(Subject)

class QuestionsOffering(Base):
    __tablename__ = "questions_offering"

    id = Column('question_id', Integer, primary_key=True)
    question = Column('question', String)

class QuestionsSubject(Base):
    __tablename__ = "questions_subject"

    id = Column('question_id', Integer, primary_key=True)
    question = Column('question', String)


class OfferingRate(Base):
  __tablename__ = "offering_rate"
  id = Column('rating_id', Integer, primary_key=True)
  offering_id = Column(Integer, ForeignKey('offering.offering_id'))
  offering = relationship(Offering)
  answers = Column('answers', Integer)
  question1 = Column('question1', Integer)
  question2 = Column('question2', Integer)
  question3 = Column('question3', Integer)
  question4 = Column('question4', Integer)
  question5 = Column('question5', Integer)
  question6 = Column('question6', Integer)

#Tabela contendo respostas cruas
class StudentRate(Base):
    __tablename__ = "studentrate"

    id = Column('studentrate_id', Integer, primary_key=True)
    offering_id = Column(Integer, ForeignKey('offering.offering_id'))
    user_id = Column(Integer, ForeignKey('user.user_id'))

    question1 = Column('question1', String)
    question2 = Column('question2', String)
    question3 = Column('question3', String)
    question4 = Column('question4', String)
    question5 = Column('question5', String)
    question6 = Column('question6', String)
    question7 = Column('question7', String)
    question8 = Column('question8', String)
    question9 = Column('question9', String)
    question10 = Column('question10', String)
    question11 = Column('question11', String)
    question12 = Column('question12', String)
    question13 = Column('question13', String)

    user = relationship(User)
    offering = relationship(Offering)

#Tabela que contém a soma das avaliações
class AnswerSum(Base):
    __tablename__ = "answersum"

    id = Column('answersum_id', Integer, primary_key=True)
    offering_id = Column(Integer, ForeignKey('offering.offering_id'))

    q1_sim = Column('q1_sim', Integer)
    q1_nao = Column('q1_nao', Integer)
    q2_correto = Column('q2_correto', Integer)
    q2_antes = Column('q2_antes', Integer)
    q2_depois = Column('q2_depois', Integer)
    q3_adequada = Column('q3_adequada', Integer)
    q3_curta = Column('q3_curta', Integer)
    q3_longa = Column('q3_longa', Integer)
    q4_alta = Column('q4_alta', Integer)
    q4_normal = Column('q4_normal', Integer)
    q4_baixa = Column('q4_baixa', Integer)
    q5_dificil = Column('q5_dificil', Integer)
    q5_normal = Column('q5_normal', Integer)
    q5_facil = Column('q5_facil', Integer)
    q6_dificil = Column('q6_dificil', Integer)
    q6_normal = Column('q6_normal', Integer)
    q6_facil = Column('q6_facil', Integer)
    q7_sim = Column('q7_sim', Integer)
    q7_nao = Column('q7_nao', Integer)
    q8_boa = Column('q8_boa', Integer)
    q8_media = Column('q8_media', Integer)
    q8_ruim = Column('q8_ruim', Integer)
    q9_sim = Column('q9_sim', Integer)
    q9_nao = Column('q9_nao', Integer)
    q10_sim = Column('q10_sim', Integer)
    q10_nao = Column('q10_nao', Integer)
    q11_sim = Column('q11_sim', Integer)
    q11_nao = Column('q11_nao', Integer)
    q12_sim = Column('q12_sim', Integer)
    q12_nao = Column('q12_nao', Integer)
    q13_sim = Column('q13_sim', Integer)
    q13_nao = Column('q13_nao', Integer)

    offering = relationship(Offering)

class AnswerSumTeacher(Base):
    __tablename__ = "answersumteacher"

    id = Column('answersumteacher_id', Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teacher.teacher_id'))
    teacher = relationship(Teacher)

    q6_dificil = Column('q6_dificil', Integer)
    q6_normal = Column('q6_normal', Integer)
    q6_facil = Column('q6_facil', Integer)
    q7_sim = Column('q7_sim', Integer)
    q7_nao = Column('q7_nao', Integer)
    q8_boa = Column('q8_boa', Integer)
    q8_media = Column('q8_media', Integer)
    q8_ruim = Column('q8_ruim', Integer)
    q9_sim = Column('q9_sim', Integer)
    q9_nao = Column('q9_nao', Integer)
    q10_sim = Column('q10_sim', Integer)
    q10_nao = Column('q10_nao', Integer)
    q11_sim = Column('q11_sim', Integer)
    q11_nao = Column('q11_nao', Integer)
    q12_sim = Column('q12_sim', Integer)
    q12_nao = Column('q12_nao', Integer)
    q13_sim = Column('q13_sim', Integer)
    q13_nao = Column('q13_nao', Integer)


class AnswerSumSubject(Base):
    __tablename__ = "answersumsubject"

    id = Column('answersumsubject_id', Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subject.subject_id'))
    subject = relationship(Subject)

    q1_sim = Column('q1_sim', Integer)
    q1_nao = Column('q1_nao', Integer)
    q2_correto = Column('q2_correto', Integer)
    q2_antes = Column('q2_antes', Integer)
    q2_depois = Column('q2_depois', Integer)
    q3_adequada = Column('q3_adequada', Integer)
    q3_curta = Column('q3_curta', Integer)
    q3_longa = Column('q3_longa', Integer)
    q4_alta = Column('q4_alta', Integer)
    q4_normal = Column('q4_normal', Integer)
    q4_baixa = Column('q4_baixa', Integer)
    q5_dificil = Column('q5_dificil', Integer)
    q5_normal = Column('q5_normal', Integer)
    q5_facil = Column('q5_facil', Integer)


class TeacherDisplay(Base):

    __tablename__ = "teacherdisplay"

    id = Column('teacherdisplay_id', Integer, primary_key=True)

    teacher_id = Column(Integer, ForeignKey('teacher.teacher_id'))
    teacher = relationship(Teacher)

    q6_resp = Column('q6_resp', String)
    q6_porc = Column('q6_porc', Integer)
    q7_resp = Column('q7_resp', String)
    q7_porc = Column('q7_porc', Integer)
    q8_resp = Column('q8_resp', String)
    q8_porc = Column('q8_porc', Integer)
    q9_resp = Column('q9_resp', String)
    q9_porc = Column('q9_porc', Integer)
    q10_resp = Column('q10_resp', String)
    q10_porc = Column('q10_porc', Integer)
    q11_resp = Column('q11_resp', String)
    q11_porc = Column('q11_porc', Integer)
    q12_resp = Column('q12_resp', String)
    q12_porc = Column('q12_porc', Integer)
    q13_resp = Column('q13_resp', String)
    q13_porc = Column('q13_porc', Integer)

class OfferingDisplay(Base):
    __tablename__ = "offeringdisplay"

    id = Column('offeringdisplay_id', Integer, primary_key=True)

    q1_resp = Column('q1_resp', String)
    q1_porc = Column('q1_porc', Integer)
    q2_resp = Column('q2_resp', String)
    q2_porc = Column('q2_porc', Integer)
    q3_resp = Column('q3_resp', String)
    q3_porc = Column('q3_porc', Integer)
    q4_resp = Column('q4_resp', String)
    q4_porc = Column('q4_porc', Integer)
    q5_resp = Column('q5_resp', String)
    q5_porc = Column('q5_porc', Integer)
    q6_resp = Column('q6_resp', String)
    q6_porc = Column('q6_porc', Integer)
    q7_resp = Column('q7_resp', String)
    q7_porc = Column('q7_porc', Integer)
    q8_resp = Column('q8_resp', String)
    q8_porc = Column('q8_porc', Integer)
    q9_resp = Column('q9_resp', String)
    q9_porc = Column('q9_porc', Integer)
    q10_resp = Column('q10_resp', String)
    q10_porc = Column('q10_porc', Integer)
    q11_resp = Column('q11_resp', String)
    q11_porc = Column('q11_porc', Integer)
    q12_resp = Column('q12_resp', String)
    q12_porc = Column('q12_porc', Integer)
    q13_resp = Column('q13_resp', String)
    q13_porc = Column('q13_porc', Integer)

    offering_id = Column(Integer, ForeignKey('offering.offering_id'))
    offering = relationship(Offering)


class SubjectDisplay(Base):
    __tablename__ = "subjectdisplay"

    id = Column('subjectdisplay_id', Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subject.subject_id'))
    subject = relationship(Subject)

    q1_resp = Column('q1_resp', String)
    q1_porc = Column('q1_porc', Integer)
    q2_resp = Column('q2_resp', String)
    q2_porc = Column('q2_porc', Integer)
    q3_resp = Column('q3_resp', String)
    q3_porc = Column('q3_porc', Integer)
    q4_resp = Column('q4_resp', String)
    q4_porc = Column('q4_porc', Integer)
    q5_resp = Column('q5_resp', String)
    q5_porc = Column('q5_porc', Integer)


def CreateDB():
    Base.metadata.create_all(DB)
