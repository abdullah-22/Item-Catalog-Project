"""
    Initialisation of the sportsbazar package.
"""
from flask import Flask

# Initialise the Flask app object
app = Flask(__name__)

import sportsbazar.views
import sportsbazar.json_endpoints
import sportsbazar.auth
