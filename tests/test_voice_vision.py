from jarvis.vision.interfaces import Observation
from jarvis.voice.interfaces import VoiceManager

def test_interfaces_are_optional():
    assert Observation(source="test").source=="test"
    assert VoiceManager().stt is None
