import os
import time
# import math
from smolagents import (
    CodeAgent,
    OpenAIServerModel,
    DuckDuckGoSearchTool,
    FinalAnswerTool,
)

def create_model():
    provider = os.getenv("MODEL_PROVIDER", "ollama").strip().lower()
    temperature = 0.5
    max_tokens = 2096

    if provider == "ollama":
        return OpenAIServerModel(
            model_id=os.getenv("OLLAMA_MODEL", "llama:latest"),
            api_base=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            api_key="ollama",
            temperature=temperature,
            max_tokens=max_tokens,
        )

    raise ValueError(f"Unsupported MODEL_PROVIDER: {provider}")


if __name__ == "__main__":

    agent = CodeAgent(
    tools=[DuckDuckGoSearchTool()],
    model=create_model(),
    max_steps=2,
    verbosity_level=2,
    )

    result = agent.run("What is the current weather in Paris?")
    print(result)

