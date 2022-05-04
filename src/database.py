from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import BigInteger, Integer


db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(BigInteger().with_variant(
        Integer, 'sqlite'), primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    mobile = db.Column(db.BigInteger)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    posts = db.relationship('Posts', backref='users', lazy=True)

    def __repr__(self):
        return "User email:{self.email}"


class Posts(db.Model):
    id = db.Column(BigInteger().with_variant(
        Integer, 'sqlite'), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    published = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    published_at = db.Column(db.DateTime, default=datetime.now())
    author_id = db.Column(
        db.BigInteger, db.ForeignKey('users.id'), nullable=False
    )
    comments = db.relationship(
        'PostComments', backref='post_comments', lazy=True)

    def __repr__(self):
        return "Post id:{self.id}"


class PostComments(db.Model):
    id = db.Column(BigInteger().with_variant(
        Integer, 'sqlite'), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text())
    published = db.Column(db.Integer(), default=0)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    published_at = db.Column(db.DateTime, default=datetime.now())
    post_id = db.Column(
        db.BigInteger, db.ForeignKey('posts.id'), nullable=False
    )

    def __repr__(self):
        return "Post Comment id:{self.id}"


class Category(db.Model):
    id = db.Column(BigInteger().with_variant(
        Integer, 'sqlite'), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text())
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    def __repr__(self):
        return "Category id:{self.id}"


class PostCategory(db.Model):
    __tablename__ = 'post_category'
    __table_args__ = (
        db.PrimaryKeyConstraint('post_id', 'category_id'),
    )

    post_id = db.Column(
        db.BigInteger, db.ForeignKey('posts.id'), primary_key=True
    )
    category_id = db.Column(
        db.BigInteger, db.ForeignKey('category.id'), primary_key=True
    )
