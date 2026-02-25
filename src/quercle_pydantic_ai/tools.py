"""Quercle tools for Pydantic AI agents."""

from __future__ import annotations

import json
from typing import Any

from pydantic_ai.tools import Tool
from pydantic_ai.toolsets import FunctionToolset
from quercle import (
    AsyncQuercleClient,
    tool_metadata,
)
from quercle.models import ExtractBodyFormat, RawFetchBodyFormat, RawSearchBodyFormat


def quercle_search_tool(
    api_key: str | None = None,
    allowed_domains: list[str] | None = None,
    blocked_domains: list[str] | None = None,
    timeout: float | None = None,
) -> Tool[Any]:
    """Create a Quercle web search tool for Pydantic AI agents.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        allowed_domains: Only include results from these domains.
        blocked_domains: Exclude results from these domains.
        timeout: Request timeout in seconds.

    Returns:
        A Pydantic AI Tool configured for web search.
    """
    client: AsyncQuercleClient | None = None

    async def quercle_search(query: str) -> str:
        nonlocal client
        if client is None:
            client = AsyncQuercleClient(api_key=api_key)
        return (await client.search(
            query,
            allowed_domains=allowed_domains,
            blocked_domains=blocked_domains,
            timeout=timeout,
        )).result

    # Set docstring dynamically using imported descriptions
    quercle_search.__doc__ = f"""Search the web and get AI-synthesized answers with citations.

    Args:
        query: {tool_metadata["search"]["parameters"]["query"]}

    Returns:
        AI-synthesized answer with source citations.
    """

    return Tool(
        quercle_search,
        name="quercle_search",
        description=tool_metadata["search"]["description"],
        takes_ctx=False,
    )


def quercle_fetch_tool(
    api_key: str | None = None,
    timeout: float | None = None,
) -> Tool[Any]:
    """Create a Quercle URL fetch tool for Pydantic AI agents.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds.

    Returns:
        A Pydantic AI Tool configured for URL fetching.
    """
    client: AsyncQuercleClient | None = None

    async def quercle_fetch(url: str, prompt: str) -> str:
        nonlocal client
        if client is None:
            client = AsyncQuercleClient(api_key=api_key)
        return (await client.fetch(url=url, prompt=prompt, timeout=timeout)).result

    # Set docstring dynamically using imported descriptions
    quercle_fetch.__doc__ = f"""Fetch a URL and analyze its content with AI.

    Args:
        url: {tool_metadata["fetch"]["parameters"]["url"]}
        prompt: {tool_metadata["fetch"]["parameters"]["prompt"]}

    Returns:
        AI-processed analysis of the page content.
    """

    return Tool(
        quercle_fetch,
        name="quercle_fetch",
        description=tool_metadata["fetch"]["description"],
        takes_ctx=False,
    )


def quercle_raw_fetch_tool(
    api_key: str | None = None,
    timeout: float | None = None,
) -> Tool[Any]:
    """Create a Quercle raw URL fetch tool for Pydantic AI agents.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds.

    Returns:
        A Pydantic AI Tool configured for raw URL fetching.
    """
    client: AsyncQuercleClient | None = None

    async def quercle_raw_fetch(
        url: str,
        format: RawFetchBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        nonlocal client
        if client is None:
            client = AsyncQuercleClient(api_key=api_key)
        result = (await client.raw_fetch(
            url,
            format=format,
            use_safeguard=use_safeguard,
            timeout=timeout,
        )).result
        return result if isinstance(result, str) else json.dumps(result)

    # Set docstring dynamically using imported descriptions
    quercle_raw_fetch.__doc__ = f"""Fetch a URL and return raw markdown or HTML.

    Args:
        url: {tool_metadata["raw_fetch"]["parameters"]["url"]}
        format: {tool_metadata["raw_fetch"]["parameters"]["format"]}
        use_safeguard: {tool_metadata["raw_fetch"]["parameters"]["use_safeguard"]}

    Returns:
        Raw page content in the requested format.
    """

    return Tool(
        quercle_raw_fetch,
        name="quercle_raw_fetch",
        description=tool_metadata["raw_fetch"]["description"],
        takes_ctx=False,
    )


def quercle_raw_search_tool(
    api_key: str | None = None,
    timeout: float | None = None,
) -> Tool[Any]:
    """Create a Quercle raw web search tool for Pydantic AI agents.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds.

    Returns:
        A Pydantic AI Tool configured for raw web search.
    """
    client: AsyncQuercleClient | None = None

    async def quercle_raw_search(
        query: str,
        format: RawSearchBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        nonlocal client
        if client is None:
            client = AsyncQuercleClient(api_key=api_key)
        result = (await client.raw_search(
            query,
            format=format,
            use_safeguard=use_safeguard,
            timeout=timeout,
        )).result
        return result if isinstance(result, str) else json.dumps(result)

    # Set docstring dynamically using imported descriptions
    quercle_raw_search.__doc__ = f"""Run web search and return raw results.

    Args:
        query: {tool_metadata["raw_search"]["parameters"]["query"]}
        format: {tool_metadata["raw_search"]["parameters"]["format"]}
        use_safeguard: {tool_metadata["raw_search"]["parameters"]["use_safeguard"]}

    Returns:
        Raw search results in the requested format.
    """

    return Tool(
        quercle_raw_search,
        name="quercle_raw_search",
        description=tool_metadata["raw_search"]["description"],
        takes_ctx=False,
    )


def quercle_extract_tool(
    api_key: str | None = None,
    timeout: float | None = None,
) -> Tool[Any]:
    """Create a Quercle content extraction tool for Pydantic AI agents.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds.

    Returns:
        A Pydantic AI Tool configured for content extraction.
    """
    client: AsyncQuercleClient | None = None

    async def quercle_extract(
        url: str,
        query: str,
        format: ExtractBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        nonlocal client
        if client is None:
            client = AsyncQuercleClient(api_key=api_key)
        result = (await client.extract(
            url,
            query,
            format=format,
            use_safeguard=use_safeguard,
            timeout=timeout,
        )).result
        return result if isinstance(result, str) else json.dumps(result)

    # Set docstring dynamically using imported descriptions
    quercle_extract.__doc__ = f"""Fetch a URL and return chunks relevant to a query.

    Args:
        url: {tool_metadata["extract"]["parameters"]["url"]}
        query: {tool_metadata["extract"]["parameters"]["query"]}
        format: {tool_metadata["extract"]["parameters"]["format"]}
        use_safeguard: {tool_metadata["extract"]["parameters"]["use_safeguard"]}

    Returns:
        Extracted content chunks relevant to the query.
    """

    return Tool(
        quercle_extract,
        name="quercle_extract",
        description=tool_metadata["extract"]["description"],
        takes_ctx=False,
    )


def _build_tools_with_shared_client(
    api_key: str | None = None,
    timeout: float | None = None,
    allowed_domains: list[str] | None = None,
    blocked_domains: list[str] | None = None,
) -> dict[str, Tool[Any]]:
    """Build all 5 Quercle tools sharing a single lazy-initialized client."""
    client: AsyncQuercleClient | None = None

    def _get_client() -> AsyncQuercleClient:
        nonlocal client
        if client is None:
            client = AsyncQuercleClient(api_key=api_key)
        return client

    async def _search(query: str) -> str:
        return (await _get_client().search(
            query,
            allowed_domains=allowed_domains,
            blocked_domains=blocked_domains,
            timeout=timeout,
        )).result

    _search.__doc__ = f"""Search the web and get AI-synthesized answers with citations.

    Args:
        query: {tool_metadata["search"]["parameters"]["query"]}

    Returns:
        AI-synthesized answer with source citations.
    """

    async def _fetch(url: str, prompt: str) -> str:
        return (await _get_client().fetch(
            url=url, prompt=prompt, timeout=timeout
        )).result

    _fetch.__doc__ = f"""Fetch a URL and analyze its content with AI.

    Args:
        url: {tool_metadata["fetch"]["parameters"]["url"]}
        prompt: {tool_metadata["fetch"]["parameters"]["prompt"]}

    Returns:
        AI-processed analysis of the page content.
    """

    async def _raw_fetch(
        url: str,
        format: RawFetchBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        result = (await _get_client().raw_fetch(
            url, format=format, use_safeguard=use_safeguard, timeout=timeout,
        )).result
        return result if isinstance(result, str) else json.dumps(result)

    _raw_fetch.__doc__ = f"""Fetch a URL and return raw markdown or HTML.

    Args:
        url: {tool_metadata["raw_fetch"]["parameters"]["url"]}
        format: {tool_metadata["raw_fetch"]["parameters"]["format"]}
        use_safeguard: {tool_metadata["raw_fetch"]["parameters"]["use_safeguard"]}

    Returns:
        Raw page content in the requested format.
    """

    async def _raw_search(
        query: str,
        format: RawSearchBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        result = (await _get_client().raw_search(
            query, format=format, use_safeguard=use_safeguard, timeout=timeout,
        )).result
        return result if isinstance(result, str) else json.dumps(result)

    _raw_search.__doc__ = f"""Run web search and return raw results.

    Args:
        query: {tool_metadata["raw_search"]["parameters"]["query"]}
        format: {tool_metadata["raw_search"]["parameters"]["format"]}
        use_safeguard: {tool_metadata["raw_search"]["parameters"]["use_safeguard"]}

    Returns:
        Raw search results in the requested format.
    """

    async def _extract(
        url: str,
        query: str,
        format: ExtractBodyFormat | None = None,
        use_safeguard: bool | None = None,
    ) -> str:
        result = (await _get_client().extract(
            url, query, format=format, use_safeguard=use_safeguard, timeout=timeout,
        )).result
        return result if isinstance(result, str) else json.dumps(result)

    _extract.__doc__ = f"""Fetch a URL and return chunks relevant to a query.

    Args:
        url: {tool_metadata["extract"]["parameters"]["url"]}
        query: {tool_metadata["extract"]["parameters"]["query"]}
        format: {tool_metadata["extract"]["parameters"]["format"]}
        use_safeguard: {tool_metadata["extract"]["parameters"]["use_safeguard"]}

    Returns:
        Extracted content chunks relevant to the query.
    """

    return {
        "quercle_search": Tool(
            _search, name="quercle_search",
            description=tool_metadata["search"]["description"], takes_ctx=False,
        ),
        "quercle_fetch": Tool(
            _fetch, name="quercle_fetch",
            description=tool_metadata["fetch"]["description"], takes_ctx=False,
        ),
        "quercle_raw_fetch": Tool(
            _raw_fetch, name="quercle_raw_fetch",
            description=tool_metadata["raw_fetch"]["description"], takes_ctx=False,
        ),
        "quercle_raw_search": Tool(
            _raw_search, name="quercle_raw_search",
            description=tool_metadata["raw_search"]["description"], takes_ctx=False,
        ),
        "quercle_extract": Tool(
            _extract, name="quercle_extract",
            description=tool_metadata["extract"]["description"], takes_ctx=False,
        ),
    }


def quercle_tools(
    api_key: str | None = None,
    timeout: float | None = None,
) -> list[Tool[Any]]:
    """Create all Quercle tools for Pydantic AI agents.

    All tools share a single lazily-initialized client instance.

    Args:
        api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
        timeout: Request timeout in seconds.

    Returns:
        A list containing all Quercle tools.
    """
    return list(_build_tools_with_shared_client(
        api_key=api_key, timeout=timeout,
    ).values())


class QuercleToolset(FunctionToolset):
    """A Pydantic AI toolset providing Quercle web search and URL fetch capabilities.

    All included tools share a single lazily-initialized client instance.

    This toolset can be composed with other toolsets using Pydantic AI's
    CombinedToolset or passed directly to agents.

    Example:
        >>> from pydantic_ai import Agent
        >>> from pydantic_ai_quercle import QuercleToolset
        >>> toolset = QuercleToolset()
        >>> agent = Agent('openai:gpt-4o', toolsets=[toolset])
    """

    def __init__(
        self,
        api_key: str | None = None,
        timeout: float | None = None,
        *,
        include_search: bool = True,
        include_fetch: bool = True,
        include_raw_fetch: bool = True,
        include_raw_search: bool = True,
        include_extract: bool = True,
        search_allowed_domains: list[str] | None = None,
        search_blocked_domains: list[str] | None = None,
    ):
        """Initialize the Quercle toolset.

        Args:
            api_key: Quercle API key. Falls back to QUERCLE_API_KEY env var if not provided.
            timeout: Request timeout in seconds.
            include_search: Include the web search tool (default: True).
            include_fetch: Include the URL fetch tool (default: True).
            include_raw_fetch: Include the raw URL fetch tool (default: True).
            include_raw_search: Include the raw web search tool (default: True).
            include_extract: Include the content extraction tool (default: True).
            search_allowed_domains: Only include search results from these domains.
            search_blocked_domains: Exclude search results from these domains.
        """
        all_tools = _build_tools_with_shared_client(
            api_key=api_key,
            timeout=timeout,
            allowed_domains=search_allowed_domains,
            blocked_domains=search_blocked_domains,
        )

        include_map = {
            "quercle_search": include_search,
            "quercle_fetch": include_fetch,
            "quercle_raw_fetch": include_raw_fetch,
            "quercle_raw_search": include_raw_search,
            "quercle_extract": include_extract,
        }

        tools = [t for name, t in all_tools.items() if include_map[name]]

        super().__init__(tools=tools)
