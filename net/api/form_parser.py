"""
Google Forms parser.
"""
import lxml.html
import codecs
#import pickle

#Raw = codecs.open("form.html", mode="r", encoding="utf-8").read()
Raw = open("form.html").read()
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


OutTable = open("questionnaire.csv", "w")

for i in Questionnaire:
  for j in i:
    OutTable.write(str(j))
  OutTable.write(", ")


#OutTable = open("questionnaire.csv", "w")

#pickle.dump(Questionnaire, OutTable)
