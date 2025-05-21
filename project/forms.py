from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Email, EqualTo, Length, Regexp

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100), Regexp(r'^[\w\s-]+$', message="Name must contain only letters, numbers, spaces, or hyphens.")])
    price = FloatField('Price ($/kg)', validators=[DataRequired(), NumberRange(min=0, max=1000, message="Price must be between 0 and 1000.")])
    description = StringField('Description', validators=[DataRequired(), Length(max=500)])
    category = StringField('Category', validators=[DataRequired(), Length(max=50), Regexp(r'^[\w\s-]+$', message="Category must contain only letters, numbers, spaces, or hyphens.")])
    image = StringField('Image', validators=[DataRequired(), Length(max=100), Regexp(r'^[\w-]+\.(jpg|png)$', message="Image must be a valid .jpg or .png filename.")])
    submit = SubmitField('Submit')

class BasketForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=100, message="Quantity must be between 1 and 100.")])
    submit = SubmitField('Update')

class CheckoutForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=100), Regexp(r'^[\w\s-]+$', message="Name must contain only letters, numbers, spaces, or hyphens.")])
    address = StringField('Delivery Address', validators=[DataRequired(), Length(max=200)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20), Regexp(r'^\+?\d{10,15}$', message="Phone number must be 10-15 digits, optionally starting with +.")])
    delivery_option = SelectField('Delivery Option', choices=[
        ('standard', 'Standard ($9.50)'),
        ('express', 'Express ($12.50)'),
        ('green', 'Green ($2.00)')
    ], validators=[DataRequired()])
    submit = SubmitField('Place Order')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=50), Regexp(r'^[\w-]+$', message="Username must contain only letters, numbers, or hyphens.")])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=128, message="Password must be at least 6 characters.")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message="Passwords must match.")])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')