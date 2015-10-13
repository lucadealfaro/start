# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################


def index():
    logger.info("Here we are, in the controller.")
    response.flash = T("Hello World")
    return dict(shops=[])


def check_unlucky(form):
    # I have:
    # form.vars.street_no is the integer
    # request.vars.street_no is the non-validated string.
    if form.vars.street_no % 13 == 0:
        form.errors.street_no = T('Unlucky number')


def add_store():
    """Lets the user add a store."""
    # logger.info("My session is: %r" % session)
    form = SQLFORM(db.store)
    if form.process(onvalidation=check_unlucky).accepted:
        session.flash = T('The data was inserted')
        redirect(URL('add_store'))
    return dict(form=form)


def show_stores():
    store_list = db(db.store).select()
    return dict(store_list=store_list)


def store_details():
    store = db.store(request.args(0))
    if store is None:
        session.flash = T('No such store')
        redirect(URL('default', 'show_stores'))
    form = SQLFORM(db.store, record=store, readonly=True)
    edit_button = A('Edit', _class='btn btn-warning',
                    _href=URL('default', 'store_edit', args=[store.id]))
    list_button = A('View all', _class='btn btn-info',
                    _href=URL('default', 'show_stores'))
    return dict(form=form, edit_button=edit_button,
                list_button=list_button)


def store_edit():
    store = db.store(request.args(0))
    if store is None:
        session.flash = T('No such store')
        redirect(URL('default', 'show_stores'))
    form = SQLFORM(db.store, record=store)
    if form.process(onvalidation=check_unlucky).accepted:
        session.flash = T('The data was edited')
        redirect(URL('default', 'store_details', args=[store.id]))
    edit_button = A('View', _class='btn btn-warning',
                    _href=URL('default', 'store_details', args=[store.id]))
    return dict(form=form, edit_button=edit_button)


def my_stores():
    # Query to view all stores.
    q = db.store
    grid = SQLFORM.grid(q,
        paginate=2,
        csv=False,
        editable=True,
        fields=[db.store.name, db.store.description]
        )
    return dict(grid=grid)


def add_ingredient():
    form = SQLFORM(db.ingredient)
    if form.process().accepted:
        session.flash = T('The data was inserted')
        redirect(URL('add_ingredient'))
    return dict(form=form)

def add_recipe():
    form = SQLFORM.factory(
        Field('name', required=True),
        Field('time_required'),
        Field('description', 'text'),
        Field('cost', 'float', requires=IS_FLOAT_IN_RANGE(0, 100))
    )
    if form.process().accepted:
        # Note: no data is inserted!
        logger.info("Inserted a recipe called %r", form.vars.name)
        logger.info("Cost, raw %r", request.vars.cost)
        logger.info("Cost, in form %r", form.vars.cost)
        session.flash = T('The data was processed')
        redirect(URL('add_recipe'))
    return dict(form=form)




def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


