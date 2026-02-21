"""
NVIDIA NIM LLM Integration for VIIPER.

Provides access to NVIDIA's AI models (z-ai/glm5, etc.) for agents.
"""

from typing import Dict, Any, List, Optional, Generator
from dataclasses import dataclass
import os
import sys


@dataclass
class LLMResponse:
    """Response from LLM."""
    content: str
    reasoning: str = ""
    model: str = ""
    tokens_used: int = 0
    success: bool = True
    error: str = ""


class NvidiaLLM:
    """
    NVIDIA NIM LLM client for VIIPER agents.
    
    Supports models:
    - z-ai/glm5 (default)
    - meta/llama-3.1-405b-instruct
    - meta/llama-3.1-70b-instruct
    - mistralai/mixtral-8x7b-instruct
    - and more...
    """
    
    DEFAULT_MODEL = "z-ai/glm5"
    BASE_URL = "https://integrate.api.nvidia.com/v1"
    
    def __init__(
        self,
        api_key: str = None,
        model: str = None,
        temperature: float = 1.0,
        top_p: float = 1.0,
        max_tokens: int = 16384,
        enable_thinking: bool = True,
    ):
        """
        Initialize NVIDIA LLM client.
        
        Args:
            api_key: NVIDIA API key (defaults to env NVIDIA_API_KEY)
            model: Model to use (defaults to z-ai/glm5)
            temperature: Sampling temperature
            top_p: Top-p sampling
            max_tokens: Maximum tokens to generate
            enable_thinking: Enable reasoning/thinking mode
        """
        self.api_key = api_key or os.getenv("NVIDIA_API_KEY", "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")
        self.model = model or self.DEFAULT_MODEL
        self.temperature = temperature
        self.top_p = top_p
        self.max_tokens = max_tokens
        self.enable_thinking = enable_thinking
        self._client = None
    
    @property
    def client(self):
        """Lazy load OpenAI client."""
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(
                base_url=self.BASE_URL,
                api_key=self.api_key,
            )
        return self._client
    
    def complete(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = None,
        max_tokens: int = None,
        stream: bool = False,
    ) -> LLMResponse:
        """
        Generate completion for a prompt.
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Override default temperature
            max_tokens: Override default max tokens
            stream: Whether to stream response
        
        Returns:
            LLMResponse with content and reasoning
        """
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": prompt})
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                top_p=self.top_p,
                max_tokens=max_tokens or self.max_tokens,
                extra_body={
                    "chat_template_kwargs": {
                        "enable_thinking": self.enable_thinking,
                        "clear_thinking": False,
                    }
                },
                stream=stream,
            )
            
            if stream:
                return self._handle_stream(completion)
            else:
                return self._handle_response(completion)
                
        except Exception as e:
            return LLMResponse(
                content="",
                reasoning="",
                model=self.model,
                success=False,
                error=str(e),
            )
    
    def _handle_response(self, completion) -> LLMResponse:
        """Handle non-streaming response."""
        if not completion.choices:
            return LLMResponse(
                content="",
                reasoning="",
                model=self.model,
                success=False,
                error="No choices in response",
            )
        
        choice = completion.choices[0]
        content = choice.message.content or ""
        reasoning = getattr(choice.message, "reasoning_content", "") or ""
        
        return LLMResponse(
            content=content,
            reasoning=reasoning,
            model=self.model,
            tokens_used=completion.usage.total_tokens if completion.usage else 0,
            success=True,
        )
    
    def _handle_stream(self, completion) -> Generator:
        """Handle streaming response."""
        content = ""
        reasoning = ""
        
        _USE_COLOR = sys.stdout.isatty() and os.getenv("NO_COLOR") is None
        _REASONING_COLOR = "\033[90m" if _USE_COLOR else ""
        _RESET_COLOR = "\033[0m" if _USE_COLOR else ""
        
        for chunk in completion:
            if not getattr(chunk, "choices", None):
                continue
            if len(chunk.choices) == 0 or getattr(chunk.choices[0], "delta", None) is None:
                continue
            
            delta = chunk.choices[0].delta
            
            chunk_reasoning = getattr(delta, "reasoning_content", None)
            if chunk_reasoning:
                reasoning += chunk_reasoning
                print(f"{_REASONING_COLOR}{chunk_reasoning}{_RESET_COLOR}", end="")
            
            chunk_content = getattr(delta, "content", None)
            if chunk_content:
                content += chunk_content
                print(chunk_content, end="")
        
        return LLMResponse(
            content=content,
            reasoning=reasoning,
            model=self.model,
            success=True,
        )
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None,
        stream: bool = False,
    ) -> LLMResponse:
        """
        Multi-turn chat completion.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Override default temperature
            max_tokens: Override default max tokens
            stream: Whether to stream response
        
        Returns:
            LLMResponse with content and reasoning
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                top_p=self.top_p,
                max_tokens=max_tokens or self.max_tokens,
                extra_body={
                    "chat_template_kwargs": {
                        "enable_thinking": self.enable_thinking,
                        "clear_thinking": False,
                    }
                },
                stream=stream,
            )
            
            if stream:
                return self._handle_stream(completion)
            else:
                return self._handle_response(completion)
                
        except Exception as e:
            return LLMResponse(
                content="",
                reasoning="",
                model=self.model,
                success=False,
                error=str(e),
            )
    
    def analyze_code(self, code: str, task: str = "review") -> LLMResponse:
        """
        Analyze code using LLM.
        
        Args:
            code: Code to analyze
            task: Type of analysis (review, explain, optimize, debug)
        
        Returns:
            LLMResponse with analysis
        """
        prompts = {
            "review": "Review this code for bugs, security issues, and improvements:\n\n```{language}\n{code}\n```\n\nProvide a detailed review.",
            "explain": "Explain what this code does:\n\n```\n{code}\n```\n\nProvide a clear explanation.",
            "optimize": "Optimize this code for performance:\n\n```\n{code}\n```\n\nSuggest optimizations.",
            "debug": "Find and fix bugs in this code:\n\n```\n{code}\n```\n\nIdentify issues and provide fixes.",
        }
        
        prompt = prompts.get(task, prompts["review"]).format(code=code, language="python")
        
        return self.complete(
            prompt=prompt,
            system_prompt="You are an expert software engineer. Provide clear, actionable feedback.",
        )
    
    def generate_code(
        self,
        description: str,
        language: str = "python",
        context: str = None,
    ) -> LLMResponse:
        """
        Generate code from description.
        
        Args:
            description: What the code should do
            language: Programming language
            context: Additional context
        
        Returns:
            LLMResponse with generated code
        """
        prompt = f"Generate {language} code for the following:\n\n{description}"
        
        if context:
            prompt += f"\n\nContext:\n{context}"
        
        prompt += "\n\nProvide clean, well-documented code."
        
        return self.complete(
            prompt=prompt,
            system_prompt=f"You are an expert {language} developer. Write clean, efficient, well-documented code.",
        )
    
    def analyze_market_trends(self, data: str) -> LLMResponse:
        """
        Analyze market trends for idea generation.
        
        Args:
            data: Market data or trend information
        
        Returns:
            LLMResponse with analysis
        """
        return self.complete(
            prompt=f"Analyze these market trends and identify opportunities:\n\n{data}",
            system_prompt="You are a market analyst and startup advisor. Identify patterns, opportunities, and actionable insights.",
        )
    
    def design_architecture(
        self,
        requirements: str,
        constraints: List[str] = None,
    ) -> LLMResponse:
        """
        Design system architecture.
        
        Args:
            requirements: System requirements
            constraints: List of constraints
        
        Returns:
            LLMResponse with architecture design
        """
        prompt = f"Design a system architecture for:\n\n{requirements}"
        
        if constraints:
            prompt += f"\n\nConstraints:\n" + "\n".join(f"- {c}" for c in constraints)
        
        prompt += "\n\nProvide a detailed architecture with components, data flow, and technology recommendations."
        
        return self.complete(
            prompt=prompt,
            system_prompt="You are a senior software architect. Design scalable, maintainable systems.",
        )


# Singleton instance for easy access
_default_llm = None


def get_llm(model: str = None, **kwargs) -> NvidiaLLM:
    """
    Get LLM instance.
    
    Args:
        model: Model to use
        **kwargs: Additional arguments for NvidiaLLM
    
    Returns:
        NvidiaLLM instance
    """
    global _default_llm
    
    if _default_llm is None or model:
        _default_llm = NvidiaLLM(model=model, **kwargs)
    
    return _default_llm


# Quick helper functions
def complete(prompt: str, **kwargs) -> str:
    """Quick completion helper."""
    llm = get_llm()
    response = llm.complete(prompt, **kwargs)
    return response.content


def chat(messages: List[Dict], **kwargs) -> str:
    """Quick chat helper."""
    llm = get_llm()
    response = llm.chat(messages, **kwargs)
    return response.content