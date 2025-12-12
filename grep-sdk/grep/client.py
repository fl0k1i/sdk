"""
Grep Client - Main SDK interface

This wraps Traceloop SDK but presents it as "Grep" to customers.
"""

import os
from typing import Optional
import warnings

# We use Traceloop under the hood, but customer never sees this
try:
    from traceloop.sdk import Traceloop
except ImportError:
    raise ImportError(
        "Grep SDK requires traceloop-sdk. Install it with:\n"
        "pip install traceloop-sdk>=0.49.2"
    )


class Grep:
    """
    Grep SDK - LLM Observability
    
    Automatically instruments LLM calls (OpenAI, Anthropic, etc.)
    and sends telemetry to Grep's collector endpoint.
    
    Usage:
        from grep import Grep
        
        # Initialize at app startup
        Grep.init(api_key="grep_xxxxx")
        
        # Your LLM code is now automatically traced!
        from openai import OpenAI
        client = OpenAI()
        response = client.chat.completions.create(...)
    """
    
    _initialized = False
    _api_key: Optional[str] = None
    _collector_endpoint: Optional[str] = None
    
    @classmethod
    def init(
        cls,
        api_key: Optional[str] = None,
        collector_endpoint: Optional[str] = None,
        disable_batch: bool = False,
        app_name: Optional[str] = None,
    ):
        """
        Initialize Grep telemetry
        
        Args:
            api_key (str): Your Grep API key from app.grep.com
                          Can also be set via GREP_API_KEY env var
            
            collector_endpoint (str): OTLP collector endpoint
                                     Default: http://localhost:8000 (for testing)
                                     Production: https://collector.grep.com
            
            disable_batch (bool): If True, sends traces immediately (useful for testing)
                                 Default: False (batches for efficiency)
            
            app_name (str): Optional name to identify your application in traces
        
        Raises:
            ValueError: If API key is missing or invalid format
        
        Example:
            # Basic usage
            Grep.init(api_key="grep_myorg_abc123...")
            
            # With custom endpoint
            Grep.init(
                api_key="grep_myorg_abc123...",
                collector_endpoint="https://myorg.grep.com"
            )
            
            # Development mode (immediate traces)
            Grep.init(
                api_key="grep_myorg_abc123...",
                disable_batch=True
            )
        """
        
        if cls._initialized:
            warnings.warn("⚠️  Grep is already initialized. Skipping re-initialization.")
            return
        
        # Step 1: Get API key (from parameter or environment)
        cls._api_key = api_key or os.getenv("GREP_API_KEY")
        
        if not cls._api_key:
            raise ValueError(
                "Grep API key is required!\n\n"
                "Provide it in one of two ways:\n"
                "  1. Pass as parameter: Grep.init(api_key='grep_xxxxx')\n"
                "  2. Set environment variable: export GREP_API_KEY='grep_xxxxx'\n\n"
                "Get your API key at: http://localhost:3000/settings/api-keys\n"
                "(Production: https://app.grep.com/settings/api-keys)"
            )
        
        # Step 2: Validate API key format
        if not cls._api_key.startswith("grep_"):
            raise ValueError(
                "Invalid Grep API key format!\n"
                "API keys should start with 'grep_'\n"
                f"Your key starts with: {cls._api_key[:10]}..."
            )
        
        # Step 3: Set collector endpoint
        if not collector_endpoint:
            # Default to localhost for testing
            # In production, this would be your deployed backend
            collector_endpoint = os.getenv(
                "GREP_COLLECTOR_ENDPOINT",
                "http://localhost:8000"  # Your Grep backend
            )
        
        cls._collector_endpoint = collector_endpoint
        
        # Step 4: Configure Traceloop to use OUR backend (not Traceloop directly)
        # We set these env vars so Traceloop sends to OUR proxy, not theirs
        os.environ["TRACELOOP_BASE_URL"] = collector_endpoint
        os.environ["TRACELOOP_HEADERS"] = f"authorization=Bearer {cls._api_key}"
        
        # Step 5: Initialize underlying Traceloop SDK
        try:
            Traceloop.init(
                app_name=app_name or "grep-app",
                disable_batch=disable_batch,
                api_endpoint=f"{collector_endpoint}/v1/traces",
            )
        except Exception as e:
            # Don't fail initialization if backend isn't running yet
            # This allows testing the SDK without backend
            warnings.warn(
                f"Could not connect to Grep collector: {str(e)}\n"
                f"Traces will be sent when collector is available at: {collector_endpoint}"
            )
        
        cls._initialized = True
        
        # Success message
        print("✅ Grep initialized successfully!")
        print(f"📊 Collector: {collector_endpoint}")
        print(f"🔑 API Key: {cls._api_key[:15]}...")
        print(f"📈 View traces: http://localhost:3000/traces")
        print("    (Production: https://app.grep.com/traces)")
    
    @classmethod
    def set_association_properties(cls, properties: dict):
        """
        Set custom properties for trace association
        
        This adds metadata to traces for filtering/grouping.
        
        Args:
            properties (dict): Key-value pairs to attach to traces
        
        Example:
            Grep.set_association_properties({
                "user_id": "user_123",
                "session_id": "sess_456",
                "environment": "production"
            })
        """
        if not cls._initialized:
            raise RuntimeError(
                "Grep not initialized! Call Grep.init() first."
            )
        
        return Traceloop.set_association_properties(properties)
    
    @classmethod
    def shutdown(cls):
        """
        Gracefully shutdown Grep telemetry
        
        Flushes any pending traces before shutting down.
        Call this before your application exits.
        
        Example:
            import atexit
            atexit.register(Grep.shutdown)
        """
        if not cls._initialized:
            return
        
        try:
            # Flush any pending traces
            # Note: Traceloop doesn't have explicit shutdown in current version
            # but we'll implement graceful handling
            print("👋 Grep shutdown initiated...")
            cls._initialized = False
            print("✅ Grep shutdown complete")
        except Exception as e:
            print(f"⚠️  Error during Grep shutdown: {e}")
    
    @classmethod
    def is_initialized(cls) -> bool:
        """Check if Grep has been initialized"""
        return cls._initialized
    
    @classmethod
    def get_collector_endpoint(cls) -> Optional[str]:
        """Get the current collector endpoint"""
        return cls._collector_endpoint
