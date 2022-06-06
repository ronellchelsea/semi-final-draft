from dataclasses import dataclass
from data import products
from re import L
from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'BLISHOPkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)

class RegisterForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})


    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()

        if existing_user_username:
            raise ValidationError(
                'That username already exists. Please choose a different one.')


class LoginForm(FlaskForm):
    username = StringField(validators=[
                           InputRequired(), Length(min=4, max=20)], render_kw={"placeholder": "Username"})

    password = PasswordField(validators=[
                             InputRequired(), Length(min=8, max=20)], render_kw={"placeholder": "Password"})

    submit = SubmitField('Login')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('order'))
    return render_template('login.html', form=form) 


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@ app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():   
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

#When clicking Products from the navbar
@app.route('/products')
def products():
    return render_template('products.html')

#When clicking Order Now from the navbar
@app.route('/order_now')
def order():
    print(request.form)
    print(request.form.get("account"))
    return render_template("order.html")

#When clickning Swimsuit/Rash Guard/Sports Bra from the dropdown menu in navbar
@app.route('/swimsuit')
def swimsuit():
    return render_template('swimsuit.html')

@app.route('/rash_guard')
def rash_guard():
    return render_template('rashguard.html')

@app.route('/sports_bra')
def sports_bra():
    return render_template('sportsbra.html')

#When clicking About Us from the navbar
@app.route('/AboutUs')
def AboutUs():
    return render_template('about_us.html')

#When clicking Contact Us from the navba
@app.route('/ContactUs')
def ContactUs():
    return render_template('contact.html')

#item view of swimsuits
@app.route('/swimsuit/valentine')
def valentine():
    return render_template('swimsuit_valentine.html')

@app.route('/swimsuit/beth')
def beth():
    return render_template('swimsuit_beth.html')

@app.route('/swimsuit/tiffany')
def tiffany():
    return render_template('tiffany.html')

@app.route('/swimsuit/shakira')
def shakira():
    return render_template('shakira.html')

@app.route('/swimsuit/poppy')
def poppy():
    return render_template('poppy.html')

#item view of rash guards
@app.route('/rashguard/shakira')
def shakira():
    return render_template('swimsuit_shakira.html')

@app.route('/sportsbra/shelsea')
def shelsea():
    return render_template('shelsea.html')

@app.route('/sportsbra/lianne')
def lianne():
    return render_template('lianne.html')

@app.route('/sportsbra/celine')
def celine():
    return render_template('celine.html')

@app.route('/sportsbra/athena')
def athena():
    return render_template('athena.html')

#item view of rash guards
@app.route('/rashguard/aritha')
def aritha():
    return render_template('aritha.html')

@app.route('/rashguard/amethyst')
def amethyst():
    return render_template('amethyst.html')

@app.route('/rashguard/oceana')
def oceana():
    return render_template('oceana.html')

@app.route('/rashguard/luxe')
def luxe():
    return render_template('luxe.html')

if __name__ == '__main__':
    app.run(debug=True)
