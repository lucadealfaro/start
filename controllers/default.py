# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

SHOP_LIST = {
    0: {'name': 'Safeway',
        'ingredients': ['pasta', 'oil', 'salt', 'anchovies']},
    1: {'name': "Trader Joe's",
        'ingredients': ['tuna', 'peanuts', 'beer']},
    2: {'name': 'The Milk Pail',
        'ingredients': ['yoghurt', 'bread', 'onions', 'parmesan']}
}


def index():
    logger.info("Here we are, in the controller.")
    response.flash = T("Hello World")
    return dict(shops=SHOP_LIST)


def store():
    store_id = request.args(0)
    try:
        sid = int(store_id)
    except Exception, e:
        session.message = T('Bad URL')
        redirect(URL('default', 'index'))
    s = SHOP_LIST.get(sid)
    logger.info("Found the store: %r" % s)
    if s is None:
        session.message = T('No such store')
        redirect(URL('default', 'index'))
    session.pasta_sauce = "Pesto" # Not used.
    return dict(shop=s)


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


