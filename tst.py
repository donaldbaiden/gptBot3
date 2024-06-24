from amplitude import Amplitude, BaseEvent
from concurrent.futures import ThreadPoolExecutor
from config import settings

# Initialize the Amplitude client
client = Amplitude(settings.amplitude_api_key)


# Define a function to send an event
def send_event(user_id, event_type, event_properties):
    event = BaseEvent(
        event_type=event_type,
        user_id=user_id,
        event_properties=event_properties
    )
    print(event)
    client.track(event)


# List of events to send
events = [
    {"user_id": "user1", "event_type": "event1", "event_properties": {"key1": "value1"}},
    {"user_id": "user2", "event_type": "event2", "event_properties": {"key2": "value2"}},
    # Add more events as needed
]

# Use ThreadPoolExecutor to send events concurrently
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(send_event, event["user_id"], event["event_type"], event["event_properties"]) for event
               in events]

# Optionally, wait for all futures to complete
for future in futures:
    future.result()

# Flush the event buffer to ensure all events are sent
client.flush()
