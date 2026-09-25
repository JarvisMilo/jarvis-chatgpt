from jarvis.memory import MemoryRepository


def test_memory_crud(tmp_path):
    repo = MemoryRepository(tmp_path / "m.db")
    saved = repo.save("preference", "Spanish")
    assert repo.get(saved.id).content == "Spanish"
    updated = repo.update(saved.id, content="Spanish, concise")
    assert updated.content == "Spanish, concise"
    assert repo.list(10)[0].content == "Spanish, concise"
