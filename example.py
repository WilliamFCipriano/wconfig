import wconfig

data = wconfig.ini('test-files/basic.ini')

print(data.this_is_a_test)
wconfig.about()