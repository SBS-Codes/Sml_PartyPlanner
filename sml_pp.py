import os
import time
import datetime
import mlflow

from smolagents import (
    CodeAgent,
    OpenAIServerModel,
    Tool,
    tool,
    DuckDuckGoSearchTool,
    VisitWebpageTool,
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

@tool
def suggest_menu(occasion: str) -> str:
    """
    Suggests a menu based on the occasion.
    Args:
        occasion (str): The type of occasion for the party. Allowed values are:
                        - "casual": Menu for casual party.
                        - "formal": Menu for formal party.
                        - "superhero": Menu for superhero party.
                        - "custom": Custom menu.
    """
    if occasion == "casual":
        return "Pizza, snacks, and drinks."
    elif occasion == "formal":
        return "3-course dinner with wine and dessert."
    elif occasion == "superhero":
        return "Buffet with high-energy and healthy food."
    else:
        return "Custom menu for the butler."

@tool   
def catering_service_tool(query: str) -> str:
    """
    This tool returns the highest-rated catering service in Gotham City.
    
    Args:
        query: A search term for finding catering services.
    """
    # Example list of catering services and their ratings
    services = {
        "Gotham Catering Co.": 4.9,
        "Wayne Manor Catering": 4.8,
        "Gotham City Events": 4.7,
    }
    
    # Find the highest rated catering service (simulating search query filtering)
    best_service = max(services, key=services.get)
    
    return best_service

class SuperheroPartyThemeTool(Tool):
    name = "superhero_party_theme_generator"
    description = """
    This tool suggests creative superhero-themed party ideas based on a category.
    It returns a unique party theme idea."""
    
    inputs = {
        "category": {
            "type": "string",
            "description": "The type of superhero party (e.g., 'classic heroes', 'villain masquerade', 'futuristic Gotham').",
        }
    }
    
    output_type = "string"

    def forward(self, category: str):
        themes = {
            "classic heroes": "Justice League Gala: Guests come dressed as their favorite DC heroes with themed cocktails like 'The Kryptonite Punch'.",
            "villain masquerade": "Gotham Rogues' Ball: A mysterious masquerade where guests dress as classic Batman villains.",
            "futuristic gotham": "Neo-Gotham Night: A cyberpunk-style party inspired by Batman Beyond, with neon decorations and futuristic gadgets."
        }
        
        return themes.get(category.lower(), "Themed party idea not found. Try 'classic heroes', 'villain masquerade', or 'futuristic Gotham'.")


if __name__ == "__main__":
    mlflow.smolagents.autolog() 
    agent = CodeAgent(
    tools=[
        DuckDuckGoSearchTool(), 
        VisitWebpageTool(),
        suggest_menu,
        catering_service_tool,
        SuperheroPartyThemeTool(),
	    FinalAnswerTool()
    ], 
    model=create_model(),
    max_steps=5,
    verbosity_level=2,
    additional_authorized_imports=['datetime']
)

    # agent.run("Prepare a formal menu for the party.")
    # agent = CodeAgent(tools=[suggest_menu], model=create_model(), max_steps=3)
    agent.run(
        """
        Alfred needs to prepare for the party. Here are the tasks:
        1. Prepare the drinks - 30 minutes
        2. Decorate the mansion - 60 minutes
        3. Set up the menu - 45 minutes
        4. Prepare the music and playlist - 45 minutes

        If we start right now, at what time will the party be ready?
        """
    )
