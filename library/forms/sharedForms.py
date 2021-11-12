from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,HiddenField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError

class searchForm(FlaskForm):
    search= StringField('Search a book', 
        [
            DataRequired(),
            Length(min=1, message='Your comment is too short,please have at least 5 letters')
        ])
    searchBy =  SelectField("Search by",choices=["By release year", "By author name","By publisher name"])
    submit = SubmitField('Search')