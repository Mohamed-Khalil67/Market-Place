from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, IntegerField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired(), Length(min=2, max=30)])
    price = IntegerField('Price (in $)', validators=[DataRequired(), NumberRange(min=1)])
    barcode = StringField('Barcode', validators=[DataRequired(), Length(min=8, max=12)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=10, max=1024)])
    category = SelectField('Category', coerce=int, validators=[DataRequired()])
    stock = IntegerField('Stock', validators=[DataRequired(), NumberRange(min=0)])
    image = FileField('Product Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Add Product')

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[DataRequired(), Length(min=2, max=30)])
    description = TextAreaField('Description', validators=[Length(max=256)])
    submit = SubmitField('Add Category')
