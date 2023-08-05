from tracardi.domain.context import Context
from tracardi.domain.entity import Entity
from tracardi.domain.event import Event
from tracardi.domain.profile import Profile
from tracardi.domain.session import Session
from tracardi_plugin_sdk.service.plugin_runner import run_plugin

from tracardi_text_classification.plugin import TextClassificationAction

init = {
    "source": {
        "id": "75b367da-9adc-46c9-a4b2-99087e10e3ff"
    },
    "language": "en",
    "model": "press",
    "title": "payload@title",
    "text": "payload@text"
}
payload = {
    "title": "iPhone 13 is here",
    "text": "The iPhone 13 isn’t a game changer for Apple’s series of smartphones, but it’s an important "
            "iteration that offers better battery life, a better processor and an upgraded camera setup than "
            "iPhones that have gone before it. If you’re looking for a fast and capable smartphone, and don’t "
            "need the extra features of the pricier Pro model, this is a top choice."
}
profile = Profile(id="profile-id")
event = Event(id="event-id",
              type="event-type",
              profile=profile,
              session=Session(id="session-id"),
              source=Entity(id="source-id"),
              context=Context())
result = run_plugin(TextClassificationAction, init, payload,
                    profile)

print("OUTPUT:", result.output)
print("PROFILE:", result.profile)
