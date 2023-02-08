# from flask_wtf import FlaskForm
# from wtforms import StringField,PasswordField,SubmitField

# class RegisterForm(FlaskForm):
#     username=StringField('Username')
#     email=StringField('Email')
#     password1=PasswordField('Password')
#     password2=PasswordField('Confirm Password')
#     submit=SubmitField('Register')
    
    
    
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,FloatField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired,ValidationError
from .models.user import User

class RegisterForm(FlaskForm):
    def validate_username(self, username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Please use a different username.')
    def validate_email(self, email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Please use a different email address.')
            

    
    
    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')
    
    
class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit=SubmitField(label='Login')
    
    
class PurchaseItemForm(FlaskForm):
    submit=SubmitField(label='Purchase Item')


class SellItemForm(FlaskForm):
    submit=SubmitField(label='Sell Item')
    
class AddItemForm(FlaskForm):
    name = StringField(label='ProductName:', validators=[Length(min=2, max=30), DataRequired()])
    barcode = StringField(label='Barcode:', validators=[Length(min=3), DataRequired()])
    price = FloatField(label='Price:', validators=[ DataRequired()])
    submit=SubmitField(label='Add Item')