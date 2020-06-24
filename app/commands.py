import click
from flask.cli import with_appcontext

from .extensions import guard, db
from .models import User, Tournament, Role

@click.command(name='create_database')
@with_appcontext
def create_database():
    db.create_all()

@click.command(name='create_demo_data')
@with_appcontext
def create_demo_data():
    one = User(username='peter@nomail.com', firstname='Peter', lastname='Doe', password=guard.hash_password('password'), gender='m', dob='1991-01-01')
    two = User(username='paul@nomail.com', firstname='Paul', lastname='Smith', password=guard.hash_password('password'), gender='m', dob='1991-12-13')
    three = User(username='paula@nomail.com',  firstname='Paula', lastname='Doe', password=guard.hash_password('password' ), gender='f', dob='1992-01-01')


    db.session.add_all([one, two, three])
    db.session.commit()

    rolenames = ['overlord', 'minion']

    tournament1 = Tournament(name="Demo_Data_Doe")
    tournament2 = Tournament(name="Demo_Data_Smith")

    db.session.add_all([tournament1, tournament2])
    db.session.commit()

    tournament1_overlord = Role.query.filter_by(name="{}-overlord".format(tournament1.id)).first()
    tournament1_minion = Role.query.filter_by(name="{}-minion".format(tournament1.id)).first()
    tournament2_overlord = Role.query.filter_by(name="{}-overlord".format(tournament2.id)).first()
    tournament2_minion = Role.query.filter_by(name="{}-minion".format(tournament2.id)).first()

    # tournament1_overlord = Role(name='{}-{}'.format(tournament1.id, rolenames[0]),
    #                         description='{} - {}'.format(tournament1.name, str(rolenames[0]).capitalize()),
    #                         type=rolenames[0],
    #                         tournament_id=tournament1.id)
    # tournament1_minion = Role(name='{}-{}'.format(tournament1.id, rolenames[1]),
    #                         description='{} - {}'.format(tournament1.name, str(rolenames[1]).capitalize()),
    #                         type=rolenames[1],
    #                         tournament_id=tournament1.id)
    # tournament2_overlord = Role(name='{}-{}'.format(tournament2.id, rolenames[0]),
    #                         description='{} - {}'.format(tournament2.name, str(rolenames[0]).capitalize()),
    #                         type=rolenames[0],
    #                         tournament_id=tournament2.id)
    # tournament2_minion = Role(name='{}-{}'.format(tournament2.id, rolenames[1]),
    #                         description='{} - {}'.format(tournament2.name, str(rolenames[1]).capitalize()),
    #                         type=rolenames[1],
    #                         tournament_id=tournament2.id)
    #
    # db.session.add_all([tournament1_overlord, tournament1_minion, tournament2_overlord, tournament2_minion])
    # db.session.commit()
    #
    tournament1_overlord.users.append(one)
    tournament2_overlord.users.append(two)
    tournament1_minion.users.append(three)
    tournament2_minion.users.append(three)
    db.session.commit()

@click.command(name='delete_demo_data')
@with_appcontext
def delete_demo_data():
    tournament1 = Tournament.query.filter_by(name="Demo_Data_Doe").one_or_none()
    tournament2 = Tournament.query.filter_by(name="Demo_Data_Smith").one_or_none()
    families = [tournament1, tournament2]
    # Remove Users from role
    # Remove Roles
    for tournament in families:
        for role in tournament.roles:
            for user in role.users:
                role.users.remove(user)

            db.session.delete(role)
        db.session.delete(tournament)

    db.session.commit()