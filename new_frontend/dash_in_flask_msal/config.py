import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    BRAND = os.environ.get('Super Duper Comparison Thingy') or 'Super Duper Comparison Thingy'

