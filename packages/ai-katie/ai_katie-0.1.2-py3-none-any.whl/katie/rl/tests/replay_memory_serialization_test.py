import os
import pickle
import pytest
from katie.rl.replay_memory import ReplayMemory

_file_name = "buffer.pickle"
_file_name2 = "buffer2.pickle"
_file_name_no_extension = "buffer"
_file_hash = "buffer.SHA256"
_file_hash2 = "buffer2.SHA256"


def _fill_memory(replay_memory: ReplayMemory, data: str = ""):
    for n in range(0, replay_memory.get_capacity()):
        replay_memory.append_memory(str(n) + data)


def test_save_memory():
    rm = ReplayMemory()
    _fill_memory(rm)
    rm.save_memory_buffer(_file_name)
    assert (os.path.exists(_file_name))
    os.remove(_file_name)


def test_save_memory_wrong_file_format():
    rm = ReplayMemory()
    _fill_memory(rm)
    with pytest.raises(TypeError):
        rm.save_memory_buffer(_file_name_no_extension)


def test_save_memory_hash():
    rm = ReplayMemory()
    _fill_memory(rm)
    rm.save_memory_buffer(_file_name, hash=True)
    assert (os.path.exists(_file_hash))
    os.remove(_file_name)
    os.remove(_file_hash)


def test_load_memory():
    rm = ReplayMemory()
    _fill_memory(rm)
    rm.save_memory_buffer(_file_name)
    assert (os.path.exists(_file_name))

    rm_load = ReplayMemory()
    rm_load.load_memory_buffer(_file_name)

    assert (rm._buffer == rm_load._buffer)
    os.remove(_file_name)


def test_load_memory_no_existing_file():
    rm = ReplayMemory()
    with pytest.raises(FileNotFoundError):
        rm.load_memory_buffer(_file_name)


def test_load_memory_wrong_format_file():
    rm = ReplayMemory()
    with pytest.raises(TypeError):
        rm.load_memory_buffer(_file_name_no_extension)


def test_load_memory_buffer_is_cleaned():
    rm = ReplayMemory()
    _fill_memory(rm)
    rm.save_memory_buffer(_file_name)
    assert (os.path.exists(_file_name))

    rm_load = ReplayMemory()
    _fill_memory(rm_load, data="TEST")
    rm_load.load_memory_buffer(_file_name)

    assert (rm._buffer == rm_load._buffer)
    os.remove(_file_name)


def test_load_memory_do_not_corrupt_buffer_when_fails():
    rm = ReplayMemory()
    _fill_memory(rm, data="TEST")
    buffer_copy = rm._buffer.copy()

    with pytest.raises(TypeError):
        rm.load_memory_buffer(_file_name_no_extension)
    assert (buffer_copy == rm._buffer)

    with pytest.raises(FileNotFoundError):
        rm.load_memory_buffer(_file_name2)
    assert (buffer_copy == rm._buffer)


def test_load_memory_keeps_the_set_capacity():
    rm = ReplayMemory(capacity=1000)
    _fill_memory(rm)
    rm.save_memory_buffer(_file_name)

    rm_2 = ReplayMemory(capacity=500)
    rm_2.load_memory_buffer(_file_name)

    assert (len(rm_2._buffer) == rm_2._capacity)
    os.remove(_file_name)


def test_load_memory_not_fails_when_pickle_content_not_iterable():
    test_pickle = 15000
    with open(_file_name, "wb") as f:
        pickle.dump(test_pickle, f)
    rm = ReplayMemory()
    with pytest.raises(TypeError):
        rm.load_memory_buffer(_file_name)
    os.remove(_file_name)


def test_load_hash_memory():
    rm = ReplayMemory()
    _fill_memory(rm)
    rm.save_memory_buffer(_file_name, hash=True)
    assert (os.path.exists(_file_name))
    assert (os.path.exists(_file_hash))

    rm_load = ReplayMemory()
    rm_load.load_memory_buffer(_file_name, _file_hash)

    assert (rm._buffer == rm_load._buffer)
    os.remove(_file_name)
    os.remove(_file_hash)


def test_load_hash_memory_with_wrong_hash():
    rm = ReplayMemory()
    _fill_memory(rm)
    rm.save_memory_buffer(_file_name, hash=True)
    assert (os.path.exists(_file_name))
    assert (os.path.exists(_file_hash))

    rm2 = ReplayMemory()
    _fill_memory(rm2, data="TEST")
    rm2.save_memory_buffer(_file_name2, hash=True)
    assert (os.path.exists(_file_name2))
    assert (os.path.exists(_file_hash2))

    rm_load = ReplayMemory()
    with pytest.raises(BufferError):
        rm_load.load_memory_buffer(_file_name, _file_hash2)
    with pytest.raises(BufferError):
        rm_load.load_memory_buffer(_file_name2, _file_hash)

    os.remove(_file_name)
    os.remove(_file_hash)
    os.remove(_file_name2)
    os.remove(_file_hash2)


def test_load_hash_memory_no_hash_file():
    rm = ReplayMemory()
    _fill_memory(rm)
    rm.save_memory_buffer(_file_name)
    assert (os.path.exists(_file_name))

    rm_load = ReplayMemory()
    with pytest.raises(FileNotFoundError):
        rm_load.load_memory_buffer(_file_name, _file_hash)

    os.remove(_file_name)


def test_load_hash_memory_hash_file_wrong_format():
    rm = ReplayMemory()
    _fill_memory(rm)
    rm.save_memory_buffer(_file_name)
    assert (os.path.exists(_file_name))

    rm_load = ReplayMemory()
    with pytest.raises(TypeError):
        rm_load.load_memory_buffer(_file_name, _file_name_no_extension)

    os.remove(_file_name)
