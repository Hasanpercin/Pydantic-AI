"""
AstraCalc Agent - N8N Report Generator

Level 2: Full chart report generation via N8N webhook
"""

import httpx
from typing import Dict, Any
import logging
from config import settings

logger = logging.getLogger(__name__)


async def generate_chart_report(
    ctx,
    birth_date: str,
    birth_time: str,
    city: str,
    latitude: float,
    longitude: float
) -> str:
    """
    Kullanıcı için tam doğum haritası raporu oluşturur.
    
    Bu tool N8N workflow'unu tetikler ve detaylı bir astroloji raporu döner.
    Kullanıcı "doğum haritamı çıkar", "tam rapor istiyorum" dediğinde kullan.
    
    Args:
        ctx: Pydantic AI RunContext (otomatik geçilir)
        birth_date: Doğum tarihi (YYYY-MM-DD formatında, örn: "1990-03-15")
        birth_time: Doğum saati (HH:MM formatında, örn: "14:30")
        city: Şehir adı (örn: "Istanbul")
        latitude: Enlem (örn: 41.0082)
        longitude: Boylam (örn: 28.9784)
    
    Returns:
        str: Rapor özeti veya rapor oluşturulma durumu
    """
    try:
        logger.info(f"Generating chart report for {city}, {birth_date} {birth_time}")
        
        # N8N webhook'a gönderilecek data
        webhook_data = {
            "birth_date": birth_date,
            "birth_time": birth_time,
            "birth_location": {
                "city": city,
                "lat": latitude,
                "lon": longitude
            }
        }
        
        # N8N webhook çağrısı
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                settings.N8N_WEBHOOK_URL,
                json=webhook_data
            )
            
            if response.status_code == 200:
                data = response.json()
                
                logger.info(f"N8N webhook success: {data}")
                
                # Response'u formatla
                result = f"✅ Doğum haritası raporu oluşturuldu!\n\n"
                result += f"📅 Doğum: {birth_date} {birth_time}\n"
                result += f"📍 Yer: {city}\n\n"
                
                # N8N'den gelen rapor datasını ekle
                # (N8N response formatına göre düzenlenecek)
                if "report" in data:
                    result += f"📊 Rapor Özeti:\n{data['report']}\n"
                
                if "report_id" in data:
                    result += f"\n🔗 Rapor ID: {data['report_id']}"
                
                return result
            else:
                error_msg = f"N8N webhook error: {response.status_code}"
                logger.error(f"{error_msg} - Response: {response.text}")
                return f"❌ Rapor oluşturma hatası: {error_msg}"
                
    except httpx.TimeoutException:
        logger.error("N8N webhook timeout")
        return "❌ Rapor oluşturulurken zaman aşımı oluştu. Lütfen tekrar deneyin."
    except Exception as e:
        logger.error(f"Error in generate_chart_report: {str(e)}")
        return f"❌ Rapor oluşturma hatası: {str(e)}"
