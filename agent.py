"""
AstraCalc Agent - Pydantic AI Agent Definition

Level 0: Basic agent without tools
"""

from pydantic_ai import Agent
from config import settings
import logging

logger = logging.getLogger(__name__)


# System prompt
SYSTEM_PROMPT = """Sen AstraCalc AI, empatik ve bilgili bir astroloji danışmanısın.

ÖZELLİKLERİN:
- Kullanıcılara astroloji konularında yardımcı olursun
- Empatik ve destekleyici bir dil kullanırsun
- Açık ve anlaşılır açıklamalar yaparsın
- Her seviyeden kullanıcıya uygun iletişim kurarsun

ŞU AN:
- Bu Level 0 versiyonudur
- Henüz tool'lar aktif değil
- Basit sohbet yapabiliyorsun
- Yakında çok daha güçlü olacaksın!

Kullanıcıya nazik bir şekilde karşılık ver ve astroloji konularında yardımcı ol.
"""


def create_agent() -> Agent:
    """
    Creates and returns a Pydantic AI agent
    
    Level 0: Basic agent with system prompt only
    No tools, no dependencies yet
    """
    logger.info("Creating Pydantic AI agent...")
    logger.info(f"Model: {settings.ANTHROPIC_MODEL}")
    
    agent = Agent(
        model=settings.ANTHROPIC_MODEL,
        system_prompt=SYSTEM_PROMPT,
        retries=2,  # Retry on failure
    )
    
    logger.info("Agent created successfully!")
    return agent


# For testing
if __name__ == "__main__":
    agent = create_agent()
    
    # Test the agent
    print("\n🧪 Testing agent...")
    result = agent.run_sync("Merhaba!")
    print(f"\n✅ Agent response: {result.data}\n")