from fastapi import FastAPI, Depends, HTTPException, status, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
import shutil
import os
import uuid

from . import models, database

# --- 配置 ---
SECRET_KEY = "your-secret-key-keep-it-secret" # 生产环境应从环境变量获取
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- 安全工具 ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="token", auto_error=False)

# --- 数据库初始化 ---
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

# Ensure uploads directory exists
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# --- Pydantic 模型 ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True

class PostCreate(BaseModel):
    title: str
    content: str
    category: Optional[str] = "LOG"
    tags: Optional[str] = ""

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    category: Optional[str]
    tags: Optional[str]
    created_at: Optional[str]
    year: Optional[str]
    date: Optional[str]
    views: int = 0
    likes: int = 0
    is_liked: bool = False
    owner_id: int
    owner: UserResponse
    class Config:
        orm_mode = True

class PostListResponse(BaseModel):
    items: List[PostResponse]
    total: int

class CommentCreate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    owner_id: int
    post_id: int
    owner: UserResponse

    class Config:
        orm_mode = True

# --- 辅助函数 ---
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

async def get_current_user_optional(token: Optional[str] = Depends(oauth2_scheme_optional), db: Session = Depends(database.get_db)):
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
    except JWTError:
        return None
    user = db.query(models.User).filter(models.User.username == token_data.username).first()
    return user

# --- 路由 ---

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI Backend with MySQL"}

@app.get("/health")
def read_health():
    return {"status": "ok"}

# 注册
@app.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 登录 (获取 Token)
@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 获取当前用户
@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# 新增文章 (需要登录)
@app.post("/posts/", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    now = datetime.now()
    db_post = models.Post(
        title=post.title, 
        content=post.content,
        category=post.category,
        tags=post.tags,
        created_at=now.strftime("%Y-%m-%d %H:%M:%S"), # 更精确的时间格式
        year=str(now.year),
        date=f"{now.month}.{now.day}",
        owner_id=current_user.id,
        views=0,
        likes=0
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

from sqlalchemy import or_, desc, asc

# 获取文章列表 (公开)
@app.get("/posts/", response_model=PostListResponse)
def read_posts(
    skip: int = 0, 
    limit: int = 10, 
    q: Optional[str] = None,
    sort_by: Optional[str] = "date", # date, views, likes
    order: Optional[str] = "desc",
    db: Session = Depends(database.get_db)
):
    query = db.query(models.Post)
    
    if q:
        search = f"%{q}%"
        query = query.filter(
            or_(
                models.Post.title.like(search),
                models.Post.content.like(search),
                models.Post.tags.like(search),
                models.Post.category.like(search)
            )
        )
    
    if sort_by == "views":
        sort_attr = models.Post.views
    elif sort_by == "likes":
        sort_attr = models.Post.likes
    else: # date
        sort_attr = models.Post.id
        
    if order == "asc":
        query = query.order_by(asc(sort_attr))
    else:
        query = query.order_by(desc(sort_attr))
        
    total = query.count()
    posts = query.offset(skip).limit(limit).all()
    return {"items": posts, "total": total}

# 更新文章 (需要登录且是作者)
@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post: PostCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
    db_post.title = post.title
    db_post.content = post.content
    db_post.category = post.category
    db_post.tags = post.tags
    db.commit()
    db.refresh(db_post)
    return db_post

# 删除文章 (需要登录且是作者)
@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if db_post.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    db.delete(db_post)
    db.commit()
    return {"message": "Post deleted successfully"}

# 获取单篇文章详情 (公开，增加浏览量)
@app.get("/posts/{post_id}", response_model=PostResponse)
def read_post(post_id: int, db: Session = Depends(database.get_db), current_user: Optional[models.User] = Depends(get_current_user_optional)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 增加浏览量
    post.views += 1
    db.commit()
    db.refresh(post)

    # Check if liked by current user
    post.is_liked = False
    if current_user:
        if db.query(models.PostLike).filter(models.PostLike.post_id == post_id, models.PostLike.user_id == current_user.id).first():
            post.is_liked = True

    return post

# 点赞/取消点赞文章 (需要登录)
@app.post("/posts/{post_id}/like")
def like_post(post_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Check if already liked
    existing_like = db.query(models.PostLike).filter(models.PostLike.post_id == post_id, models.PostLike.user_id == current_user.id).first()
    
    if existing_like:
        # Unlike
        db.delete(existing_like)
        post.likes = max(0, post.likes - 1)
        is_liked = False
    else:
        # Like
        new_like = models.PostLike(post_id=post_id, user_id=current_user.id)
        db.add(new_like)
        post.likes += 1
        is_liked = True

    db.commit()
    return {"likes": post.likes, "is_liked": is_liked}

# 新增评论 (需要登录)
@app.post("/posts/{post_id}/comments/", response_model=CommentResponse)
def create_comment(post_id: int, comment: CommentCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    db_comment = models.Comment(content=comment.content, post_id=post_id, owner_id=current_user.id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

# 获取评论列表 (公开)
@app.get("/posts/{post_id}/comments/", response_model=List[CommentResponse])
def read_comments(post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    comments = db.query(models.Comment).filter(models.Comment.post_id == post_id).offset(skip).limit(limit).all()
    return comments

# 删除评论 (需要登录且是作者)
@app.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    if db_comment.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    db.delete(db_comment)
    db.commit()
    return {"message": "Comment deleted successfully"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), current_user: models.User = Depends(get_current_user)):
    file_extension = os.path.splitext(file.filename)[1]
    # Generate a unique filename
    file_name = f"{uuid.uuid4()}{file_extension}"
    file_path = f"uploads/{file_name}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Return the URL (relative to the server root)
    return {"url": f"/uploads/{file_name}"}

