class BaseParser(object):

    def get_variables(self):
        raise NotImplementedError("Method not implemented")

    def get_execution_args(self):
        raise NotImplementedError("Method not implemented")
