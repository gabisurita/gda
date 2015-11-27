#!/usr/env/python
"""
GDA - Config File.

Define Global Constants Here!
"""

import web
import os

BaseTitle = "GDA"

# Base Directory
BaseDir = os.path.dirname(os.path.abspath(__file__))
UploadDir = BaseDir + '/uploads'
os.chdir(BaseDir)

# Hadled by App or WSGI, WSGI recommended for production.
AppStaticHandler = True

# Static directories (for css, js, other scripts, etc...)
StaticDirs = ["static"]

# Disable debug and enable Sessions
#web.config.debug = False

# Databases
SystemDB = 'sqlite:///test.db'
UserDB = 'sqlite:///test.db'
