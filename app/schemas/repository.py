from pydantic import BaseModel, HttpUrl, ConfigDict

class RepositoryCreate(BaseModel):
    owner: str
    repo_name: str

class RepositoryUpdate(BaseModel):
    stars: int

class RepositoryResponse(BaseModel):
    # Pydantic v2 config
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    owner: str
    stars: int
    url: HttpUrl
