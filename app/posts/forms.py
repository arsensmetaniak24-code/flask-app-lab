from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, TextAreaField, SubmitField, DateTimeLocalField, SelectField
from wtforms.validators import DataRequired, Length
from .models import CATEGORIES


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=4, max=150)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(max=500)])
    is_active = BooleanField('Active')
    publish_date = DateTimeLocalField('Publish Date', default=datetime.now)
    category = SelectField('Category', choices=CATEGORIES)
    submit = SubmitField('Submit')

class DeleteForm(FlaskForm):
    pass
