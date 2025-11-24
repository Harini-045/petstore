import asyncio
import httpx
from fastmcp import FastMCP

# HOST = "127.0.0.1"
# PORT = 8000

PET_OPENAPI_URL = "https://petstore3.swagger.io/api/v3/openapi.json"
PET_API_BASE = "https://petstore3.swagger.io/api/v3"

TENABLE_OPENAPI_URL = "https://developer.tenable.com/openapi/5c926ae6a9b73900ee2740cb"
TENABLE_API_BASE = "https://www.tenable.com/downloads/api/v2"

async def fetch_spec(url: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        r.raise_for_status()
        return r.json()

async def create_sub_mcp(openapi_url: str, api_base: str, name: str):
    spec = await fetch_spec(openapi_url)
    api_client = httpx.AsyncClient(base_url=api_base, timeout=None)
    sub_mcp = FastMCP.from_openapi(openapi_spec=spec, client=api_client, name=name)
    return sub_mcp, api_client

async def main():
    main_mcp = FastMCP("McpServer1")

    pet_mcp, pet_client = await create_sub_mcp(PET_OPENAPI_URL, PET_API_BASE, "Petstore")
    tenable_mcp, tenable_client = await create_sub_mcp(TENABLE_OPENAPI_URL, TENABLE_API_BASE, "Tenablestore")

    await main_mcp.import_server(pet_mcp, prefix="pet")
    await main_mcp.import_server(tenable_mcp, prefix="tenable")

    loop = asyncio.get_running_loop()
    try:
        # run blocking server in a thread so we can clean up after it stops
        await loop.run_in_executor(None, lambda: main_mcp.run(transport="http", port=8080, endpoint="/mcp", host="127.0.0.1"))
    finally:
        await pet_client.aclose()
        await tenable_client.aclose()

if __name__ == "__main__":
    asyncio.run(main())