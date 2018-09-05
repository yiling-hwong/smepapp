from flask import current_app, g
import os

from flask_mysqldb import MySQL


def init_db(app):

# configure db

    fn = os.path.join(os.path.dirname(__file__), '..','instance','db.csv')
    lines = open(fn,'r').readlines()

    db_dict = {}

    for line in lines:
        spline = line.rstrip('\n').split(',')
        db_dict[spline[0]] = spline[1]

    app.config['MYSQL_HOST'] = db_dict['mysql_host']
    app.config['MYSQL_USER'] = db_dict['mysql_user']
    app.config['MYSQL_PASSWORD'] = db_dict['mysql_password']
    app.config['MYSQL_DB'] = db_dict['mysql_db']

    # instantiate db

    mysql = MySQL(app)

    return mysql


