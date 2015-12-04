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
    return str("/docentes/%s" % self.name.lower().replace(" ","_").decode("utf8"))


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
  question7 = Column('question7', Integer)
  question8 = Column('question8', Integer)
  question9 = Column('question9', Integer)
  question10 = Column('question10', Integer)


def CreateDB():
  Base.metadata.create_all(DB)
