from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length
from app import db
from app.models import Grosses, Shows, Theatres

list_theatre = []
list_theatre_id = []
for u in db.session.query(Theatres).order_by(Theatres.theatre).all():
            values = u.__dict__
            list_theatre.append(values['theatre'])
            list_theatre_id.append(values['theatre_id'])

list_show = []
list_show_id = []
for u in db.session.query(Shows).order_by(Shows.show_name).all():
            values = u.__dict__
            list_show.append(values['show_name'])
            list_show_id.append(values['show_id'])



class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=15)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

class SessionForm(FlaskForm):
    clear_session = SubmitField("Clear")

class TheatreForm(FlaskForm):
    theatres = SelectField("Theatres", choices=(list_theatre))
    theatres_submit = SubmitField("Submit")

class ShowsForm(FlaskForm):
    shows = SelectField("Shows", choices=(list_show))
    shows_submit = SubmitField("Submit")