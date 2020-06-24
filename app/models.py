from app import db
import  datetime
import uuid


class Tournament(db.Model):
    id = db.Column(db.CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(30))
    roles = db.relationship('Role', backref='tournament', passive_deletes=True)


roles_users = db.Table('roles_users',
        db.Column('user_id', db.CHAR(36), db.ForeignKey('user.id', ondelete='CASCADE')),
        db.Column('role_id', db.CHAR(36), db.ForeignKey('role.id', ondelete='CASCADE')))

class Role(db.Model):
    id = db.Column(db.CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))
    type = db.Column(db.String(10), unique=False)
    tournament_id = db.Column(db.CHAR(36), db.ForeignKey('tournament.id', ondelete='CASCADE'))


class User(db.Model):
    id = db.Column(db.CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True)
    firstname = db.Column(db.String(80), unique=False)
    lastname = db.Column(db.String(80), unique=False)
    activision_id = db.Column(db.String(80), unique=False)
    stream_url = db.Column(db.String(255), unique=False)
    stream_type = db.Column(db.String(25), unique=False)
    avatar_url = db.Column(db.String(255), unique=False)
    dob = db.Column(db.Date, nullable=False)
    gender = db.Column(db.CHAR(1), default='u')
    registration_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    password = db.Column(db.Text)
    account_verified = db.Column(db.Boolean, default=False)
    roles = db.relationship('Role',
                            secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    is_active = db.Column(db.Boolean, default=True)
    otp = db.relationship('UserOTP', backref='user', passive_deletes=True)

    @property
    def rolenames(self):
        role_list = []
        if len(self.roles) == 0:
            return role_list
        else:
            for role in self.roles:
                role_list.append(role.name)
            return role_list

    @classmethod
    def lookup(cls, username):
        return cls.query.filter_by(username=username).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    @property
    def identity(self):
        return self.id

    def is_valid(self):
        return self.is_active

    @property
    def organizers_of_tournaments(self):
        role_list = []
        if len(self.roles) == 0:
            return role_list
        else:
            for role in self.roles:
                if role.type == 'organizers':
                    role_list.append(role.tournament_id)
            return role_list

    @property
    def participants_of_tournaments(self):
        role_list = []
        if len(self.roles) == 0:
            return role_list
        else:
            for role in self.roles:
                if role.type == 'participants':
                    role_list.append(role.tournament_id)
            return role_list


class UserOTP(db.Model):
    __tablename__ = "user_otp"
    id = db.Column(db.CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    type = db.Column(db.String(10), unique=False)
    code = db.Column(db.String(10), unique=False)
    sg_message_id = db.Column(db.String(30), unique=False)
    reg_exp_date = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    exp_time = db.Column(db.DateTime, default=reg_exp_date)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # https://stackoverflow.com/questions/5033547/sqlalchemy-cascade-delete
    user_id = db.Column(db.CHAR(36), db.ForeignKey('user.id', ondelete='CASCADE'))






# Events
@db.event.listens_for(Tournament, "after_insert")
def create_roles_for_tournament(mapper, connection, target):
    role = Role.__table__
    connection.execute(role.insert().values(name="{}-participants".format(target.id),
                                            description="{} - Participants".format(target.name),
                                            type="participants",
                                            tournament_id=target.id))
    connection.execute(role.insert().values(name="{}-organizers".format(target.id),
                                            description="{} - Organizers".format(target.name),
                                            type="organizers",
                                            tournament_id=target.id))






