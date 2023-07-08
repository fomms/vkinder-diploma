import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class UserVKTinder(Base):

    __tablename__ = 'UserVKTinder'

    user_vktinder_id = sq.Column(sq.Integer)
    user_vk_id = sq.Column(sq.Integer, unique=True, primary_key=True)
    user_vktinder_name = sq.Column(sq.String(length=20))
    user_vktinder_surname = sq.Column(sq.String(length=30))
    user_vktinder_age = sq.Column(sq.Integer)

    def __str__(self):
        return f'{self.user_vktinder_id}, {self.user_vk_id}, {self.user_vktinder_name}, {self.user_vktinder_surname}, {self.user_vktinder_age}'


class SearhPair(Base):
    __tablename__ = 'SearhPair'

    searh_pair_id = sq.Column(sq.Integer, primary_key=True)
    searh_pair_name = sq.Column(sq.String(length=30))
    searh_pair_surname = sq.Column(sq.String(length=30))
    searh_pair_page_link = sq.Column(sq.String)
    searh_pair_vk_id = sq.Column(sq.Integer)
    attribute = sq.Column(sq.Integer)
    user_vktinder_id = sq.Column(sq.Integer, sq.ForeignKey("UserVKTinder.user_vk_id"))
    UserVKTinder = relationship(UserVKTinder, backref="SearhPair")

    def __str__(self):
        return f'{self.searh_pair_id}, {self.searh_pair_name}, {self.searh_pair_surname}, {self.searh_pair_page_link}, {self.searh_pair_vk_id}, {self.attribute}, {self.user_vktinder_id}'


class SearhPairPhoto(Base):

    __tablename__ = 'SearhPairPhoto'

    searh_pair_photo_id = sq.Column(sq.Integer, primary_key=True)
    searh_pair_id = sq.Column(sq.Integer, sq.ForeignKey("SearhPair.searh_pair_id"))
    photo_1 = sq.Column(sq.String)
    photo_2 = sq.Column(sq.String)
    photo_3 = sq.Column(sq.String)
    SearhPair = relationship(SearhPair, backref="SearhPairPhoto")

    def __str__(self):
            return f'{self.searh_pair_photo_id}, {self.searh_pair_vk_id}, {self.photo_1}, {self.photo_2}, {self.photo_3}'


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)