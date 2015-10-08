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

db.define_table('store',
                Field('name'),
                Field('phone'),
                Field('created_on', 'datetime'),
                Field('star_rating', 'float'),
                Field('description', 'text'),
                )

db.store.created_on.default = datetime.utcnow()
db.store.star_rating.default = 3

# All these tables have an "id" already defined.
db.define_table('ingredient',
                Field('name'),
                Field('description', 'text'),
                Field('favorite_store', 'reference store'), # This is called a foreign key
                )

db.ingredient.favorite_store.ondelete = "SET NULL"


# 'integer', 'float', 'text', ...