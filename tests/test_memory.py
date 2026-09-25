from jarvis.memory import MemoryRepository

def test_memory_roundtrip(tmp_path):
    repo=MemoryRepository(tmp_path/"m.db")
    saved=repo.save("preference","Spanish")
    assert saved.content=="Spanish"
    assert repo.recent(1)[0].content=="Spanish"
