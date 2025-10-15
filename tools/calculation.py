# Yedek al
cp tools/calculation.py tools/calculation.py.backup

# Yeni içeriği yaz
cat > tools/calculation.py << 'EOF'
# backend/tools/calculation.py
"""
Calculation Engine Integration
Connects to Calculation Engine API for astrological calculations
"""

import httpx
from datetime import datetime
from typing import Optional, Dict, Any
import logging
from config import settings

logger = logging.getLogger(__name__)

# Burç isimleri (sign_index -> Türkçe isim)
ZODIAC_SIGNS = [
    "Koç",      # 0 - Aries
    "Boğa",     # 1 - Taurus
    "İkizler",  # 2 - Gemini
    "Yengeç",   # 3 - Cancer
    "Aslan",    # 4 - Leo
    "Başak",    # 5 - Virgo
    "Terazi",   # 6 - Libra
    "Akrep",    # 7 - Scorpio
    "Yay",      # 8 - Sagittarius
    "Oğlak",    # 9 - Capricorn
    "Kova",     # 10 - Aquarius
    "Balık"     # 11 - Pisces
]


async def calculate_sun_sign(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    tz_offset: float = 3.0
) -> Dict[str, Any]:
    """
    Güneş burcunu hesapla
    
    Args:
        year: Doğum yılı (örn: 1990)
        month: Doğum ayı (1-12)
        day: Doğum günü (1-31)
        hour: Doğum saati (0-23)
        minute: Doğum dakikası (0-59)
        tz_offset: UTC offset (İstanbul için 3.0)
    
    Returns:
        {
            "sun_sign": "Balık",
            "sun_degree": 354.6,
            "ts_utc": "1990-03-15T11:30:00+00:00"
        }
    """
    try:
        request_data = {
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "tz_offset": tz_offset
        }
        
        logger.info(f"📡 Calculation Engine'e istek: {request_data}")
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{settings.CALCULATION_ENGINE_URL}/natal/basic",
                json=request_data,
                headers={
                    "Content-Type": "application/json",
                    **({"X-API-Key": settings.CALCULATION_ENGINE_API_KEY} 
                       if settings.CALCULATION_ENGINE_API_KEY else {})
                }
            )
            response.raise_for_status()
            data = response.json()
        
        logger.info(f"✅ Calculation Engine yanıtı alındı")
        
        # Güneş'i bul (lowercase "sun")
        sun_data = next(
            (body for body in data["bodies"] if body["name"].lower() == "sun"),
            None
        )
        
        if not sun_data:
            logger.error(f"❌ Güneş verisi bulunamadı")
            raise ValueError("Güneş verisi bulunamadı")
        
        sign_index = sun_data["sign_index"]
        sun_sign = ZODIAC_SIGNS[sign_index]
        
        result = {
            "sun_sign": sun_sign,
            "sun_degree": round(sun_data["lon"], 2),
            "ts_utc": data["ts_utc"]
        }
        
        logger.info(f"🌞 Sonuç: {result}")
        return result
        
    except Exception as e:
        logger.error(f"❌ Hata: {str(e)}")
        raise


async def test_calculation_engine() -> bool:
    """Calculation Engine bağlantısını test et"""
    try:
        test_data = {
            "year": 2000,
            "month": 1,
            "day": 1,
            "hour": 12,
            "minute": 0,
            "tz_offset": 0.0
        }
        
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{settings.CALCULATION_ENGINE_URL}/natal/basic",
                json=test_data
            )
            return response.status_code == 200
    except:
        return False
EOF

# Dosyayı kontrol et
head -30 tools/calculation.py
