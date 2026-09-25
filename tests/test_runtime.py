from jarvis.runtime.agents import default_agents
from jarvis.runtime.permissions import PermissionBroker, PermissionLevel
from jarvis.runtime.state import JarvisState, StateMachine
from jarvis.runtime.events import Event, EventBus

def test_default_agents_are_real_specs():
    agents=default_agents().list()
    assert len(agents)>=15
    assert all(a.mission and a.name for a in agents)

def test_permission_broker_gates_high():
    broker=PermissionBroker(PermissionLevel.CRITICAL)
    assert not broker.decide(PermissionLevel.HIGH).allowed
    assert broker.decide(PermissionLevel.HIGH, confirmed=True).allowed

def test_state_and_event_bus():
    sm=StateMachine(); assert sm.transition(JarvisState.THINKING)==JarvisState.THINKING
    seen=[]; bus=EventBus(); bus.subscribe("x",lambda e:seen.append(e.payload["v"])); bus.publish(Event("x",{"v":3})); assert seen==[3]
