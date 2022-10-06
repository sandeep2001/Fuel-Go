from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, logout_user
from .models import User, Profile, Quote
from . import db

quote_info = []
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('views.homepage'))
    

@views.route('/profilepage', methods=['GET', 'POST'])
def create_profile():
    if request.method == 'POST':
        full_name = request.form.get('fullname')
        address1 = request.form.get('address1')
        address2 = request.form.get('address2')
        city = request.form.get('city')
        state = request.form.get('state')
        zipcode = request.form.get('zipcode')

        if len(full_name) < 2 or len(full_name) > 50:
            flash('Full name must be greater than 2 and less than 50 characters.', category='error')
        elif len(address1) < 2 or len(address1) > 100:
            flash('Address must be greater than 2 and less than 100 characters.', category='error')
        elif len(city) < 2 or len(city) > 100:
            flash('City must be greater than 2 and less than 100 characters.', category='error')
        elif len(state) != 2:
            flash('Reselect state.', category='error')
        elif len(zipcode) < 5 or len(zipcode) > 9:
            flash('Zipcode must be greater than 5 and no more than 9 characters.', category='error')
        else:
            print("current_user id is :", current_user.id)
            new_user_profile = Profile(full_name=full_name, address1=address1, address2=address2, city=city,
                                       state=state, zipcode=zipcode, user_id=current_user.id)
            db.session.add(new_user_profile)
            db.session.commit()

            flash('Profile created!', category='success')
            return redirect(url_for('views.fuel_quote_form'))

    return render_template("profilepage.html", user=current_user)


@views.route('/fuel-quote', methods=['GET', 'POST'])
def fuel_quote_form():
    user = User.query.get(current_user.id)
    profile_list = user.user_profile
    cur_profile_id = profile_list[0].id
    user_profile = Profile.query.get(cur_profile_id)
    if user_profile.address2 == '':
        user_address = user_profile.address1 + ', ' + user_profile.city
    else:
        user_address = user_profile.address1 + ', ' + user_profile.address2 + ', ' + user_profile.city
    user_state = user_profile.state
    print("the user's address is: ", user_address)
    print("the user's state is: ", user_state)

    if request.method == 'POST':
        request_gallons = request.form.get('Total_Gallons_Requested')
        request_date = request.form.get('delivery_date')
        request_address = request.form.get('delivery_Address')
        quote_history = Quote.query.get(current_user.id)
        if quote_history:
            history_flag = 1
        else:
            history_flag = 0

        quote_result = get_price(user_state, history_flag, int(request_gallons))
        print("suggest price is: ", quote_result[0], "total price is: ", quote_result[1])
        global quote_info
        quote_info = [request_gallons, request_address, request_date, quote_result[0], quote_result[1]]
        flash('Suggest price created!', category='success')
        return redirect(url_for('views.fuel_quote_result'))

    return render_template("quote.html", user=current_user, address=user_address, state=user_state)


@views.route('/fuel-quote-result', methods=['GET', 'POST'])
def fuel_quote_result():
    global quote_info
    print('quote_result ', quote_info)
    if request.method == 'POST':
        
        new_quote_result = Quote(gallons_requested=quote_info[0],
                                 delivery_address=quote_info[1],
                                 date=quote_info[2],
                                 suggest_price=quote_info[3],
                                 total_price=quote_info[4], user_id=current_user.id
                                 )
        db.session.add(new_quote_result)
        db.session.commit()

        flash('Quote result added!', category='success')
        return redirect(url_for('views.fuel_quote_history'))

    return render_template("quote_result.html", user=current_user, gallons_requested=quote_info[0],
                           delivery_address=quote_info[1], delivery_date=quote_info[2], suggest_price=quote_info[3],
                           total_price=quote_info[4])


@views.route('/fuel-quote-history', methods=['GET', 'POST'])
def fuel_quote_history():
    user = User.query.get(current_user.id)
    history_list = user.user_quote
    return render_template("quotehistory.html", user=current_user, history_list=history_list)

@views.route('/homepage', methods=['GET', 'POST'])
def homepage():
    return render_template("homepage.html", user=current_user)

@views.route('/Assignments', methods=['GET', 'POST'])
def Assignments():
    return render_template("Assignments.html", user=current_user)

@views.route('/Aboutus', methods=['GET', 'POST'])
def Aboutus():
    return render_template("AboutUs.html", user=current_user)


@views.route('/home_login_page')
def home_login():
    logout_user()
    return redirect(url_for('auth.login'))


@views.route('/home_registration')
def home_registration():
    logout_user()
    return redirect(url_for('auth.sign_up'))

##########################################################################################
def get_price(state, request_frequent, request_gallons):
    # since we don't need to implement the price module for this assignment,
    # we can just assign hyphons for suggested price and total amount due, and put those into 'results'  
    # Pricing module will be implemented later
 
    results =  ['--', '--']
    
    return results
