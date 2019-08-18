""" Flask App
"""
import getpass

import click
from flask.cli import with_appcontext

from config import Config
from iot import create_app, db, socketio
from iot.models.user import User

app = create_app(Config)


@app.cli.command()
@with_appcontext
def create_user():
    """ Create a new account.
    """
    username = input('Please enter your username: ')
    if db.session.query(User).filter(User.username == username).first():
        click.echo('This username is already exist, please use another one')
        return
    while True:
        password = getpass.getpass('Please enter your password: ')
        password2 = getpass.getpass('Please enter your password again: ')
        if password == password2:
            break
        print('Password mismatch, please try again')

    email = input('Please enter your email: ')
    if db.session.query(User).filter(User.email == email).first():
        click.echo('This Email has been used, please use another one')
    else:
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        click.echo('Account Created')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', log_output=True)
