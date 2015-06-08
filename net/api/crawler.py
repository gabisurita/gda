# encoding:utf-8
import requests
#import HTMLParser
import lxml.html
import codecs

import sys
sys.path.append("..")
from models import *

#import cookielib, urllib2


def OfferingFeeder():

  CreateDB()
  S = sessionmaker(bind=DB)()
  
  RawHtml = codecs.open("oferecimentos/1s2015.htt", mode="r", encoding="utf-8").read()

  Html = lxml.html.fromstring(RawHtml)
  
  Table = [Tag for Tag in Html if Tag.tag == "table"][0][0]

  Header = Table[:1]
#  print [Col.text_content() for Col in Header]
  
  Content = Table[1:]
  
  Iter = 0
  for Row in Content:
    Col = [Col.text_content() for Col in Row]
    Type = Col[0]
    Code = Col[1]
    SubCode = Col[1][:5]
    ClassCode = Col[1][6:]
    Name = Col[2]
    TeacherName = Col[3]
    SemesterData = Col[4].split(" - ")
    Year = int(SemesterData[0])
    Sems = int(SemesterData[1][0])
    Slots = int(Col[5])
    StudentsNum = int(Col[6])

    
    Sub = S.query(Subject).filter(Subject.code == SubCode)
    if Sub.count():

      Sem = S.query(Semester).filter(Semester.year == Year, Semester.sem == Sems)
      if Sem.count():  
        Sem = Sem.one()
      else:
        Sem = Semester(year=Year, sem=Sems)
        S.add(Sem)
        S.commit()
              
              
      Tec = S.query(Teacher).filter(Teacher.name == TeacherName)
      if Tec.count():  
        Tec = Tec.one()
      else:
        Tec = Teacher(name=TeacherName)
        S.add(Tec)
        S.commit()

      Sub = Sub.one()
      Off = Offering(code=ClassCode, subject=Sub, teacher=Tec, semester=Sem, slots=Slots, students=StudentsNum)
      S.add(Off)

  S.commit()
      
      
      
def SubjectFeeder():
  CreateDB()
  S = sessionmaker(bind=DB)()

  URL = "http://www.dac.unicamp.br/sistemas/catalogos/grad/catalogo2015/coordenadorias/0011/0011.html"

  RawHtml = requests.get(URL).text

  Html = lxml.html.fromstring(RawHtml)
  Content = Html.find_class("texto")[0]

  SubjectNames = Content.find_class("ancora")[1:]
  SubjectSum = Content.find_class("justificado")
  SubjectInfo = [Tag for Tag in Content if Tag.tag == "p"]

  for SubjectData, Summary, Info in zip(SubjectNames, SubjectSum, SubjectInfo):
    Code, Name = SubjectData.text_content().strip().split(" - ")
    Sum = Summary.text_content().split("Ementa: ")[1]  
    Meta, Req = Info.text_content().strip().split("%")
    Metas = (Meta+"%").split(" ")
    Credits = int(Metas[8][3:])
    Reqs = Req.split("  ")[1:]
    Reqs = [Req.split("/ ") for Req in Reqs]
    
    Sub = Subject(code=Code, name=Name, credits=Credits, summary = Sum)
    S.add(Sub)

    for Group, Gnum in zip(Reqs, range(len(Reqs))):
      for Code in Group:
        Req = Requirement(group=Gnum, code=Code, subject=Sub)
        S.add(Req)
        
  S.commit()  


def StudentFeeder():
  URL = "http://www.daconline.unicamp.br/altmatr/conspub_matriculadospordisciplinaturma.do"

  Header = {
  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
  "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
  }

  Request = requests.post(URL, allow_redirects=True, headers=Header)
  print Request.headers
  
  i = Request.content.find("var token = ")
  print Request.content[i: i+20]


  URL = "http://www.daconline.unicamp.br/altmatr/conspub_matriculadospordisciplinaturma.do"


  Data = {
    "org.apache.struts.taglib.html.TOKEN":
    "e0cb3c55fce40ae315454ff3fd90ae84",
    "cboSubG":1,
    "cboSubP":0,
    "cboAno":2015,
    "txtDisciplina":"EA616",
    "txtTurma":"A",
    "btnAcao":"Continuar",
  }

  Request = requests.post(URL, params=Data, allow_redirects=True,)
  
  
  print dir(Request)
#  print Request.content.strip()
#  print Request.status_code
  
   #  timeout=30.

def CleanDB():
  Subject.__table__.drop(DB)
  Requirement.__table__.drop(DB)
  Offering.__table__.drop(DB)
  Teacher.__table__.drop(DB)
  Semester.__table__.drop(DB)

#CleanDB()

#SubjectFeeder()
#OfferingFeeder()
StudentFeeder()


#def OfferingFeeder():
#  URL = "http://grade.daconline.unicamp.br/ajax/ax_busca.php"

#  Cookie = "GDE=tmnjlrjnd4er817hcb8nt9smr2; __utmt=1; __utma=61793146.1391364510.1431115862.1431115862.1431115862.1; __utmb=61793146.1.10.1431115862; __utmc=61793146; __utmz=61793146.1431115862.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); me=lA%824-%8DX%7D%F4%95%B6%9C%0F%FF%CC3%14%F8%E8%2A%06%AF%FE%E4%C8%C1%3B%80%2B%9EFv%F8%8F%15-%12V%EA%7B%CB%AC%3F%05V%E7%93%D8%2B%23c%9E%B2%FA%14%7DP%83%26%A1%E1%05q%EB%23%26%40%23%99%F3%85%B7%2FK%02w%04%90%DB%24%E3%28S%0C%40j%0A%2B%D0%C8%97a6%83%D7%BDKe%3A%E0"
#  
#  Data = {
#    "t":"tab_oferecimentos",
#    "periodo":0,
#    "sigla":"",
#    "turma":"",
#    "nivel":0,
#    "nome":"",
#    "professor":"",
#    "creditos":"",
#    "instituto":0,
#    "dia":"",
#    "horario":"",
#    "sala":"",
#    "ord[oferecimentos_a]":"1",
#    "em[oferecimentos_a]":"1",
#    "resultados_pagina":10,
#    "buscar":"",
#    "p":1,
##    "q":"E",
#  }
#  
#  Header = {
#  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
#"Accept-Encoding":"gzip, deflate, sdch",
#"Accept-Language":"pt-BR,pt;q=0.8,en-US;q=0.6,en;q=0.4",
#"Connection":"keep-alive",
#"Cookie":"GDE=tmnjlrjnd4er817hcb8nt9smr2; __utmt=1; __utma=61793146.1391364510.1431115862.1431115862.1431115862.1; __utmb=61793146.1.10.1431115862; __utmc=61793146; __utmz=61793146.1431115862.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); me=lA%824-%8DX%7D%F4%95%B6%9C%0F%FF%CC3%14%F8%E8%2A%06%AF%FE%E4%C8%C1%3B%80%2B%9EFv%F8%8F%15-%12V%EA%7B%CB%AC%3F%05V%E7%93%D8%2B%23c%9E%B2%FA%14%7DP%83%26%A1%E1%05q%EB%23%26%40%23%99%F3%85%B7%2FK%02w%04%90%DB%24%E3%28S%0C%40j%0A%2B%D0%C8%97a6%83%D7%BDKe%3A%E0",
#"DNT":"1",
#"Host":"grade.daconline.unicamp.br",
#"Referer":"https://grade.daconline.unicamp.br/controladores/ControlLogin.php",
#"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.101 Safari/537.36",
#"X-Requested-With":"XMLHttpRequest",
#}
#  
#  CookieHandler = Cookie.split("=")
#  Keys = CookieHandler[::2]
#  Values = CookieHandler[1::2]
#  Cookies = {Key : Value for Key, Value in zip(Keys, Values)}
#  
#  
#  Request = requests.post(URL, params=Data, cookies=Cookies, allow_redirects=True,) #  timeout=30.
#    
#  print dir(Request)
#  print Request.raw.d    ata
#
#
#  
#OfferingFeeder()
