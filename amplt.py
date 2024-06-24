import ssl

import certifi
from amplitude import Amplitude, BaseEvent
from concurrent.futures import ThreadPoolExecutor

from config import settings

executor = ThreadPoolExecutor()
client = Amplitude(api_key=settings.amplitude_api_key)


#
def callback_fun(e, code, message):
    """A callback function"""
    print(e)
    print(code, message)


client.configuration.callback = callback_fun



def send_amplitude_event(user_id: str, event_type: str, event_properties: dict):
    def send_event_in_thread():
        try:
            event = BaseEvent(event_type=event_type, user_id=user_id, event_properties=event_properties)
            client.track(event)
            lst = client.flush()
            print(lst)
        except Exception as e:
            print(f"Error sending event to Amplitude: {e}")

    executor.submit(send_event_in_thread)


# Пример использования
async def log_user_action(user_id: str, action: str):
    event_type = 'user_action'
    event_properties = {'action': action}
    send_amplitude_event(user_id, event_type, event_properties)
