import logging

logging.basicConfig(level = logging.DEBUG,
                    format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    filename = 'mag.log'
)

logger = logging.getLogger('MAG')