import httpx
from fastmcp import FastMCP

PET_API_BASE = httpx.AsyncClient(base_url="https://petstore3.swagger.io/api/v3")
PET_OPENAPI_URL = httpx.get("https://petstore3.swagger.io/api/v3/openapi.json").json()

mcp = FastMCP.from_openapi(
    openapi_spec=PET_OPENAPI_URL,
    client=PET_API_BASE,
    name="PetServer"
)

if __name__ == "__main__":
    mcp.run(transport="http", port=8000, host="127.0.0.1")
