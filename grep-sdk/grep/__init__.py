"""
Grep SDK - LLM Observability Platform

Customer-facing SDK that wraps Traceloop/OpenLLMetry.
Customers never see Traceloop - only Grep branding.
"""

from .client import Grep

__version__ = "0.1.0"
__all__ = ["Grep"]
