"""
AstraCalc Agent - Calculation Engine Tools

Level 2: Direct calculation engine calls for quick astrology data
"""

import httpx
from datetime import datetime
from typing import Dict, Any
import logging
from config import settings

logger = logging.getLogger(__name__)


async def get_planet_positions(
    ctx,
    birth_date: str,
    birth_time: str,
    latitude: float,
    longitude: float,
    city: str = "Unknown"
) -> str:
    """
    Doğum anındaki gezegen pozisyonlarını hesaplar.
    
    Kullanıcı doğum bilgilerini verdiğinde (tarih, saat, yer) bu tool ile
    hızlıca gezegen pozisyonlarını öğrenebilirsin.
    
    Args:
        ctx: Pydantic AI RunContext (otomatik geçilir)
        birth_date: Doğum tarihi (YYYY-MM-DD formatında, örn: "1990-03-15")
        birth_time: Doğum saati (HH:MM formatında, örn: "14:30")
        latitude: Enlem (örn: 41.0082 İstanbul için)
        longitude: Boylam (örn: 28.9784 İstanbul için)
        city: Şehir adı (opsiyonel, bilgi amaçlı)
    
    Returns:
        str: Gezegen pozisyonları ve burç bilgileri
    """
    try:
        # Tarih ve saati birleştir
        datetime_str = f"{birth_date}T{birth_time}:00"
        
        logger.info(f"Calculating planets for {datetime_str} at {city} ({latitude}, {longitude})")
        
        # Calculation Engine API çağrısı
        # Engine reposunda endpoint kontrol edilmeli
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{settings.CALCULATION_ENGINE_URL}/natal",
                json={
                    "datetime": datetime_str,
                    "latitude": latitude,
                    "longitude": longitude
                },
                headers={
                    "Authorization": f"Bearer {settings.CALCULATION_ENGINE_API_KEY}"
                } if settings.CALCULATION_ENGINE_API_KEY else {}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Response'u formatla
                result = f"🌟 Doğum Bilgileri: {city}\n"
                result += f"📅 Tarih: {birth_date} {birth_time}\n"
                result += f"📍 Konum: {latitude}, {longitude}\n\n"
                
                # Gezegenleri formatla (API response yapısına göre düzenlenecek)
                if "planets" in data:
                    result += "Gezegenler:\n"
                    for planet, info in data["planets"].items():
                        result += f"  {planet}: {info.get('sign', '?')} {info.get('degree', '?')}°\n"
                
                logger.info(f"Successfully calculated planets for {city}")
                return result
            else:
                error_msg = f"Calculation Engine error: {response.status_code}"
                logger.error(error_msg)
                return f"❌ Hesaplama hatası: {error_msg}"
                
    except httpx.TimeoutException:
        logger.error("Calculation Engine timeout")
        return "❌ Calculation Engine'e bağlanırken zaman aşımı oluştu."
    except Exception as e:
        logger.error(f"Error in get_planet_positions: {str(e)}")
        return f"❌ Hesaplama hatası: {str(e)}"
