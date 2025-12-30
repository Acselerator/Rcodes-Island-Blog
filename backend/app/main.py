from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List

from . import models, database

# 创建数据库表 (生产环境通常使用 Alembic 进行迁移，这里为了简单直接创建)
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Pydantic 模型 (用于请求体和响应体验证)
class PostCreate(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        orm_mode = True

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend with MySQL"}

@app.get("/health")
def read_health():
    return {"status": "ok"}

# 新增文章
@app.post("/posts/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(database.get_db)):
    db_post = models.Post(title=post.title, content=post.content)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

# 获取文章列表
@app.get("/posts/", response_model=List[PostResponse])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts
