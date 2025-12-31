from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(100))

    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    category = Column(String(50))  # 新增：分类
    tags = Column(String(200))     # 新增：标签（逗号分隔字符串）
    content = Column(Text)
    created_at = Column(String(50)) # 新增：创建时间字符串
    year = Column(String(10))       # 新增：年份
    date = Column(String(20))       # 新增：日期 (MM.DD)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    post_id = Column(Integer, ForeignKey("posts.id"))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")
