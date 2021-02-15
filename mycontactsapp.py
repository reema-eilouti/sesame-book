from flask import Flask, request, render_template, session, url_for, session, redirect, flash 
from datetime import timedelta 
import datetime
from functools import wraps

myapp = Flask(__name__)

user = None

today = datetime.date.today()

myapp.secret_key = ".13456356sdfHello"
# myapp.permanent_session_lifetime = timedelta(days=1)

contacts_dictionary={
    "contact":[ {"name" : "Elmo","phone_number":"0785121254"},
                {"name" : "CookieMonster","phone_number":"0775292323"},
                {"name" : "Bert","phone_number":"0779632147"},
                {"name" : "Ernie","phone_number":"079512789"},
                {"name" : "kermit the Frog","phone_number":"0775893214"}
			]}


def login_required(f):
    @wraps(f)

    
    def check(*args, **kwargs):
        

        if 'user' in session:
            return f(*args, **kwargs)
            
        else:

            return redirect(url_for('login' , next=request.url))
            
    return check

        

# def login_required(f):
#     @wraps(f)
#     def decorated_function(*args, **kwargs):
#         if 'user' not in session:
#             return redirect(url_for('login', next=request.url))
#         return f(*args, **kwargs)
#     return decorated_function



@myapp.route('/')
def home():
    return render_template('home.html')


@myapp.route('/view/<int:index>')
def view(index):
    view_contact = contacts_dictionary['contact'][index -1]
    return render_template('view.html', contact = view_contact,  today = today )

    

@myapp.route('/delete/<int:index>')
def delete(index):
    contacts_dictionary['contact'].pop(index - 1)
    return redirect(url_for("contact_book"))



@myapp.route('/edit/<int:index>', methods=['GET','POST'])
def edit(index):
    if request.method == 'GET':
        view_contact = contacts_dictionary['contact'][index -1]
        return render_template('edit.html', contact = view_contact,  today = today )
    else:
        new_contact = request.form['newname']
        new_number = request.form['newnumber']
        contacts_dictionary['contact'][index -1].update({'name':new_contact,'phone_number':new_number})
        return redirect(url_for('contact_book'))

    




@myapp.route('/add', methods=["POST","GET"])
def add():
    if request.method == "GET":
        return render_template('add.html')
    else:
        contactname = request.form['contactname']
        contactnumber = request.form['contactnumber']
        contacts_dictionary['contact'].append({'name':contactname,'phone_number':contactnumber})
        return redirect(url_for('contact_book'))



@myapp.route('/profile')
@login_required
def profile():

    return render_template('profile.html', user = user)



@myapp.route('/contacts')
@login_required
def contact_book():
    return render_template('contacts.html',user=user, dictionary=contacts_dictionary)

    


@myapp.route('/about')
def about_us():
    return render_template('about.html')



@myapp.route("/login", methods = ["POST" , "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        # session.permanent = True
        global user
        user = request.form["username"]
        password = request.form["password"]
        next_url = request.form["next_url"]
        session["user"] = user
        # session["password"] = password
        flash("You were successfully logged in.", "info")
        return redirect(next_url)




@myapp.route('/logout')
def logout():
    session.clear()
    flash("You were successfully logged out." , "info")
    return redirect(url_for("login"))



if __name__ == '__main__':
    myapp.run(debug=True)