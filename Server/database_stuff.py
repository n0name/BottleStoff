from sqlobject import *
import os

_DB_NAME = os.path.dirname(os.path.realpath(__file__)) + r"\users.db"
print(_DB_NAME)

sqlhub.processConnection = connectionForURI('sqlite:/{}'.format(_DB_NAME))


class UserInfo(SQLObject):
    pos_x = IntCol()
    pos_y = IntCol()
    pass


class User(SQLObject):
    name = StringCol()
    password = StringCol()
    user_data = ForeignKey('UserInfo', notNull=True)


User.createTable(ifNotExists=True)
UserInfo.createTable(ifNotExists=True)
