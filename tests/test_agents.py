from jarvis.agents import build_builtin_agents
from jarvis.runtime.agent_runtime import AgentRuntime

def test_minimum_agent_team():
    agents=build_builtin_agents()
    assert len(agents) >= 15
    assert {"Planner","Computer Control","File System","Browser","Research","Coding","Vision","Voice","Memory","Security Policy","QA Verification"} <= set(agents)

def test_agent_runtime_executes_by_id():
    runtime=AgentRuntime(); result=runtime.run("QA Verification", {"check":"demo"}, "task-1")
    assert result.success if hasattr(result,"success") else result.status == "SUCCESS"
