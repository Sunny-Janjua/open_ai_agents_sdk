"""06 Beginner: Unit conversion server."""

from _compat import MCPServer

mcp = MCPServer("server-06-unit-converter")


@mcp.tool()
def celsius_to_fahrenheit(celsius: float) -> float:
    return (celsius * 9 / 5) + 32


@mcp.tool()
def fahrenheit_to_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5 / 9


@mcp.tool()
def km_to_miles(km: float) -> float:
    return km * 0.621371


@mcp.tool()
def miles_to_km(miles: float) -> float:
    return miles / 0.621371


if __name__ == "__main__":
    mcp.run(transport="stdio")

