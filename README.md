# Grep SDK

> Getting started

Grep SDK is the easiest way to get started with Grep services. It enables instant adoption of Grep through a seamless manner within a minute.

## 🚀 Quick Start

### Installation

```bash
pip install grep-sdk
```

### Basic Usage

```python
from grep import Grep

# Initialize once at app startup
Grep.init(api_key="grep_myorg_abc123...")

# That's it! Your LLM calls are now automatically traced
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## 🔑 Configuration

### Getting Your API Key

1. Go to http://grep2.com/ (create your account)
   - Production: https://app.grep2.com/settings/api-keys
2. Create a new API key
3. Copy the key (starts with `grep_`)

### Option 1: Pass API Key Directly

```python
Grep.init(api_key="grep_myorg_abc123...")
```

### Option 2: Use Environment Variable

```bash
export GREP_API_KEY="grep_myorg_abc123..."
```

```python
Grep.init()  # Automatically uses GREP_API_KEY
```

### Custom Collector Endpoint

For self-hosted or org-specific collectors:

```python
Grep.init(
    api_key="grep_myorg_abc123...",
    collector_endpoint="https://myorg.grep.com"
)
```

### Development Mode

Get traces immediately (no batching):

```python
Grep.init(
    api_key="grep_myorg_abc123...",
    disable_batch=True  # Useful for debugging
)
```

## 📊 What Gets Traced?

Grep automatically instruments:

- **LLM Providers**: OpenAI, Anthropic, Cohere, Bedrock, Azure OpenAI
- **Vector DBs**: Pinecone, Qdrant, Weaviate, Chroma, Milvus
- **Frameworks**: LangChain, LlamaIndex, Haystack
- **Libraries**: Requests, HTTPX, AsyncIO

### Trace Details Include:

- Prompts and completions
- Model parameters (temperature, max_tokens, etc.)
- Latency and token usage
- Errors and exceptions
- Vector similarity scores
- Chain/agent execution flow

## 🎯 Advanced Usage

### Add Custom Properties

```python
Grep.set_association_properties({
    "user_id": "user_123",
    "session_id": "session_456",
    "environment": "production"
})
```

### Graceful Shutdown

```python
import atexit

# Flush traces before exit
atexit.register(Grep.shutdown)
```

### Check Initialization Status

```python
if Grep.is_initialized():
    print("Grep is running!")
```

## 🐛 Troubleshooting

### "Grep API key is required"

Make sure you've set your API key:
```python
Grep.init(api_key="grep_xxxxx")
```

Or via environment:
```bash
export GREP_API_KEY="grep_xxxxx"
```

### "Invalid Grep API key format"

API keys must start with `grep_`. Check that you copied the full key.

### Connection Errors

Verify your collector endpoint is reachable:
```python
Grep.init(
    api_key="grep_xxxxx",
    collector_endpoint="http://localhost:8000"  # Default for local testing
)
```

### No Traces Appearing

1. Check if batching is enabled (default)
   - Use `disable_batch=True` for immediate traces
2. Verify your API key is active in the dashboard
3. Check collector endpoint is correct

## 📚 Documentation

- [Full Documentation](https://docs.grep2.com) *(coming soon)*
- [API Reference](https://docs.grep2.com/api) *(coming soon)*
- [Example Projects](https://github.com/yourusername/grep-examples) *(coming soon)*

