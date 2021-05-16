from sqlalchemy.sql.schema import ForeignKey
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), unique=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    password = db.Column(db.String(45))

class Theatres(db.Model):
    theatre_id = db.Column(db.Integer, primary_key=True)
    theatre = db.Column(db.String(45))

class Grosses(db.Model):
    performance_id = db.Column(db.Integer, primary_key=True)
    show_id = db.Column(db.Integer)
    theatre_id = db.Column(db.Integer)
    week_ending = db.Column(db.Date)
    week_number = db.Column(db.Integer)
    weekly_gross_overall = db.Column(db.Float)
    weekly_gross_overall = db.Column(db.Float)
    potential_gross = db.Column(db.Float)
    avg_ticket_price = db.Column(db.Float)
    top_ticket_price = db.Column(db.Float)
    seats_sold = db.Column(db.Integer)
    seats_in_theatre = db.Column(db.Integer)
    pct_capacity = db.Column(db.Float)
    performances = db.Column(db.Integer)
    previews = db.Column(db.Integer)

class Shows(db.Model):
    show_id = db.Column(db.Integer, primary_key=True)
    show_name = db.Column(db.String(125))