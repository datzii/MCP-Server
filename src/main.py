import os
import json
import time
import uvicorn
import common.config as config
from mcp.server.fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.responses import JSONResponse
from service.brain_tumor_diagnosis import classify_brain_tumor_from_MRI_function

settings = dict(
    host = config.server_host,
    port = int(config.server_port),
    log_level = config.server_log_level
)

# Create the MCP Server
mcp = FastMCP("mcp-server-brain-tumor-diagnosis", settings = settings)

@mcp.tool()
def classify_brain_tumor_from_MRI(file_path: str) -> str:
    """
    Get the prediction and classification of brain tumor over a MRI Image

    Args:
        file_path (str): the file path where the MRI Image is
    
    Returns:
        str: The label and confidence value of the prediction
    """
    return classify_brain_tumor_from_MRI_function(file_path)



# Endpoints functions
def create_starlette_app(mcp_server: FastMCP, *, debug: bool=False) -> Starlette:

    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,
        ) as (read_stream, write_stream):
            await mcp_server._mcp_server.run(
                read_stream,
                write_stream,
                mcp_server._mcp_server.create_initialization_options()
            )

    async def handle_status(request: Request) -> None:
        start = time.time()
        took_ms = round((time.time()-start)*1000) + 1
        return JSONResponse(dict(kudos="up", took_ms=took_ms))
    
    async def handle_list_tools(request: Request) -> None:
        tools = await mcp_server.list_tools()
        return JSONResponse([tool.__dict__ for tool in tools])
    
    return Starlette(
        debug=debug,
        routes=[
            Route("/v1/status/", methods=['GET', 'OPTIONS'], endpoint=handle_status),
            Route("/v1/tools/", methods=['GET', 'OPTIONS'], endpoint=handle_list_tools),

            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message)
        ]
    )

if __name__ == "__main__":
    print(f"MCP Server running - Port {config.server_port}")
    starlette_app = create_starlette_app(mcp, debug=True)
    uvicorn.run(starlette_app, host = settings["host"], port=settings["port"])