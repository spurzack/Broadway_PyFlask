from flask.signals import template_rendered
from app import app, db
from flask import render_template, redirect, flash, session, url_for, send_file
from app.forms import LoginForm, TheatreForm, ShowsForm
from app.models import Grosses, User, Theatres, Shows
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from io import BytesIO
import pandas as pd
import numpy as np
from sqlalchemy import func

# cnx = mysql.connector.connect(user='root', password='password', database='Broadway_DB')
curA = cnx.cursor()
curB = cnx.cursor()

theatreid = 1
showid = 1

@app.route("/")
@app.route("/index")
@app.route("/home")
def index():
    return render_template("index.html", index=True)

@app.route("/login", methods=['POST', 'GET'])
def login():
    if session.get('first_name'):
        test = session.get('first_name')
        return redirect(url_for('index'), index=True, data=test, logout=False)

    form = LoginForm()
    if form.validate_on_submit():
        form_username = form.username.data
        password = form.password.data
        for u in db.session.query(User).filter(User.username == form_username).all():
            pwc = u.__dict__
        # print("TESTING: ",pwc)

        if not (pwc is None):
            if pwc['password'] == password:
                flash(f"Welcome, {pwc['first_name']}, you have successfully logged in.", "success")
                session['user_id'] = pwc['user_id']
                session['first_name'] = pwc['first_name']
                return redirect("/index")
            else:
                flash("The username and password did not match.", "danger")
        else:
            flash("Sorry, something went wrong.", "danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/theatres", methods=['POST', 'GET'])
def theatres():
    theatreform = TheatreForm()
    if not session.get('first_name'):
        return redirect(url_for('login'))

    if theatreform.is_submitted():
        theatre = theatreform.theatres.data
        for u in db.session.query(Theatres).filter(Theatres.theatre == theatre).all():
            theatre = u.__dict__

        session['theatre_id'] = theatre['theatre_id']

    return render_template("theatres.html", title="Broadway Theatres", theatreform=theatreform, theatres=True)

@app.route("/shows", methods=['POST', 'GET'])
def shows():
    showsform = ShowsForm()

    if not session.get('first_name'):
        return redirect(url_for('login'))

    if showsform.is_submitted():
        show_name = showsform.shows.data
        for u in db.session.query(Shows).filter(Shows.show_name == show_name).all():
            show = u.__dict__

        session['show_id'] = show['show_id']


    return render_template("shows.html", title="Show Data", shows=True, showsform = showsform)

@app.route("/shows_visualize")
def shows_visualize():

    if not session.get('show_id'):
        for u in db.session.query(Grosses).order_by(func.rand()).limit(1):
            random = u.__dict__

        theatreid = random['theatre_id']
        showid = random['show_id']


    if session.get('show_id'):

        showid = session.get('show_id')
        for u in db.session.query(Grosses).filter(Grosses.show_id == showid).order_by(func.rand()).limit(1):
            convert = u.__dict__

        theatreid = convert['theatre_id']

    # query1 = (
    #     "SELECT weekly_gross/potential_gross from Grosses "
    #     "WHERE theatre_id = %d AND show_id = %d AND weekly_gross IS NOT NULL AND potential_gross IS NOT NULL "
    #     "order by performance_id asc") % (theatreid, showid)

    # query2 = (
    #     "SELECT COUNT(performance_id) AS 'Weeks Performing', MIN(weekly_gross/potential_gross) AS Min, MAX(weekly_gross/potential_gross) AS Max, AVG(weekly_gross/potential_gross) AS Average from Grosses "
    #     "WHERE theatre_id = %d AND show_id = %d "
    #     "ORDER BY performance_id DESC "
    #     "Limit 5 ") % (theatreid, showid)


    query1 = (
        "SELECT pct_capacity from Grosses "
        "WHERE theatre_id = %d AND show_id = %d AND pct_capacity <> 0 "
        "order by performance_id asc") % (theatreid, showid)

    query2 = (
        "SELECT COUNT(performance_id) AS 'Weeks Performing', MIN(pct_capacity) AS Min, MAX(pct_capacity) AS Max, AVG(pct_capacity) AS Average from Grosses "
        "WHERE theatre_id = %d AND show_id = %d AND pct_capacity <> 0 "
        "ORDER BY performance_id DESC "
        "Limit 5 ") % (theatreid, showid)

    print("THEATRE ID: ", theatreid," SHOW ID: ", showid)

    # Get Graph Data Frames
    df1 = pd.read_sql_query(query1,cnx)
    df2 = pd.read_sql_query(query2,cnx)
    print(df2)
    xmax = df2['Weeks Performing'].values
    # xmax = 51

    # Plot Min/Max/Average
    plt.plot(df1)
    plt.axhline(df2['Min'].values,color='red',ls='--')
    plt.axhline(df2['Max'].values,color='green',ls='--')
    plt.axhline(df2['Average'].values,color='blue',ls='--')

    # Axis Names
    plt.xlabel("Weeks Performing")
    plt.ylabel("Weekly Gross Potential")

    # Pull Super Title Information
    for u in db.session.query(Theatres).filter(Theatres.theatre_id == theatreid).all():
        theatre = u.__dict__
    for u in db.session.query(Shows).filter(Shows.show_id == showid).all():
        show = u.__dict__

    # Pull Title Information
    minshow = df2['Min'].values
    maxshow = df2['Max'].values
    avgshow = df2['Average'].values

    print(minshow, maxshow)

    plt.suptitle(f"{show['show_name']} - {theatre['theatre']}")
    plt.title(f"Min: {minshow} - Max: {maxshow} - Average: {avgshow}")
    plt.yticks(np.arange(0,1.1,.1))
    if xmax <=30:
        plt.xticks(np.arange(0,xmax,1))
    img2 = BytesIO()
    plt.savefig(img2)
    img2.seek(0)
    plt.close()

    return send_file(img2,mimetype='img/png')

@app.route("/theatres_visualize")
def theatres_visualize():


    if not session.get('theatre_id'):
        for u in db.session.query(Grosses).order_by(func.rand()).limit(1):
            random = u.__dict__

        theatre_theatreid = random['theatre_id']


    else:
        for u in db.session.query(Grosses).filter(Grosses.theatre_id == session.get('theatre_id')).limit(1):
            random = u.__dict__

        theatre_theatreid = random['theatre_id']

    print("THEATRE ID: ", theatre_theatreid)

    query1 = (
        "SELECT AVG(weekly_gross/potential_gross) AS Avg from Grosses "
        "WHERE theatre_id = %d AND weekly_gross IS NOT NULL AND potential_gross IS NOT NULL ") % (theatre_theatreid)

   # Only Used for Print
    query2 = (
        "SELECT show_name, MIN(weekly_gross/potential_gross) AS Min, MAX(weekly_gross/potential_gross) AS Max, AVG(weekly_gross/potential_gross) AS Avg from Grosses "
        "JOIN shows on shows.show_id = grosses.show_id "
        "WHERE theatre_id = %d AND weekly_gross IS NOT NULL AND potential_gross IS NOT NULL "
        "GROUP BY grosses.show_id "
        "ORDER BY performance_id DESC ") % (theatre_theatreid)

    # Get Graph Data Frames
    df1 = pd.read_sql_query(query1,cnx)
    df2 = pd.read_sql_query(query2,cnx)
    print(df2)

        # Pull Super Title Information
    for u in db.session.query(Theatres).filter(Theatres.theatre_id == theatre_theatreid).all():
        theatre = u.__dict__

    minimum = df2['Min']
    maxmimum = df2['Max']
    average = df2['Avg']
    names = df2['show_name']
    theatre_avg = df1['Avg'].values

    plt.figure(figsize = (8,10))

    plt.axvline(theatre_avg, color = 'black', ls='--')
    # plt.barh(range(len(maxmimum)), maxmimum, color = 'green')
    plt.barh(range(len(average)), average, tick_label = names)
    # plt.barh(range(len(minimum)), minimum, color = 'red')
    plt.suptitle(f"{theatre['theatre']}")
    plt.title(f"Theatre Average: {theatre_avg}")
    plt.xlabel("Average Potential")
    plt.ylabel("Show Name")


    plt.xticks(np.arange(0,1.1,.1))
    plt.tight_layout()

    img2 = BytesIO()
    plt.savefig(img2)
    img2.seek(0)
    plt.close()

    return send_file(img2,mimetype='img/png')

# @app.route("/shows_visualize2")
# def shows_visualize2():

    if not session.get('show_id'):
        for u in db.session.query(Grosses).order_by(func.rand()).limit(1):
            random = u.__dict__

        theatreid = random['theatre_id']
        showid = random['show_id']


    if session.get('show_id'):

        showid = session.get('show_id')
        for u in db.session.query(Grosses).filter(Grosses.show_id == showid).order_by(func.rand()).limit(1):
            convert = u.__dict__

        theatreid = convert['theatre_id']

    query3 = (
        "SELECT pct_capacity from Grosses "
        "WHERE theatre_id = %d AND show_id = %d AND pct_capacity <> 0 "
        "order by performance_id asc") % (theatreid, showid)

    query4 = (
        "SELECT COUNT(performance_id) AS 'Weeks Performing', MIN(pct_capacity) AS Min, MAX(pct_capacity) AS Max, AVG(pct_capacity) AS Average from Grosses "
        "WHERE theatre_id = %d AND show_id = %d AND pct_capacity <> 0 "
        "ORDER BY performance_id DESC "
        "Limit 5 ") % (theatreid, showid)

    print("THEATRE ID: ", theatreid," SHOW ID: ", showid)

    # Get Graph Data Frames
    df1 = pd.read_sql_query(query3,cnx)
    df2 = pd.read_sql_query(query4,cnx)
    print(df2)
    xmax = df2['Weeks Performing'].values
    # xmax = 51

    # Plot Min/Max/Average
    plt.plot(df1)
    plt.axhline(df2['Min'].values,color='red',ls='--')
    plt.axhline(df2['Max'].values,color='green',ls='--')
    plt.axhline(df2['Average'].values,color='blue',ls='--')

    # Axis Names
    plt.xlabel("Weeks Performing")
    plt.ylabel("Weekly Gross Potential")

    # Pull Super Title Information
    for u in db.session.query(Theatres).filter(Theatres.theatre_id == theatreid).all():
        theatre = u.__dict__
    for u in db.session.query(Shows).filter(Shows.show_id == showid).all():
        show = u.__dict__

    # Pull Title Information
    minshow = df2['Min'].values
    maxshow = df2['Max'].values
    avgshow = df2['Average'].values

    print(minshow, maxshow)

    plt.suptitle(f"{show['show_name']} - {theatre['theatre']}")
    plt.title(f"Min: {minshow} - Max: {maxshow} - Average: {avgshow}")
    plt.yticks(np.arange(0,1.1,.1))
    if xmax <=30:
        plt.xticks(np.arange(0,xmax,1))
    img2 = BytesIO()
    plt.savefig(img2)
    img2.seek(0)
    plt.close()

    return send_file(img2,mimetype='img/png')
