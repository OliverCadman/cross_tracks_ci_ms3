"""
Cross//Tracks run.py
=====================

Calls the instantiated Flask application from 
"application/__init__.py, and commands the server
to run the instance.
"
"""

import os
from application import create_app
from application.config import Config


app = create_app()

# Run the app with IP and PORT variables from 
# env.py file
if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)


