__VERSION__ = '0.1'
__AUTHOR__ = 'Galkan'
__DATE__ = '2013'


class SeesExceptions(Exception):
        def __init__(self, err_mess):
                self.err = err_mess

        def __str__(self):
                return self.err

