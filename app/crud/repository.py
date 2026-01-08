from sqlalchemy.orm import Session
from app.models.repository import Repository

def create_repo(db: Session, data: dict):
    repo = Repository(**data)
    db.add(repo)
    db.commit()
    db.refresh(repo)
    return repo

def get_repo(db: Session, repo_id: int):
    return db.query(Repository).filter(Repository.id == repo_id).first()

def delete_repo(db: Session, repo: Repository):
    db.delete(repo)
    db.commit()
