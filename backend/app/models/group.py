from .. import db
from sqlalchemy import Enum

class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(100), nullable=False)
    owner = db.relationship('User', backref='owned_groups')

class GroupMember(db.Model):
    __tablename__ = 'group_members'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id'), primary_key=True)
    role = db.Column(Enum('owner', 'admin', 'member'), default='member')
    user = db.relationship('User', backref='group_memberships')
    group = db.relationship('Group', backref='members') 