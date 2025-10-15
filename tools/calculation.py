# backend/tools/calculation.py

import httpx
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)

CALCULATION_ENGINE_URL = "http://calculation-engine:8001"

# Burç isimleri (sign_index -> isim)
ZODIAC_SIGNS = [
    "Koç",      # 0
    "Boğa",     # 1
    "İkizler",  # 2
    "Yengeç",   # 3
    "Aslan",    # 4
    "Başak",    # 5
    "Terazi",   # 6
    "Akrep",    # 7
    "Yay",      # 8
    "Oğlak",    # 9
    "Kova",     # 10
    "Balık"     # 11
]


async def calculate_sun_sign(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    tz_offset: float = 3.0  # İstanbul için varsayılan
) -> dict:
    """
    Güneş burcunu hesapla
    
    Args:
        year: Doğum yılı
        month: Doğum ayı (1-12)
        day: Doğum günü (1-31)
        hour: Doğum saati (0-23)
        minute: Doğum dakikası (0-59)
        tz_offset: UTC offset (İstanbul için 3.0)
    
    Returns:
        {
            "sun_sign": "Balık",
            "sun_degree": 354.5,
            "ts_utc": "1990-03-15T11:30:00Z"
        }
    """
    try:
        # 1️⃣ Request hazırla
        request_data = {
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "tz_offset": tz_offset
        }
        
        logger.info(f"📡 Calculation Engine'e istek gönderiliyor: {request_data}")
        
        # 2️⃣ API'ye istek gönder
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{CALCULATION_ENGINE_URL}/natal/basic",
                json=request_data,
                timeout=10.0
            )
            response.raise_for_status()
            data = response.json()
        
        logger.info(f"✅ Calculation Engine yanıtı alındı")
        
        # 3️⃣ Güneş'i bul
        sun_data = next(
            (body for body in data["bodies"] if body["name"] == "Sun"),
            None
        )
        
        if not sun_data:
            raise ValueError("Güneş verisi bulunamadı")
        
        # 4️⃣ Burç ismini çevir
        sign_index = sun_data["sign_index"]
        sun_sign = ZODIAC_SIGNS[sign_index]
        
        result = {
            "sun_sign": sun_sign,
            "sun_degree": sun_data["lon"],
            "ts_utc": data["ts_utc"]
        }
        
        logger.info(f"🌞 Sonuç: {result}")
        return result
        
    except httpx.HTTPError as e:
        logger.error(f"❌ HTTP hatası: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"❌ Genel hata: {str(e)}")
        raise


async def test_connection() -> bool:
    """
    Calculation Engine bağlantısını test et
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{CALCULATION_ENGINE_URL}/health",
                timeout=5.0
            )
            return response.status_code == 200
    except Exception as e:
        logger.error(f"❌ Bağlantı testi başarısız: {str(e)}")
        return False
