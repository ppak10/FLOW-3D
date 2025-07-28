from mcp.server.fastmcp import FastMCP

def register_resources(app: FastMCP):
    @app.resource("search")
    def search() -> str:
        print("searching...")
        return "searching..."

    return search
