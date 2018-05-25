import pytest
import serial
import uuid


@pytest.fixture(scope="session")
def test_uuid():
    test_uuid = uuid.uuid4()
    print(test_uuid)
    return test_uuid

# /etc/udev/rules.d/42-osh-hil.rules
# ACTION=="add", ATTRS{product}=="digital_1O1I", SYMLINK+="digital_1O1I"
@pytest.fixture(scope="function")
def ser():
    with serial.Serial(
        port='/dev/ttyUSB0',
        baudrate=9600,
        dsrdtr=True,
        rtscts=True) as ser:
        yield ser
