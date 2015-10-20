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

from datetime import datetime

# This is a table for all users.
db.define_table('people',
    Field('user_id', db.auth_user, default=auth.user_id),
    Field('name', required=True),
    Field('description', 'text'),
    )

db.people.id.readable = False
db.people.user_id.readable = False
db.people.description.represent = lambda v, r: DIV(v, _class="msg_content")


# Here is a table for messages.
db.define_table('messages',
    Field('user0', db.auth_user),
    Field('user1', db.auth_user),
    Field('sender',  db.auth_user, default=auth.user_id),
    Field('msg_time', 'datetime', default=datetime.utcnow()),
    Field('msg_text', 'text'))

db.messages.msg_time.label = "Time"
db.messages.msg_text.label = "Message"
db.messages.msg_text.represent = lambda v, r: DIV(v, _class="msg_content")
