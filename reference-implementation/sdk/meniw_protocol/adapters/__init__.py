"""Adapters that wire the Meniw gate into the places where agent tool-calls actually run.

Each adapter is dependency-light: the optional framework (openai / langchain / mcp) is
imported lazily inside the function, so importing this package never requires them.
"""
from .openai_tools import guard_openai_tool_call
from .langchain_tool import governed_tool
from .mcp_gateway import guard_mcp_call

__all__ = ["guard_openai_tool_call", "governed_tool", "guard_mcp_call"]
