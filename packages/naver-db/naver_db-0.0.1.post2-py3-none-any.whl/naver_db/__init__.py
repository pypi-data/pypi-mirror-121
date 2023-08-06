try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    __path__ = __import__('pkgutil').extend_path(__path__, __name__)

from .persistence import Persistence
from .mysqldb import MySQLDB
from naver_config import NaverConfig
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


class NaverDB(NaverConfig):

    def __init__(self):

        self.myDb = SQLAlchemy(self.myApp)
        self.myApp = Flask(__name__)
        super().__init__(self.myApp) 
        self.persistence = Persistence(super(), self.myApp, self.myDb)
        # self.mysqldb = MySQLDB(super(), self.myApp, self.myDb)


if __name__ == '__main__':
    pass
