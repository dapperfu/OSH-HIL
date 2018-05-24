import time

def test_DTR_False(ser):
    ser.dtr=False
    time.sleep(0.5)
    assert ser.cts == False
    
def test_DTR_True(ser):
    ser.dtr=True
    time.sleep(0.5)
    assert ser.cts == True
