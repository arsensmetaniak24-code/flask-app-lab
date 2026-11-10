from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, DecimalField, SelectField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, InputRequired


class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3)])
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={'rows': 5, "cols": 40})
    price = DecimalField('Price', validators=[InputRequired(), NumberRange(min=0.01)], places=2)
    category = SelectField('Category', choices=[('laptop', 'Laptop'), ('phone', 'Phone'), ('pc', 'PC'), ('other', 'Other')])
    quantity = IntegerField('Quantity', validators=[InputRequired(), NumberRange(min=0)])
    image = FileField('Image', validators=[FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Submit')