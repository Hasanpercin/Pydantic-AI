"""
AstraCalc Agent - Basic Tools

Level 1: First tool - get_current_date
"""

from datetime import datetime
from zoneinfo import ZoneInfo
import logging

logger = logging.getLogger(__name__)


def get_current_date() -> str:
    """
    Bugünün tarihini döndürür.
    
    Bu tool mevcut tarihi Türkiye saat diliminde (Europe/Istanbul) verir.
    Kullanıcı "bugün hangi gün", "tarih nedir", "ayın kaçı" gibi 
    sorular sorduğunda bu tool'u kullan.
    
    Returns:
        str: ISO format tarih (YYYY-MM-DD) ve gün adı
        Örnek: "2025-10-14 (Pazartesi)"
    """
    try:
        # Türkiye saati
        tz = ZoneInfo("Europe/Istanbul")
        now = datetime.now(tz)
        
        # Türkçe gün isimleri
        days_tr = {
            0: "Pazartesi",
            1: "Salı", 
            2: "Çarşamba",
            3: "Perşembe",
            4: "Cuma",
            5: "Cumartesi",
            6: "Pazar"
        }
        
        day_name = days_tr[now.weekday()]
        date_str = now.strftime("%Y-%m-%d")
        
        result = f"{date_str} ({day_name})"
        
        logger.info(f"get_current_date called: {result}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error in get_current_date: {str(e)}")
        return f"Tarih alınamadı: {str(e)}"
