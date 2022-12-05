
from flask_sqlalchemy import SQLAlchemy

import config as cfg



db = SQLAlchemy()


class _CRUD:
    @classmethod
    def create_with_form(cls, **kwargs):
        kwargs.pop("csrf_token", None)
        return cls(**kwargs)

    def update(self, *, commit=True, **kwargs):
        for attr in kwargs:
            if hasattr(self, attr) or hasattr(self.__class__, attr):
                setattr(self, attr, kwargs.get(attr))
        return self.save(commit=commit)

    def add(self, commit=True):
        db.session.add(self)
        return self.save(commit=commit)

    def delete(self, commit=True):
        db.session.delete(self)
        return self.save(commit=commit)

    def save(self, commit=True):
        if commit:
            db.session.commit()
        return self

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    complete = db.Column(db.Boolean, nullable=False)
    cat_id = db.Column(db.Integer, db.ForeignKey("categories.id"))

    def __repr__(self):
        return "<Task: %s>" % (self.title)


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    tasks = db.relationship("Task", backref="categories", lazy="dynamic")

    def __repr__(self):
        return "<Category: %s>" % (self.name)

