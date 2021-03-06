from wtforms import Form
from wtforms.fields import simple,html5
from wtforms import validators
from wtforms import widgets

class LoginForm(Form):
    username = simple.StringField(
        validators=[
            validators.DataRequired(message='用户名不能为空.')
        ],
        widget=widgets.TextInput(),

    )
    password = simple.PasswordField(
        validators=[
            validators.DataRequired(message='密码不能为空.'),
            validators.Length(min=8, message='密码长度必须大于%(min)d'),

        ],
        widget=widgets.PasswordInput(),
    )

class RegisterForm(Form):
    username = simple.StringField(
        validators=[
            validators.DataRequired(message='用户名不能为空.')
        ],
        widget=widgets.TextInput(),

    )
    password = simple.PasswordField(
        validators=[
            validators.DataRequired(message='密码不能为空.'),
            validators.Length(min=8, message='密码长度必须大于%(min)d'),

        ],
        widget=widgets.PasswordInput(),
    )

class RoomCreateForm(Form):
    roomname = simple.StringField(
        validators=[
            validators.DataRequired(message='房間名不能为空.'),
            validators.Length(min=2, message='房間名长度必须大于%(min)d'),
        ],
        widget=widgets.TextInput(),

    )
