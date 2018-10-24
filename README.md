# Project # 04: Item Catalog
## by Abdullah A. Salman

This is the fourth project of ***[Udacity Full Stack Web Developer Nanodegree Program](https://classroom.udacity.com/nanodegrees/nd004/)*** .

### Summary
* *An online catalog to store, retrieve and modify the information of different items in various categories.*
* *It is a web application created with Python based micro web framework Flask .*
* *Uses SQLALchemy to perform CRUD operations.*
* *Uses Google Oauth 2.0 for the authentication and server side authorization with sessions and cookies.*
* *Implements RESTful APIs endpoints with JSON.*

## Introduction
This project requires students to build a web application using [Flask](http://flask.pocoo.org/) - *a microframework for [Python](https://www.python.org/)* - that provides an online catalog to store, view, and modify information about different items in various categories. The app should:

* Let the users to register on using a secure authentication - *such as OAuth* - provided by a third party.
* Let the user log in and out of the app with secure session handling and a local permission system to authorize or restrict a user from using different features of the app.
* Let the user to view different items in various categories, add their own items to the catalog, modify their information or delete it when required.
*  Provide an aesthetic interface and experience to the users.
* Implements JSON endpoint to serve the purpose of RESTful API.

*View more information about the project's requirements [here](https://review.udacity.com/#!/rubrics/5/view).*

### *SPORTS BAZAR*
*I have implemented my solution as a generic catalog, keeping in mind the working of an online marketplace for the sporting goods and activewears.*

*User can sign in with their Google accounts and add, modify and delete items.
While only 'admin' can add, modify or delete the categories.*

## Contents
The project repository is organized as following:
```
Item-Catalog-Project
├── sportsbazar/
|	└── static/
|		└── css/
|		└── img/
|		└──js/
|	└── templates/
|	└──  __init__.py
|	└──  auth.py
|	└──  db_connect.py
|	└──  db_populate.py
|	└──  db_setup.py
|	└──  json_endpoints.py
|	└──  views.py
├── app.py
├── dependencies.txt
├── g_client_secrets.json
├── sportsbazar.db
└── README.md
```
### Description
**Directories:**
* `Item-Catalog-Project`- Root directory containing the app.
* `sportsbazar` - Main module of the app.
* `static` - Contains the content for the flask web app and relevant sub-directories containing the stylesheets, javascript files and images etc.
* `templates` - Contains the html templates which are rendered and sent to the client side on requests.

**Files:**

 * `app.py` - Main Python script to configure and start the app.
 *  `g_client_secrets.json`  - Client secrets for Google OAuth login.
 *  `sportsbazar.db` - Database file for the SQLite database.  (*Generated by the `app.py` script*)
 * `readme.md` - Me :)
 * `sportsbazar/`
	 * `__init.py__` - Initializes the sportsbazar module.
	 * `auth.py` -  Handles authentication routines: login & logout.
	 * `db_connect.py` - Snippet to make the connection with database.
	 * `db_populate.py` - Populates the database with the test data
	 *  `db_setup.py` - Sets up and create the database tables.
	 * `json_endpoints.py` - Provides the data in json format.
	 * `views.py` - Implements the CRUD operations on database, enforce authorization rules and return the rendered html pages to the client side according the program logic.

## Try by yourself

### Requirements
Main dependencies for this project to run are following:
* Python 2.7.*
* httplib2  0.11.*
* Flask  1.0.*
* SQLAlchemy 1.2.*
* Flask-HTTPAuth   3.2.*
* Flask-SQLAlchemy 2.3.*
* oauth2client 4.3.*

See `dependencies.txt` file for detailed specifications.

### Setting up the environment
The project runs best in the Linux Virtual Box interfaced with Vagrant. Check out [here](https://github.com/abdullah-22/Logs-Analysis-Project) for the setup guidelines or follow [this](https://www.udacity.com/wiki/ud088/vagrant) link.
* Place the project repository in the shared folder `vagrant/` of the virtual machine.
* Make sure to get your Google Oauth credentials from [here](https://console.developers.google.com/?pli=1). (*Follow [this](https://developers.google.com/api-client-library/python/auth/web-app) document to have the insight into Google OAuth*)
* Copy your `client_secrets` into the `g_client_secrets.py` file.
* Copy your `client_id` from these credentials and put at *line 25* of  `login.html` - for the `data-clientid`value.

### Run
To run the app, make sure to be in the `Item-Catalog-Project` directory in the running virtual machine.
For the first time on executing the following command, the database will be created and filled with test data.
```bash
python app.py
```
It will start the web server. To check out what is being served, open any web browser in your host machine and try:
```
http://localhost:5000/
```
Explore the app :)
*(To stop the server, press `ctrl-c` in the bash)*

### Miscellaneous
* To be able to add, modify or delete categories user must be an admin. This can be specified in the `app.py` file by setting the
	* `app.config['ADMIN_ID']`
	*  `app.config['ADMIN_NAME']`
	* `app.config['ADMIN_EMAIL']`
values to the ones with which you registered.
* Lines 29-31 can be used in the development environment to generate a random `app.secret_key`. This will enhance the security of sessions.
* Some of the code used in this project was provided by Udacity (without any copyrights info).
* All the media (including images, links, videos) used in this website may subject to copyrights of the respective owners.
* These are used for educational purpose only and not for any commercial use.
* This readme file is created by following the guidelines provided on [Udacity Discussion Forum](https://discussions.udacity.com/t/movie-trailer-website-checklist-read-this-before-you-submit-your-project/39852) and using an online markdown [editor](https://stackedit.io/).
* Helpful material: this [link](https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask), this [repo](https://github.com/SteveWooding/fullstack-nanodegree-vm/tree/master/vagrant/catalog),  this [article](https://pythonspot.com/login-to-flask-app-with-google/) and [this](https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask).

_(stuck at someplace? found any error? or just want to connect? see below :))_

## [](https://github.com/abdullah-22/Logs-Analysis-Project#ping-me-)Ping me @

**Abdullah A. Salman**

-   [Email](mailto:20abdullahahmadsalman@gmail.com)
-   [Github](https://github.com/abdullah-22)
-   [Linkedin](http://www.linkedin.com/in/abdullahasalman)
