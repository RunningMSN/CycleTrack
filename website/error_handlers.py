from flask import redirect, url_for

def page_not_found(e):
  return redirect(url_for('pages.index'))