#########################################################################
## Define your tables below; for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

# Let's generate a random user id for this user, and store it in the session.
from gluon import utils as gluon_utils


if session.user_key is None:
    session.user_key = gluon_utils.web2py_uuid()
    logger.info("Created new user key %r" % session.user_key)

# This is a table for all users.
db.define_table('people',
    Field('name', required=True),
    Field('user_key', required=True, default=session.user_key))

# We don't want to display the user_key, which looks like gibberish.
db.people.user_key.readable = False
