"""
Sets the configuration variables needed for
the application to run. 

class 'Config' passed into create_app()
function in "application?__init__.py"

"""

import os
if os.path.exists("env.py"):
    import env

class Config:
    # MongoDB config
    SECRET_KEY = os.environ.get("SECRET_KEY")
    MONGO_URI = os.environ.get("MONGO_URI")
    MONGO_DBNAME = os.environ.get("MONGO_DBNAME")
    
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    SENDINBLUE_API_KEY = os.environ.get("SENDINBLUE_API_KEY")
    






