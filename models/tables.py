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
                Field('street_no', 'integer'),
                Field('star_rating', 'float'),
                Field('description', 'text'),
                )

db.store.created_on.default = datetime.utcnow()
db.store.star_rating.default = 3
db.store.street_no.label = 'Street number'
db.store.id.readable = False

# All these tables have an "id" already defined.
db.define_table('ingredient',
                Field('name'),
                Field('description', 'text'),
                )

db.define_table('canbuy',
                Field('user_id', db.auth_user),
                Field('store', 'reference store'),
                Field('ingredient', 'reference ingredient'),
                Field('is_favorite', 'boolean'),
                )
db.canbuy.user_id.default = auth.user_id
db.canbuy.is_favorite.default = False

db.define_table('recipe',
        Field('name', required=True),
        Field('time_required', 'float'),
        Field('description', 'text'),
        Field('recipe_cost', 'float', requires=IS_FLOAT_IN_RANGE(0, 100))
      )
db.recipe.recipe_cost.label = 'Cost'


# 'integer', 'float', 'text', ...