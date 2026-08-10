# from flask_mysqldb import MYSQL #alt for pymysql
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth


bcrypt = Bcrypt()
mail = Mail()
jwt = JWTManager()
oauth = OAuth()

#THis file is used to create package needed to be initialized