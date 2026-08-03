# from flask_mysqldb import MYSQL #alt for pymysql
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_jwt_extended import JWTManager


bcrypt = Bcrypt()
mail = Mail()
jwt = JWTManager()

#THis file is used to create package needed to be initialized