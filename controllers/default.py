# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

def index():
    """
    Allows a person to register in the system, if they are not registered already.
    """
    # If the person is registered, we store the person id in session.person_id.
    db.people.name.label = "What's your name?"
    row = db.people(session.person_id)
    form = SQLFORM(db.people, record=row)
    if form.process().accepted:
        session.person_id = form.vars.id
        session.flash = "Welcome, %s!" % form.vars.name
        redirect(URL('default', 'people'))
    return dict(form=form)


def people():
    """
    Gives the person a table displaying all the people, to search.
    """
    db.people.name.label = "Name"
    if session.person_id is None:
        # First, we need to know who you are.
        return redirect(URL('default', 'index'))
    # Creates a list of other people.
    q = db.people
    links = [dict(header='',
                 body = lambda r: A(I(_class='fa fa-comments'), 'Chat', _class='btn btn-success',
                                    _href=URL('default', 'chat', args=[session.person_id, r.id])))]
    grid = SQLFORM.grid(q,
                        links=links,
                        editable=False,
                        details=False,
                        csv=False)
    return dict(grid=grid)





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


