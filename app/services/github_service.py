import httpx

GITHUB_API = "https://api.github.com/repos"

async def fetch_repo(owner: str, repo: str):
    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get(f"{GITHUB_API}/{owner}/{repo}")
        response.raise_for_status()
        return response.json()
