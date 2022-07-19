from flask import Blueprint
import pandas as pd

jinja_templates = Blueprint('jinja_templates', __name__)

@jinja_templates.app_template_filter()
def format_days(timedelta):
    return pd.Timedelta(timedelta).days