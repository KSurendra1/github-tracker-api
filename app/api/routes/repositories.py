from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.repository import *
from app.services.github_service import fetch_repo
from app.core.database import get_db
from app.crud import repository as crud

router = APIRouter(prefix="/repositories", tags=["Repositories"])

@router.post("/", response_model=RepositoryResponse, status_code=201)
async def create_repository(payload: RepositoryCreate, db: Session = Depends(get_db)):
    data = await fetch_repo(payload.owner, payload.repo_name)
    repo_data = {
        "name": data["name"],
        "owner": data["owner"]["login"],
        "stars": data["stargazers_count"],
        "url": data["html_url"],
    }
    return crud.create_repo(db, repo_data)

@router.get("/{repo_id}", response_model=RepositoryResponse)
def read_repository(repo_id: int, db: Session = Depends(get_db)):
    repo = crud.get_repo(db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    return repo

@router.put("/{repo_id}", response_model=RepositoryResponse)
def update_repository(repo_id: int, payload: RepositoryUpdate, db: Session = Depends(get_db)):
    repo = crud.get_repo(db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    repo.stars = payload.stars
    db.commit()
    db.refresh(repo)
    return repo

@router.delete("/{repo_id}", status_code=204)
def delete_repository(repo_id: int, db: Session = Depends(get_db)):
    repo = crud.get_repo(db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    crud.delete_repo(db, repo)
