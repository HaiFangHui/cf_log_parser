import logging
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("log_parser.cfg")

level = logging.WARN
if config.getboolean('LOG', 'DEBUG'):
    level = logging.DEBUG

logging.basicConfig(level=level,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M')
