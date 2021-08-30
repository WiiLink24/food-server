from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from models import CategoryTypes


class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Enter the pantry")


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField("Password", validators=[DataRequired()])
    new_password = PasswordField("New Password", validators=[DataRequired()])
    new_password_confirmation = PasswordField(
        "Confirm New Password", validators=[DataRequired()]
    )
    complete = SubmitField("Complete")

    def validate_current_password(self, _):
        if self.current_password.data == self.new_password.data:
            return ValidationError("New password cannot be the same as current!")

    def validate_new_password(self, _):
        if self.new_password.data != self.new_password_confirmation.data:
            return ValidationError("New passwords must be the same")


class FoodTypes(FlaskForm):
    food = SelectField(
        "Food Types",
        choices=CategoryTypes.choices(),
        coerce=CategoryTypes.coerce,
    )
    next = SubmitField("Next")


class RestaurantEditForm(FlaskForm):
    restaurant_name = StringField("Restaurant Name", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    wait_time = StringField("Wait Time", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    amenity = StringField("Amenity", validators=[DataRequired()])
    phone = StringField("Phone Number", validators=[DataRequired()])
    message = StringField("Message", validators=[DataRequired()])
    logo = FileField("Restaurant logo")
    submit = SubmitField("Edit")


class RestaurantAddForm(FlaskForm):
    restaurant_name = StringField("Restaurant Name", validators=[DataRequired()])
    food_type = SelectField(
        "Food Types",
        choices=CategoryTypes.choices(),
        coerce=CategoryTypes.coerce,
    )
    description = StringField("Description", validators=[DataRequired()])
    wait_time = StringField("Wait Time", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    amenity = StringField("Amenity", validators=[DataRequired()])
    phone = StringField("Phone Number", validators=[DataRequired()])
    message = StringField("Message", validators=[DataRequired()])
    logo = FileField("Restaurant logo", validators=[DataRequired()])
    submit = SubmitField("Submit")


class MenuEditForm(FlaskForm):
    menu_name = StringField("Menu Name", validators=[DataRequired()])
    info = StringField("Info", validators=[DataRequired()])
    submit = SubmitField("Edit")


class MenuAddForm(FlaskForm):
    menu_name = StringField("Menu Name", validators=[DataRequired()])
    info = StringField("Info", validators=[DataRequired()])
    submit = SubmitField("Add")


class ItemEditForm(FlaskForm):
    name = StringField("Food Name", validators=[DataRequired()])
    description = StringField("Food Description", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    image = FileField("Item Image", validators=[DataRequired()])
    submit = SubmitField("Edit")


class ItemAddForm(FlaskForm):
    name = StringField("Food Name", validators=[DataRequired()])
    description = StringField("Food Description", validators=[DataRequired()])
    price = StringField("Price", validators=[DataRequired()])
    image = FileField("Item Image", validators=[DataRequired()])
    submit = SubmitField("Add")


class DeleteForm(FlaskForm):
    given_id = StringField("ID", validators=[DataRequired()])
    submit = SubmitField("Delete")
