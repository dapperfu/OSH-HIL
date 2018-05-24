import pytest
import serial
import uuid


@pytest.fixture(scope="session")
def test_uuid():
    test_uuid = uuid.uuid4()
    print(test_uuid)
    return test_uuid

@pytest.fixture(scope="function")
def ser():
    with serial.Serial(
        port='/dev/ttyUSB1',
        baudrate=9600,
        dsrdtr=True,
        rtscts=True) as ser:
        yield ser
