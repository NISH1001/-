
class DBHandlerError(Exception):
    def __init__(self, args):
        self.args = args

    def Display(self):
        print(''.join(self.args))
