"""
AstraCalc Agent - Pydantic AI Agent Definition
Level 2: Agent with calculation engine and report tools
"""

from pydantic_ai import Agent, RunContext
from config import settings
from tools.basic import get_current_date
from tools.calculation import calculate_sun_sign
from tools.report import generate_chart_report
import logging

logger = logging.getLogger(__name__)


# System prompt
SYSTEM_PROMPT = """Sen AstraCalc AI, empatik ve bilgili bir astroloji danışmanısın.

ÖZELLİKLERİN:
- Kullanıcılara astroloji konularında yardımcı olursun
- Empatik ve destekleyici bir dil kullanırsın
- Açık ve anlaşılır açıklamalar yaparsın
- Her seviyeden kullanıcıya uygun iletişim kurarsun

TOOL'LARIN VE KULLANIM KURALLARI:

1. get_current_date
   - Kullanım: Bugünün tarihini öğrenmek için
   - Ne zaman: "bugün hangi gün", "tarih nedir" sorularında

2. get_sun_sign (HIZLI GÜNEŞ BURCU)
   - Kullanım: Güneş burcunu hesapla
   - Ne zaman: 
     * "Güneşim hangi burçta?"
     * "Burcum ne?"
     * "Hangi burçtanım?"
   - GEREKLİ BİLGİLER: Doğum tarihi (yıl, ay, gün), saati (saat, dakika), UTC offset (İstanbul: 3.0)
   - CEVAP STİLİ: Kısa ve öz! 2-3 cümle
   - Örnek: "Güneşiniz Balık burcunda 354°'de. Bu sizi empatik ve hayal gücü güçlü biri yapıyor."

3. generate_chart_report (N8N - DETAYLI RAPOR)
   - Kullanım: Tam doğum haritası raporu
   - Ne zaman:
     * "Doğum haritamı çıkar"
     * "Tam rapor istiyorum"
     * "Detaylı analiz yap"

ÖNEMLİ KURALLAR:
- Doğum bilgisi sorularında MUTLAKA: yıl, ay, gün, saat, dakika bilgisi iste
- Eksik bilgi varsa kibarca sor, ASLA tahmin etme
- UTC offset için İstanbul kullanıcıları için 3.0 kullan (varsayılan)
- Basit sorular = get_sun_sign (hızlı)
- Detaylı analiz = generate_chart_report (tam rapor)

Kullanıcıya nazik bir şekilde karşılık ver ve astroloji konularında yardımcı ol.
"""


async def get_sun_sign_tool(
    ctx: RunContext[None],
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    tz_offset: float = 3.0
) -> str:
    """
    Kullanıcının güneş burcunu hesapla.
    
    Args:
        ctx: Pydantic AI RunContext (otomatik geçilir)
        year: Doğum yılı (örn: 1990)
        month: Doğum ayı (1-12)
        day: Doğum günü (1-31)
        hour: Doğum saati (0-23)
        minute: Doğum dakikası (0-59)
        tz_offset: UTC offset (İstanbul için 3.0, varsayılan)
    
    Returns:
        str: Güneş burcu ve derece bilgisi
    """
    try:
        logger.info(f"🌞 Güneş burcu hesaplanıyor: {year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}")
        
        result = await calculate_sun_sign(year, month, day, hour, minute, tz_offset)
        
        response = f"""🌞 Güneş Burcunuz: {result['sun_sign']}

📊 Detaylar:
- Derece: {result['sun_degree']}°
- UTC Zaman: {result['ts_utc']}

{result['sun_sign']} burcu, sizin temel karakterinizi ve ego yapınızı temsil eder."""
        
        return response
        
    except Exception as e:
        logger.error(f"❌ Güneş burcu hesaplamasında hata: {str(e)}")
        return f"❌ Güneş burcunu hesaplarken bir hata oluştu. Lütfen doğum bilgilerinizi kontrol edin ve tekrar deneyin."


def create_agent() -> Agent:
    """
    Create and configure the Pydantic AI agent
    
    Level 2: Agent with calculation and report tools
    """
    logger.info("Creating Pydantic AI agent with tools...")
    
    agent = Agent(
        model=settings.ANTHROPIC_MODEL,
        system_prompt=SYSTEM_PROMPT,
    )
    
    # Register tools
    agent.tool(get_current_date)
    agent.tool(get_sun_sign_tool)
    agent.tool(generate_chart_report)
    
    logger.info("Agent created successfully with 3 tools")
    return agent
