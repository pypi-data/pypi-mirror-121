class Action:
    @staticmethod
    def action(tokens):
        return tokens


class ExpressionAction(Action):
    @staticmethod
    def action(tokens):
        return {
            '$'
            + ''.join(
                [
                    part.capitalize() if i else part
                    for i, part in enumerate(tokens[0].lower().split('_'))
                ]
            ): tokens[1:]
        }


class UnaryExpressionAction(Action):
    @staticmethod
    def action(tokens):
        return {
            '$'
            + ''.join(
                [
                    part.capitalize() if i else part
                    for i, part in enumerate(tokens[0].lower().split('_'))
                ]
            ): tokens[-1]
        }
