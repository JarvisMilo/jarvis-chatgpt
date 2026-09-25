from __future__ import annotations
from enum import Enum

class JarvisState(str, Enum):
    SLEEPING="SLEEPING"; LISTENING="LISTENING"; THINKING="THINKING"; PLANNING="PLANNING"; EXECUTING="EXECUTING"; WAITING="WAITING"; ASKING_PERMISSION="ASKING_PERMISSION"; VERIFYING="VERIFYING"; SUCCESS="SUCCESS"; ERROR="ERROR"; RECOVERING="RECOVERING"; SPEAKING="SPEAKING"

class StateMachine:
    def __init__(self, initial: JarvisState=JarvisState.SLEEPING) -> None: self.state=initial
    def transition(self, state: JarvisState) -> JarvisState:
        self.state=state; return state
