
def test_DTR_False(ser):
    ser.dtr=False
    assert ser.cts == False
    
def test_DTR_True(ser):
    ser.dtr=True
    assert ser.cts == True
