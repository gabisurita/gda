"""
Google Forms parser.
"""
import lxml.html
import codecs
import os
import csv
#import pickle


def ParseForm(File):
  #Raw = codecs.open("form.html", mode="r", encoding="utf-8").read()

  Raw = open(File).read()
  Html = lxml.html.fromstring(Raw)

  Form = Html.xpath("//div[@class='ss-form-page']")

  Questionnaire = []

  for Page in Form:
    Group = []
    
    Sections = Page.xpath("div[@role='group']")

    for Entry in Sections:
      Content = Entry.xpath("div[@class='ss-form-entry']")[0].getchildren()
      
      Q = {}
    
      Q["name"] = Content[0].text_content()
      Q["help"] = Content[1].text_content()
      Input = Content[2]

      # Select
      if Input.tag == "ul":      
        Options = Input.getchildren()
        Q["type"] = Options[0][0][0].attrib["type"]
        Q["opts"] = [Op.text_content() for Op in Options]


      # Table
      elif Input.tag == "table":
        Lines = Input.getchildren()
        
        # Scale Question
        if len(Lines) == 1:
          Q["type"] = "scale"
          Cols = Lines[0].getchildren()
          Q["opts"] = [op.text_content() for op in Cols[0][1:-1]]
          Q["down"] = Cols[1][0].text_content()
          Q["up"] = Cols[1][-1].text_content()

        # Multi Scale Question
        else:
          Q["type"] = "table"
          Head = Lines[0]
          Body = Lines[1]        
          
          Options = Head[0].getchildren()[1:]
          Q["opts"] = [op.text_content() for op in Options]
          Topics = Body.getchildren()
          Q["itens"] = [op.text_content() for op in Topics]
          
      # Textarea
      elif Input.tag == "div":
        Q["type"] = "textarea"
        
        
      else:
        raise NotImplementedError("Question type not parsable")   
      
      
      Group.append(Q)  
    Questionnaire.append(Group)




  QTable = open("questions.csv", "w")
  W = csv.writer(QTable)
  

  for Page, i in zip(Questionnaire, range(len(Questionnaire))):
    for Q, j in zip(Page, range(len(Page))):
      if "itens" in Q:
        R = [i,j,Q["name"], Q["help"], Q["type"], Q["opts"], Q["itens"], []]
      elif "opts" in Q:
        R = [i,j,Q["name"], Q["help"], Q["type"], Q["opts"], [], []]
      else:
        R = [i,j,Q["name"], Q["help"], Q["type"], "", "",""]
      
      W.writerow(R)



  PageListing = ""
  Fields = ""

  for Group, i in zip(Questionnaire, range(len(Questionnaire))):
    if i == 0:
      PageListing += '<li class="current active"><span>%s</span></li>\n' % (i + 1)
      
      Fields += '<fieldset class="current">\n'

    else:
      PageListing += '<li><span>%s</span></li>\n' % (i + 1)
      Fields += '<fieldset class="next">\n'
    
    for Q, j in zip(Group, range(len(Group))):
      Id =str(i)+"."+str(j)
      if Q["type"] in ("radio", "checkbox"):
        Fields += '<label for="%s">%s</label><br>\n' % (Id, Q["name"])
        Fields += '<p>%s</p>\n' % (Q["help"])

        for Op in Q["opts"]:
          Fields += '<input name="%s" type="%s" value="%s">%s<br>\n' % (Id, Q["type"], Op, Op)


      if Q["type"] == "table":
        Fields += '<label for="%s">%s</label><br>\n' % (Id, Q["name"])
        Fields += '<p>%s</p>\n' % (Q["help"])


        Fields += '<table>\n'

        Fields += '<thead>\n<tr>\n'
        Fields += '<td></td>\n'
        for Op in Q["opts"]:
          Fields += '<td>%s</td>' % Op
        Fields += '</tr>\n</thead>\n'
        
        Fields += '<tbody>\n'
        for It in Q["itens"]:
          Fields += '<tr>\n'     
          Fields += '<td>%s</td>\n' % It
          for Op in Q["opts"]:
            Fields += '<td><input name="%s" value="%s" type="radio"><br></td>\n' % (Id+It, Op)
          Fields += '</tr>\n'
        Fields += '</tbody>\n'

        Fields += '</table>\n'
        

      if Q["type"] == "scale":
        Fields += '<label for="%s">%s</label><br>\n' % (Q["name"], Q["name"])
        Fields += '<p>%s</p>\n' % (Q["help"])
        
        Fields += '<table>\n'

        Fields += '<thead>\n<tr>\n'
        Fields += '<td></td>\n'
        for Op in Q["opts"]:
          Fields += '<td>%s</td>' % Op
        Fields += '<td></td>\n'
        Fields += '</tr>\n</thead>\n'
        
        Fields += '<tbody>\n'
        Fields += '<tr>\n'     
        Fields += '<td>%s</td>\n' % Q["down"]
        for Op in Q["opts"]:
          Fields += '<td><input name="%s" value="%s" type="radio"><br></td>\n' % (Id, Op)
        Fields += '<td>%s</td>\n' % Q["down"]
        Fields += '</tr>\n'
        Fields += '</tbody>\n'

        Fields += '</table>\n'
               
        
      
      if Q["type"] == "textarea":    
        Fields += '<label for="%s">%s</label><br>\n' % (Id, Q["name"])
        Fields += '<p>%s</p>\n' % (Q["help"])

        Fields += '<textarea name="%s"></textarea><br>\n' % (Id)
    
    Fields += '</fieldset>\n'

  OutForm = open("form.html", "w")



  OutForm.write(
"""$def with (OfferingInst)
"""
  )


  OutForm.write('<form id="jsform" action="avaliar" method="POST">')
  OutForm.write('<ul id="section-tabs">')
  OutForm.write(PageListing)
  OutForm.write('</ul>')
  OutForm.write('<div id="fieldsets">')
  OutForm.write(Fields)
  OutForm.write('<a class="btn" id="next">Próxima pergunta</a>\n')
  OutForm.write('<input type="submit" class="btn">\n')
  OutForm.write('</div>\n</form>\n')


  OutForm.write(
  """
  """
  )
  

if __name__ == "__main__":
  ParseForm("form.htt")
  
