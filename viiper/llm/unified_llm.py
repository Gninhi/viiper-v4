"""
Unified LLM Interface for VIIPER.

Provides a unified interface to multiple LLM providers (NVIDIA, Kimi, etc.)
with skill-based agent routing.
"""

from typing import Dict, Any, List, Optional, Generator
from dataclasses import dataclass
from enum import Enum
import os
import sys
import requests
import json


class LLMProvider(str, Enum):
    """Available LLM providers."""
    NVIDIA = "nvidia"
    KIMI = "kimi"


class ModelType(str, Enum):
    """Available models with their capabilities."""
    # NVIDIA Models
    GLM5 = "z-ai/glm5"
    LLAMA_405B = "meta/llama-3.1-405b-instruct"
    LLAMA_70B = "meta/llama-3.1-70b-instruct"
    MIXTRAL = "mistralai/mixtral-8x7b-instruct"
    
    # Kimi Models
    KIMI_K25 = "moonshotai/kimi-k2.5"


@dataclass
class LLMResponse:
    """Response from LLM."""
    content: str
    reasoning: str = ""
    model: str = ""
    provider: str = ""
    tokens_used: int = 0
    success: bool = True
    error: str = ""


@dataclass
class ModelCapabilities:
    """Capabilities of a model."""
    model: str
    provider: str
    api_key: str
    base_url: str
    max_tokens: int
    supports_streaming: bool = True
    supports_thinking: bool = False
    supports_reasoning: bool = False
    best_for: List[str] = None
    
    def __post_init__(self):
        if self.best_for is None:
            self.best_for = []


# Model configurations
MODEL_CONFIGS = {
    # NVIDIA GLM5 - Best for reasoning and complex tasks
    ModelType.GLM5: ModelCapabilities(
        model="z-ai/glm5",
        provider="nvidia",
        api_key="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",
        base_url="https://integrate.api.nvidia.com/v1",
        max_tokens=16384,
        supports_thinking=True,
        supports_reasoning=True,
        best_for=["code_generation", "architecture", "analysis", "reasoning"],
    ),
    
    # NVIDIA Llama 405B - Best for complex reasoning
    ModelType.LLAMA_405B: ModelCapabilities(
        model="meta/llama-3.1-405b-instruct",
        provider="nvidia",
        api_key="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",
        base_url="https://integrate.api.nvidia.com/v1",
        max_tokens=16384,
        best_for=["complex_reasoning", "architecture", "planning"],
    ),
    
    # Kimi K2.5 - Best for long context and thinking
    ModelType.KIMI_K25: ModelCapabilities(
        model="moonshotai/kimi-k2.5",
        provider="kimi",
        api_key="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",
        base_url="https://integrate.api.nvidia.com/v1",
        max_tokens=16384,
        supports_thinking=True,
        best_for=["market_research", "idea_generation", "long_context", "browsing"],
    ),
}


class UnifiedLLM:
    """
    Unified LLM interface supporting multiple providers and models.
    
    Features:
    - Multiple model support (GLM5, Kimi K2.5, Llama, Mixtral)
    - Skill-based model routing
    - Streaming and non-streaming responses
    - Thinking/reasoning support
    """
    
    def __init__(
        self,
        model: str = None,
        skill: str = None,
        temperature: float = 1.0,
        top_p: float = 1.0,
        max_tokens: int = None,
        stream: bool = False,
    ):
        """
        Initialize unified LLM.
        
        Args:
            model: Model to use (defaults to auto-select based on skill)
            skill: Skill/task type for model routing
            temperature: Sampling temperature
            top_p: Top-p sampling
            max_tokens: Maximum tokens
            stream: Enable streaming
        """
        self.model = model
        self.skill = skill
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.stream = stream
        self._client = None
    
    def select_model_for_skill(self, skill: str) -> str:
        """
        Select best model for a skill/task.
        
        Args:
            skill: Skill type (code_generation, market_research, etc.)
        
        Returns:
            Best model name for the skill
        """
        for model_type, config in MODEL_CONFIGS.items():
            if skill in config.best_for:
                return config.model
        
        # Default to GLM5
        return ModelType.GLM5.value
    
    def get_config(self, model: str = None) -> ModelCapabilities:
        """Get configuration for a model."""
        model_name = model or self.model
        
        if model_name:
            for mt, config in MODEL_CONFIGS.items():
                if config.model == model_name or mt.value == model_name:
                    return config
        
        # Auto-select based on skill
        if self.skill:
            selected = self.select_model_for_skill(self.skill)
            return MODEL_CONFIGS.get(ModelType(selected), list(MODEL_CONFIGS.values())[0])
        
        # Default to GLM5
        return MODEL_CONFIGS[ModelType.GLM5]
    
    def complete(
        self,
        prompt: str,
        system_prompt: str = None,
        model: str = None,
        temperature: float = None,
        max_tokens: int = None,
        stream: bool = None,
    ) -> LLMResponse:
        """
        Generate completion.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            model: Override model
            temperature: Override temperature
            max_tokens: Override max tokens
            stream: Override stream setting
        
        Returns:
            LLMResponse with content and reasoning
        """
        config = self.get_config(model)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        payload = {
            "model": config.model,
            "messages": messages,
            "max_tokens": max_tokens or self.max_tokens or config.max_tokens,
            "temperature": temperature or self.temperature,
            "top_p": self.top_p,
            "stream": stream if stream is not None else self.stream,
        }
        
        # Add thinking support for compatible models
        if config.supports_thinking:
            if config.provider == "kimi":
                payload["chat_template_kwargs"] = {"thinking": True}
            else:
                payload["extra_body"] = {
                    "chat_template_kwargs": {
                        "enable_thinking": True,
                        "clear_thinking": False,
                    }
                }
        
        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Accept": "text/event-stream" if payload["stream"] else "application/json",
            "Content-Type": "application/json",
        }
        
        try:
            response = requests.post(
                f"{config.base_url}/chat/completions",
                headers=headers,
                json=payload,
                stream=payload["stream"],
                timeout=120,
            )
            
            if payload["stream"]:
                return self._handle_stream_response(response, config)
            else:
                return self._handle_json_response(response, config)
                
        except Exception as e:
            return LLMResponse(
                content="",
                reasoning="",
                model=config.model,
                provider=config.provider,
                success=False,
                error=str(e),
            )
    
    def _handle_json_response(self, response, config: ModelCapabilities) -> LLMResponse:
        """Handle non-streaming JSON response."""
        try:
            data = response.json()
            
            if "error" in data:
                return LLMResponse(
                    content="",
                    model=config.model,
                    provider=config.provider,
                    success=False,
                    error=str(data["error"]),
                )
            
            choices = data.get("choices", [])
            if not choices:
                return LLMResponse(
                    content="",
                    model=config.model,
                    provider=config.provider,
                    success=False,
                    error="No choices in response",
                )
            
            message = choices[0].get("message", {})
            content = message.get("content", "")
            reasoning = message.get("reasoning_content", "")
            
            return LLMResponse(
                content=content,
                reasoning=reasoning,
                model=config.model,
                provider=config.provider,
                tokens_used=data.get("usage", {}).get("total_tokens", 0),
                success=True,
            )
            
        except Exception as e:
            return LLMResponse(
                content="",
                model=config.model,
                provider=config.provider,
                success=False,
                error=str(e),
            )
    
    def _handle_stream_response(self, response, config: ModelCapabilities) -> LLMResponse:
        """Handle streaming SSE response."""
        content = ""
        reasoning = ""
        
        _USE_COLOR = sys.stdout.isatty() and os.getenv("NO_COLOR") is None
        _REASONING_COLOR = "\033[90m" if _USE_COLOR else ""
        _RESET_COLOR = "\033[0m" if _USE_COLOR else ""
        
        for line in response.iter_lines():
            if not line:
                continue
            
            line_text = line.decode("utf-8")
            
            if line_text.startswith("data: "):
                data_str = line_text[6:]
                
                if data_str == "[DONE]":
                    break
                
                try:
                    data = json.loads(data_str)
                    choices = data.get("choices", [])
                    
                    if choices:
                        delta = choices[0].get("delta", {})
                        
                        # Handle reasoning content
                        chunk_reasoning = delta.get("reasoning_content", "")
                        if chunk_reasoning:
                            reasoning += chunk_reasoning
                            print(f"{_REASONING_COLOR}{chunk_reasoning}{_RESET_COLOR}", end="")
                        
                        # Handle regular content
                        chunk_content = delta.get("content", "")
                        if chunk_content:
                            content += chunk_content
                            print(chunk_content, end="")
                            
                except json.JSONDecodeError:
                    continue
        
        print()  # New line after streaming
        
        return LLMResponse(
            content=content,
            reasoning=reasoning,
            model=config.model,
            provider=config.provider,
            success=True,
        )
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = None,
        **kwargs,
    ) -> LLMResponse:
        """
        Multi-turn chat completion.
        
        Args:
            messages: List of message dicts
            model: Override model
            **kwargs: Additional arguments for complete()
        
        Returns:
            LLMResponse
        """
        config = self.get_config(model)
        
        payload = {
            "model": config.model,
            "messages": messages,
            "max_tokens": kwargs.get("max_tokens", self.max_tokens or config.max_tokens),
            "temperature": kwargs.get("temperature", self.temperature),
            "top_p": self.top_p,
            "stream": kwargs.get("stream", self.stream),
        }
        
        if config.supports_thinking:
            if config.provider == "kimi":
                payload["chat_template_kwargs"] = {"thinking": True}
            else:
                payload["extra_body"] = {
                    "chat_template_kwargs": {
                        "enable_thinking": True,
                        "clear_thinking": False,
                    }
                }
        
        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Accept": "text/event-stream" if payload["stream"] else "application/json",
            "Content-Type": "application/json",
        }
        
        try:
            response = requests.post(
                f"{config.base_url}/chat/completions",
                headers=headers,
                json=payload,
                stream=payload["stream"],
                timeout=120,
            )
            
            if payload["stream"]:
                return self._handle_stream_response(response, config)
            else:
                return self._handle_json_response(response, config)
                
        except Exception as e:
            return LLMResponse(
                content="",
                model=config.model,
                provider=config.provider,
                success=False,
                error=str(e),
            )
    
    # Skill-specific methods
    
    def generate_code(self, description: str, language: str = "python") -> LLMResponse:
        """Generate code (uses GLM5 by default)."""
        return self.complete(
            prompt=f"Generate {language} code for:\n\n{description}\n\nProvide clean, documented code.",
            system_prompt="You are an expert developer. Write clean, efficient code.",
            skill="code_generation",
        )
    
    def analyze_market(self, data: str) -> LLMResponse:
        """Analyze market trends (uses Kimi K2.5 by default)."""
        return self.complete(
            prompt=f"Analyze these market trends and identify opportunities:\n\n{data}",
            system_prompt="You are a market analyst. Identify patterns and opportunities.",
            model=ModelType.KIMI_K25.value,
        )
    
    def generate_ideas(self, context: str) -> LLMResponse:
        """Generate app ideas (uses Kimi K2.5 by default)."""
        return self.complete(
            prompt=f"Generate innovative SaaS app ideas based on:\n\n{context}",
            system_prompt="You are a startup advisor. Generate creative, viable ideas.",
            model=ModelType.KIMI_K25.value,
        )
    
    def design_architecture(self, requirements: str, constraints: List[str] = None) -> LLMResponse:
        """Design system architecture (uses GLM5 or Llama)."""
        prompt = f"Design a system architecture for:\n\n{requirements}"
        if constraints:
            prompt += f"\n\nConstraints:\n" + "\n".join(f"- {c}" for c in constraints)
        prompt += "\n\nProvide detailed architecture with components and data flow."
        
        return self.complete(
            prompt=prompt,
            system_prompt="You are a senior architect. Design scalable systems.",
            skill="architecture",
        )
    
    def review_code(self, code: str) -> LLMResponse:
        """Review code for issues."""
        return self.complete(
            prompt=f"Review this code for bugs, security issues, and improvements:\n\n```\n{code}\n```",
            system_prompt="You are a code reviewer. Identify issues and suggest improvements.",
            skill="analysis",
        )


# Convenience functions
_default_llm = None


def get_llm(model: str = None, skill: str = None, **kwargs) -> UnifiedLLM:
    """Get LLM instance."""
    global _default_llm
    
    if _default_llm is None or model or skill:
        _default_llm = UnifiedLLM(model=model, skill=skill, **kwargs)
    
    return _default_llm


def complete(prompt: str, model: str = None, **kwargs) -> str:
    """Quick completion helper."""
    llm = get_llm(model=model)
    response = llm.complete(prompt, **kwargs)
    return response.content


def chat(messages: List[Dict], model: str = None, **kwargs) -> str:
    """Quick chat helper."""
    llm = get_llm(model=model)
    response = llm.chat(messages, **kwargs)
    return response.content