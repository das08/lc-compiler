class REG_ERROR(Exception):
    def __init__(self, msg: str) -> None:
        super(REG_ERROR, self).__init__(msg)


class REG_CONSTRUCT_ERROR(REG_ERROR):
    def __init__(self, msg: str) -> None:
        super(REG_CONSTRUCT_ERROR, self).__init__(msg)


class REG_DECLARATION_ERROR(REG_ERROR):
    def __init__(self, msg: str) -> None:
        super(REG_DECLARATION_ERROR, self).__init__(msg)


class IMM_ERROR(Exception):
    def __init__(self, msg: str) -> None:
        super(IMM_ERROR, self).__init__(msg)


class IMM_CONSTRUCT_ERROR(IMM_ERROR):
    def __init__(self, msg: str) -> None:
        super(IMM_CONSTRUCT_ERROR, self).__init__(msg)


class OPERATOR_ERROR(Exception):
    def __init__(self, msg: str) -> None:
        super(OPERATOR_ERROR, self).__init__(msg)


class OPERATOR_CONSTRUCT_ERROR(OPERATOR_ERROR):
    def __init__(self, msg: str) -> None:
        super(OPERATOR_CONSTRUCT_ERROR, self).__init__(msg)
