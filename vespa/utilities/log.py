import logging


class LoggingMixIn(object):
    def __init__(self, args):
        levels = {'info': logging.INFO,
                  'debug': logging.DEBUG,
                  'error': logging.ERROR,
                  'warning': logging.warning}
        self.logger = logging
        FT = ("[%(asctime)s.%(msecs)03d:"
              " %(filename)s:%(lineno)s]"
              " %(levelname)s "
              "%(message)s")
        DATEFMT = '%I:%M:%S'
        self.logger.basicConfig(format=FT,
                                datefmt=DATEFMT,
                                level=levels.get(args.log_level, logging.INFO))
