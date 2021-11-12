from flask import Blueprint, render_template,request,url_for,session,redirect
from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, SubmitField,HiddenField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError


from library.search import service
import library.adapters.repository as repo
from library.authentication.authentication import login_required
from library.forms.sharedForms import *
search_blueprint = Blueprint(
    'search_bp', __name__)

#empty route?
@search_blueprint.route('/search', methods=['POST'])
def search():
    sidebarSearchForm = searchForm()
    if sidebarSearchForm.validate_on_submit():
        # Successful POST, i.e. the comment text has passed data validation.
        # Extract the user search string
        inp = sidebarSearchForm.search.data
        message = "Please click on the book to see more!"
        foundBooks =[]
        
        if sidebarSearchForm.searchBy.data == "By release year": 
            foundBooks = service.find_books_by_year(inp, repo.repo_instance)

        elif sidebarSearchForm.searchBy.data == "By author name":
            foundBooks = service.find_books_by_author(inp, repo.repo_instance)

        elif sidebarSearchForm.searchBy.data == "By publisher name":
            foundBooks = service.find_books_by_publisher(inp, repo.repo_instance)
            # default case for catching errors
        else:
            message = "Sorry, we did not find any matches for you. \n\nTry another search?"
        if foundBooks == []:
            message = "Sorry, we did not find any matches for you. \n\nTry another search?"

            

        return render_template('search/search.html',
                                sidebarSearchForm = sidebarSearchForm,
                                books = foundBooks,
                                message = message,

        )

    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the book id of the book being commented from the form.
        book_id = int(form.book_id.data)
        reviews = service.get_reviews_for_book(book_id, repo.repo_instance)

    # For an unsuccessful POST, retrieve the book to comment in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    book = service.get_book_by_id(book_id, repo.repo_instance)
    return render_template(
        'search/search.html',
        books=[],
        message = "An error has occurred when searching.\nPlease try again!",
        sidebarSearchForm =  sidebarSearchForm
    )