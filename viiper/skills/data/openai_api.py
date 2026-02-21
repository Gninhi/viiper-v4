"""
OpenAI API Integration Skill.

LLM integration patterns for AI features.
"""

from typing import Dict, Any, Optional
from viiper.skills.base import Skill, SkillMetadata, SkillCategory, SkillDifficulty, Dependency, BestPractice, UsageExample, AntiPattern


class OpenAIAPISkill(Skill):
    """
    OpenAI API integration patterns.

    Features:
    - Chat completions
    - Embeddings
    - Function calling
    - Streaming responses
    - Rate limit handling
    - Token management
    """

    metadata: SkillMetadata = SkillMetadata(
        name="OpenAI API Integration",
        slug="openai-api",
        category=SkillCategory.DATA_ML_INTEGRATION,
        difficulty=SkillDifficulty.ADVANCED,
        tags=["openai", "llm", "ai", "chatgpt", "embeddings", "function-calling"],
        estimated_time_minutes=50,
        description="OpenAI API integration for AI features",
    )

    dependencies: list = [
        Dependency(name="openai", version="^4.24.0", package_manager="npm", reason="OpenAI SDK (Node.js)"),
        Dependency(name="openai", version="^1.7.0", package_manager="pip", reason="OpenAI SDK (Python)"),
        Dependency(name="tiktoken", version="^0.5.2", package_manager="pip", reason="Token counting"),
    ]

    best_practices: list = [
        BestPractice(title="Stream Responses", description="Stream tokens for better UX", code_reference="stream: true", benefit="Faster perceived response, lower latency"),
        BestPractice(title="Handle Rate Limits", description="Implement retry with backoff", code_reference="exponential backoff, max 3 retries", benefit="Resilient to API limits"),
        BestPractice(title="Token Management", description="Track and limit token usage", code_reference="tiktoken for counting", benefit="Cost control, prevent errors"),
        BestPractice(title="System Prompts", description="Clear role and constraints", code_reference="You are a helpful assistant specialized in...", benefit="Better, more consistent outputs"),
    ]

    usage_examples: list = [
        UsageExample(
            name="Chat Completions (Node.js)",
            description="Basic chat with streaming",
            code=r'''import OpenAI from 'openai';
import { StreamingTextResponse } from 'ai';

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export async function chatWithStreaming(messages: Array<{role: string, content: string}>) {
  const response = await openai.chat.completions.create({
    model: 'gpt-4-turbo-preview',
    messages: [
      {
        role: 'system',
        content: 'You are a helpful customer support assistant. Be concise and friendly.',
      },
      ...messages,
    ],
    stream: true,
    temperature: 0.7,
    max_tokens: 1000,
  });

  return new StreamingTextResponse(response);
}

// Non-streaming version
export async function chat(messages: Array<{role: string, content: string}>) {
  try {
    const response = await openai.chat.completions.create({
      model: 'gpt-4-turbo-preview',
      messages: [
        { role: 'system', content: 'You are a helpful assistant.' },
        ...messages,
      ],
      temperature: 0.7,
      max_tokens: 500,
    });

    return response.choices[0].message.content;
  } catch (error) {
    if (error instanceof OpenAI.RateLimitError) {
      // Handle rate limit
      await sleep(2000);
      return chat(messages);
    }
    throw error;
  }
}
''',
        ),
        UsageExample(
            name="Function Calling",
            description="Tool use with OpenAI",
            code=r'''import OpenAI from 'openai';

const openai = new OpenAI();

const tools: OpenAI.Chat.Completions.ChatCompletionTool[] = [
  {
    type: 'function',
    function: {
      name: 'get_weather',
      description: 'Get current weather for a location',
      parameters: {
        type: 'object',
        properties: {
          location: { type: 'string', description: 'City name' },
          unit: { type: 'string', enum: ['celsius', 'fahrenheit'] },
        },
        required: ['location'],
      },
    },
  },
  {
    type: 'function',
    function: {
      name: 'search_products',
      description: 'Search products in catalog',
      parameters: {
        type: 'object',
        properties: {
          query: { type: 'string', description: 'Search query' },
          category: { type: 'string' },
          maxPrice: { type: 'number' },
        },
        required: ['query'],
      },
    },
  },
];

export async function chatWithFunctions(messages: Array<{role: string, content: string}>) {
  const response = await openai.chat.completions.create({
    model: 'gpt-4-turbo-preview',
    messages,
    tools,
    tool_choice: 'auto',
  });

  const message = response.choices[0].message;

  // Check if model wants to call a function
  if (message.tool_calls) {
    for (const toolCall of message.tool_calls) {
      const args = JSON.parse(toolCall.function.arguments);

      let result;
      if (toolCall.function.name === 'get_weather') {
        result = await getWeather(args.location, args.unit);
      } else if (toolCall.function.name === 'search_products') {
        result = await searchProducts(args.query, args.category, args.maxPrice);
      }

      // Add function result to conversation
      messages.push({
        role: 'tool',
        tool_call_id: toolCall.id,
        content: JSON.stringify(result),
      });
    }

    // Get final response
    const finalResponse = await openai.chat.completions.create({
      model: 'gpt-4-turbo-preview',
      messages,
    });

    return finalResponse.choices[0].message.content;
  }

  return message.content;
}
''',
        ),
        UsageExample(
            name="Embeddings (Python)",
            description="Generate and store embeddings",
            code=r'''from openai import OpenAI
import numpy as np
from typing import List

client = OpenAI()

def generate_embedding(text: str, model: str = "text-embedding-3-small") -> List[float]:
    """Generate embedding for text"""
    response = client.embeddings.create(
        model=model,
        input=text,
    )
    return response.data[0].embedding

def generate_batch_embeddings(texts: List[str]) -> List[List[float]]:
    """Generate embeddings in batch"""
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts,
    )
    return [e.embedding for e in response.data]

def cosine_similarity(a: List[float], b: List[float]) -> float:
    """Calculate cosine similarity between vectors"""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Usage
text = "This is a sample text for embedding"
embedding = generate_embedding(text)
print(f"Embedding dimension: {len(embedding)}")

# For RAG: Store embeddings in vector DB (Pinecone, Weaviate, etc.)
''',
        ),
        UsageExample(
            name="Token Counting",
            description="Track token usage for cost control",
            code=r'''import { encoding_for_model } from 'tiktoken';

const encoder = encoding_for_model('gpt-4');

export function countTokens(text: string): number {
  return encoder.encode(text).length;
}

export function countMessageTokens(messages: Array<{role: string, content: string}>): number {
  let total = 0;
  for (const msg of messages) {
    total += countTokens(msg.content);
    // Add overhead for role
    total += 4;
  }
  // Add 2 for message start
  return total + 2;
}

export function truncateMessages(
  messages: Array<{role: string, content: string}>,
  maxTokens: number
): Array<{role: string, content: string}> {
  let tokens = countMessageTokens(messages);

  if (tokens <= maxTokens) return messages;

  // Remove oldest messages first
  const result = [...messages];
  while (tokens > maxTokens && result.length > 1) {
    result.shift();
    tokens = countMessageTokens(result);
  }

  return result;
}

// Usage
const messages = [{ role: 'user', content: 'Hello!' }];
const tokens = countMessageTokens(messages);
console.log(`Token count: ${tokens}`);
''',
        ),
    ]

    anti_patterns: list = [
        AntiPattern(bad="No Error Handling", why="Assuming API always succeeds", good="Handle rate limits, timeouts, errors"),
        AntiPattern(bad="Sending Sensitive Data", why="PII in API requests", good="Redact sensitive information"),
        AntiPattern(bad="No Token Limits", why="Unbounded conversations", good="Truncate old messages"),
        AntiPattern(bad="Trusting LLM Output", why="Using output without validation", good="Validate and sanitize responses"),
    ]

    def generate(self, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context = context or {}
        return {
            "files": {
                "services/openai/chat.ts": self.usage_examples[0].code,
                "services/openai/functions.ts": self.usage_examples[1].code,
                "services/openai/embeddings.py": self.usage_examples[2].code,
                "services/openai/tokens.ts": self.usage_examples[3].code,
            },
            "metadata": {},
        }
