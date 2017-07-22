import os

class Config:
    home_path = os.path.dirname(os.path.realpath(__file__))
    data_path = os.path.join(home_path, '..', 'data')
    ont_path = os.path.join(data_path, '..', 'ont')
    mongo_db = 'bme'
    bme3_onto = "http://example.com/bme3.owl"
    tomita_path = '/opt/tomita-parser/build/bin/tomita-parser'

config = Config()
