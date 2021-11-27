class BaseParser(object):

    def get_variables(self, message: bytes):
        raise NotImplementedError("Method not implemented")
