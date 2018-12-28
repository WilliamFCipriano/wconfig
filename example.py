import wconfig

# Load a INI file
example_ini = wconfig.load_ini('test-files/example.ini')

# Read a property from the INI
example_ini.lookup_by_key('arbitrary property name')

# It even works if you mess up the capitalization
example_ini.lookup_by_key('arBitrAry propErty Name')



