#!/usr/env/python
"""SuriCMS - Config File."""

import web

# Site Name
BaseTitle = "Suri.net"

# Debug Switch
web.config.debug = True

# Static directories (for css, js, other scripts, etc...)
# Hadled by App or WSGI, WSGI recommended for production.
AppStaticHandler = True
StaticDirs = ["static", "cursos/material"]

# Base Directory
BaseDir = "."

# Default Template
BasicView = "basic"
 
# Indexed Directories (generate Menus)
IndexDirs = [
  {
    "name" : "main",
    "dir"  : "contents",
    "adr"  : "/",
  },
  {
    "name" : "blog",
    "dir"  : "contents/blog",
    "adr"  : "/blog/",
    "view" : "blog",
  },
  {
    "name" : "courses",
    "dir"  : "contents/cursos",
    "adr"  : "/cursos/",
    "view" : "courses",
  },
  {
    "name" : "python",
    "dir"  : "contents/cursos/python",
    "adr"  : "/cursos/python/",
    "view" : "courses",
  },
  {
    "name" : "none",
    "dir"  : None ,
    "adr"  : "/",
  },
]

 
# Manually defined addresses ('couse you're free!)
# OBS: USE ALWAYS UTF
ManualPages = [
  { 
    "label" : "index",
    "name"  : "Index",
    "link"  : "/", 
    "file"  : "./index.md",
    "index" : "none",
  },
  { 
    "label" : "Cursos",
    "name"  : "Cursos",
    "link"  : "/cursos", 
    "file"  : "contents/Cursos.md",
    "index" : "main",
    "view"  : "courses",
  },
]


# Atomic templates that can be renderized inside views
GlobalElements = [
  "navbar",
  "includes",
  "footer",
]
    

# List available to all Templates
Global = {}
  

