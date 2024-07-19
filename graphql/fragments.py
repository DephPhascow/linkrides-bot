from .core.utils import gen_fragment

def fragment_operation_info():
    return gen_fragment(
        name="operationInfo",
        request="""
            messages {
                kind
                message
                field
                code
            }
        """,
        type_name="OperationInfo",
    )