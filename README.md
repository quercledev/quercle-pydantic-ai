# quercle-pydantic-ai

Quercle web search and fetch tools for [Pydantic AI](https://ai.pydantic.dev/).

## Installation

```bash
uv add quercle-pydantic-ai
# or
pip install quercle-pydantic-ai
```

## Setup

Set your API key as an environment variable:

```bash
export QUERCLE_API_KEY=qk_...
```

Get your API key at [quercle.dev](https://quercle.dev).

## Quick Start

```python
from pydantic_ai import Agent
from quercle_pydantic_ai import quercle_tools

agent = Agent(
    "openai:gpt-4o",
    tools=quercle_tools(),
    system_prompt="You are a helpful research assistant.",
)

result = agent.run_sync("Search for the latest news about AI agents")
print(result.output)
```

`quercle_tools()` returns all 5 tools: search, fetch, raw search, raw fetch, and extract.

## Direct Tool Usage

The tools are async (Pydantic AI tools are async by design). For direct usage, use the underlying SDK client:

```python
import asyncio
from quercle import AsyncQuercleClient

async def main():
    client = AsyncQuercleClient()

    # Search
    result = await client.search("best practices for building AI agents")
    print(result.result)

    # Search with domain filtering
    result = await client.search(
        "Python documentation",
        allowed_domains=["docs.python.org"],
    )
    print(result.result)

    # Fetch and analyze a page
    result = await client.fetch(
        "https://en.wikipedia.org/wiki/TypeScript",
        "Summarize the key features of TypeScript",
    )
    print(result.result)

asyncio.run(main())
```

### Custom API Key

```python
tools = quercle_tools(api_key="qk_...")
```

## Agentic Usage

### Research Agent

```python
from pydantic_ai import Agent
from quercle_pydantic_ai import quercle_tools

agent = Agent(
    "anthropic:claude-sonnet-4-20250514",
    tools=quercle_tools(),
    system_prompt="You are a research assistant. Search the web to find "
    "accurate, up-to-date information. Always cite your sources.",
)

result = agent.run_sync("What are the latest developments in WebAssembly?")
print(result.output)
```

### Async Agent

```python
import asyncio
from pydantic_ai import Agent
from quercle_pydantic_ai import quercle_tools

agent = Agent("openai:gpt-4o", tools=quercle_tools())

async def main():
    result = await agent.run("Search for trending AI papers this week")
    print(result.output)

asyncio.run(main())
```

### Streaming

```python
import asyncio
from pydantic_ai import Agent
from quercle_pydantic_ai import quercle_tools

agent = Agent("openai:gpt-4o", tools=quercle_tools())

async def main():
    async with agent.run_stream("Summarize the latest AI news") as response:
        async for text in response.stream_text():
            print(text, end="", flush=True)

asyncio.run(main())
```

### Individual Tools

```python
from quercle_pydantic_ai import (
    quercle_search_tool,
    quercle_fetch_tool,
    quercle_raw_search_tool,
    quercle_raw_fetch_tool,
    quercle_extract_tool,
)

# Use only search
agent = Agent("openai:gpt-4o", tools=[quercle_search_tool()])

# Use only fetch
agent = Agent("openai:gpt-4o", tools=[quercle_fetch_tool()])

# Combine specific tools
agent = Agent("openai:gpt-4o", tools=[
    quercle_search_tool(),
    quercle_raw_fetch_tool(),
    quercle_extract_tool(),
])
```

### With QuercleToolset

```python
from pydantic_ai import Agent
from quercle_pydantic_ai import QuercleToolset

# All 5 tools with domain filtering
toolset = QuercleToolset(
    search_allowed_domains=["docs.python.org", "realpython.com"],
)

# Selectively include tools
toolset = QuercleToolset(
    include_raw_fetch=False,
    include_raw_search=False,
    include_extract=False,
)

agent = Agent("openai:gpt-4o", toolsets=[toolset])
```

## Configuration

| Parameter | Default | Description |
|---|---|---|
| `api_key` | `QUERCLE_API_KEY` env var | Your Quercle API key |
| `timeout` | `None` | Request timeout in seconds |
| `allowed_domains` | `None` | Restrict search to these domains |
| `blocked_domains` | `None` | Exclude these domains from search |

## API Reference

| Export | Description |
|---|---|
| `quercle_search_tool(...)` | AI-synthesized web search with citations |
| `quercle_fetch_tool(...)` | Fetch a URL and analyze its content with AI |
| `quercle_raw_search_tool(...)` | Raw web search results (markdown or JSON) |
| `quercle_raw_fetch_tool(...)` | Raw URL content (markdown or HTML) |
| `quercle_extract_tool(...)` | Extract content chunks relevant to a query from a URL |
| `quercle_tools(...)` | Returns all 5 tools as a list |
| `QuercleToolset(...)` | Composable `FunctionToolset` for use with `toolsets=` |

## License

MIT
