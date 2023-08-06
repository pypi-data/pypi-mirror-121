class EasyMQLError(Exception):
    pass


class DatePartOutOfRangeError(EasyMQLError):
    pass


class EasyMQLSyntaxError(EasyMQLError):
    def __init__(self, qstr, emsg, line_no, col, **kwargs):
        self.qstr = qstr
        self.emsg = emsg
        self.line_no = line_no
        self.col = col
        for k, v in kwargs:
            setattr(self, k, v)

    def __str__(self):
        query_string = '\n'.join(
            [
                line
                for no, line in enumerate(self.qstr.splitlines())
                if no < self.line_no
            ]
        )
        marker_padding = ' ' * (self.col - 1)
        return (
            f'\n'
            f'{query_string}\n'
            f'{marker_padding}^\n'
            f'Error at line: {self.line_no}, col: {self.col}\n'
            f'{self.emsg}'
        )
