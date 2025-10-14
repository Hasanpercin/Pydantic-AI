"""
AstraCalc Agent - Pydantic AI Agent Definition

Level 1: Agent with first tool (get_current_date)
"""

from pydantic_ai import Agent
from config import settings
from tools.basic import get_current_date
import logging

logger = logging.getLogger(__name__)


# System prompt
SYSTEM_PROMPT = """Sen AstraCalc AI, empatik ve bilgili bir astroloji danışmanısın.

ÖZELLİKLERİN:
- Kullanıcılara astroloji konularında yardımcı olursun
- Empatik ve destekleyici bir dil kullanırsun
- Açık ve anlaşılır açıklamalar yaparsın
- Her seviyeden kullanıcıya uygun iletişim kurarsun

TOOL'LARIN:
- get_current_date: Bugünün tarihini öğrenmek için kullan
- Kullanıcı tarih, gün sorduğunda bu tool'u çağır

ŞU AN:
- Bu Level 1 versiyonudur
- Tool calling aktif!
- Tarih bilgisine erişebiliyorsun
- Daha fazla tool yakında gelecek!

Kullanıcıya nazik bir şekilde karşılık ver ve astroloji konularında yardımcı ol.
"""


def create_agent() -> Agent:
    """
    Create and configure the Pydantic AI agent
    
    Level 1: Agent with first tool
    """
    logger.info("Creating Pydantic AI agent with tools...")
    
    agent = Agent(
        model=settings.ANTHROPIC_MODEL,
        system_prompt=SYSTEM_PROMPT,
    )
    
    # Register tools
    agent.tool(get_current_date)
    
    logger.info("Agent created successfully with 1 tool")
    return agent
