from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp, Email


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=10)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone', validators=[DataRequired(), Regexp(r'^\+380\d{9}$', message='Phone must be in format +380XXXXXXXXX')])
    subject = SelectField('Subject', choices=[('general', 'General'), ('support', 'Support'), ('feedback', 'Feedback'), ('other', 'Other')])
    message = TextAreaField('Message', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Submit')
