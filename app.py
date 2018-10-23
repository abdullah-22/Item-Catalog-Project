#!/usr/bin/env python
"""
    Main Python script to configure and start the app.

    Checks if the database exists.
    If not, then creates a new databse and populate it with test data.
"""


import os.path, random, string
from sportsbazar import app
from sportsbazar.db_setup import db_create
from sportsbazar.db_populate import db_populate


# Constants for - DB, Admin
DB_URL = "sqlite:///sportsbazar.db?check_same_thread=False"

# END Constants


if __name__ == "__main__":
    # App configuration
    app.config['DB_URL'] = "sqlite:///sportsbazar.db?check_same_thread=False"
    app.config['ENV'] = "development"
    # Secret key to secure session and cookies
    #secret_key = "".join(random.choice(string.ascii_uppercase + string.digits)
     #               for x in xrange(32))
    app.secret_key = "super_secret_key"

    # Credentials of admin
    app.config['ADMIN_ID'] = 1
    app.config['ADMIN_NAME'] = "Test User"
    app.config['ADMIN_EMAIL'] = "testuser@domain.com"
    app.config['ADMIN_PICTURE'] = "https://upload.wikimedia.org/wikipedia/commons/5/55/User-admin-gear.svg"

    if app.config['DB_URL'] == "sqlite:///sportsbazar.db?check_same_thread=False":
        if os.path.isfile('sportsbazar.db') is False:
            db_create(app.config['DB_URL'])
            db_populate()

    app.debug = True
    app.run(host='0.0.0.0', port = 5000)
