import pytest

from pattern_memory_isolation import MemoryRecord, MemoryStore, MemoryWriteRejected


def test_session_memory_is_isolated_by_owner() -> None:
    store = MemoryStore()
    store.write(MemoryRecord("session", "user-a", "last_message", "hello", "low"))
    store.write(MemoryRecord("session", "user-b", "last_message", "private", "low"))
    assert [record.value for record in store.read("session", "user-a")] == ["hello"]


def test_user_preference_requires_allowed_key_and_validation() -> None:
    store = MemoryStore()
    with pytest.raises(MemoryWriteRejected):
        store.write(MemoryRecord("user_preference", "user-a", "api_key", "secret", "medium", validated=True))
    store.write(MemoryRecord("user_preference", "user-a", "timezone", "Asia/Kolkata", "medium", validated=True))
    assert store.read("user_preference", "user-a")[0].value == "Asia/Kolkata"


def test_long_term_knowledge_requires_validation() -> None:
    store = MemoryStore()
    with pytest.raises(MemoryWriteRejected):
        store.write(MemoryRecord("long_term_knowledge", "tenant-a", "fact", "Orders use v2 API", "medium"))


def test_audit_record_cannot_be_written_as_memory() -> None:
    store = MemoryStore()
    with pytest.raises(MemoryWriteRejected):
        store.write(MemoryRecord("audit_record", "user-a", "event", {"x": 1}, "high", validated=True))
