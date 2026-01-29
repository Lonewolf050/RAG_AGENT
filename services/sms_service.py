from twilio.rest import Client
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import settings


def send_sms(to_number, message):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        msg = client.messages.create(
            body=message[:1600],
            from_=settings.TWILIO_PHONE_NUMBER,
            to=to_number
        )
        
        return {"success": True, "sid": msg.sid}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_sms_service():
    return send_sms
