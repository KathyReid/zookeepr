"""The application's model objects"""
import sqlalchemy as sa

from meta import Base

from pylons.controllers.util import abort

from role import Role
from person_role_map import person_role_map

from zookeepr.model.meta import Session

def setup(meta):
    pass

class Voucher(Base):
    __tablename__ = 'voucher'

    id = sa.Column(sa.types.Integer, primary_key=True)
    code = sa.Column(sa.types.Text, nullable=False, unique=True)
    comment = sa.Column(sa.types.Text, nullable=False)
    leader_id = sa.Column(sa.types.Integer, sa.ForeignKey('person.id'),
                                                           nullable=False)
    creation_timestamp = sa.Column(sa.types.DateTime, nullable=False,
                                       default=sa.func.current_timestamp())
    last_modification_timestamp = sa.Column(sa.types.DateTime, nullable=False,
    default=sa.func.current_timestamp(), onupdate=sa.func.current_timestamp())

    def __init__(self, **kwargs):
        # remove the args that should never be set via creation
        super(Proposal, self).__init__(**kwargs)

    def __repr__(self):
        return '<Voucher id="%r" code="%s">' % (self.id, self.code)

    @classmethod
    def find_all(cls):
        return Session.query(Proposal).order_by(Proposal.id).all()
