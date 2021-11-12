from flask import Blueprint, render_template,request,url_for,session,redirect
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField,HiddenField, SelectField,IntegerField,TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange

from library.addBook import service
import library.adapters.repository as repo
from library.authentication.authentication import login_required
from library.forms.sharedForms import *

import datetime

addBook_blueprint = Blueprint(
    'addBook_bp', __name__)

@addBook_blueprint.route('/addBook', methods=['GET','POST'])
@login_required
def addBook():
   
    form = bookForm()
    search = searchForm()
    
    if form.validate_on_submit():
      
        # Successful POST, i.e. the new book has passed data validation.

        #generating a dyanamic yet unit book id
        book_id= int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        print(type(book_id))


        service.load_new_book_into_repo(book_id, form.title.data, form.Description.data, form.authorName.data, form.releaseYear.data, repo.repo_instance)

        # Cause the web browser to display the page of all books that have the same date as the commented book,
        # and display all comments, including the new comment.
        return redirect(url_for('browse_bp.viewBook',id = book_id, show = False))

    return render_template(
    'addBook/addBook.html',
    form=form,
    handler_url=url_for('addBook_bp.addBook'),
    sidebarSearchForm = search

    )


class bookForm(FlaskForm):
    title = StringField('Title', 
        [
            DataRequired(),
            Length(min=1, message='Title is too short,please have at least 1 letter')
        ])
    Description= TextAreaField('Description', 
        [
            DataRequired(),
            Length(min=10, message='Description is too short,please have at least 10 letters')
        ])
    authorName = StringField('Author name', 
        [
            DataRequired(),
            Length(min=1, message='Author name is too short,please have at least 1 letter')
        ])
    releaseYear =  IntegerField("Release Year",
        [
            DataRequired(),
            NumberRange(min=1000, max=2021, message='Release Year should be between 1000 and 2021')
        ])
    submit = SubmitField('Confirm')
