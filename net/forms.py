import web

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

myform = web.form.Form(
    #form.Textbox("boe"),
    #form.Textbox("bax",
    #    form.notnull,
    #    form.regexp('\d+', 'Must be a digit'),
    #    form.Validator('Must be more than 5', lambda x:int(x)>5)),
    #form.Textarea('moe'),
    #form.Checkbox('curly'),
        web.form.Dropdown('Semestre', [('1','primeiro'), ('2','segundo')]),
        web.form.Dropdown('teste', args = a),
        web.form.Textbox("Ano", Class="form-control"),
        web.form.Button('Submeter', Class="btn btn-primary"))
