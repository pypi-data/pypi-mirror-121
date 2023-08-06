import pydantic


class CustomFunctionData(pydantic.BaseModel):
    name: str = pydantic.Field(description="The name of a custom function")

    num_io_qubits: pydantic.conint(ge=1) = pydantic.Field(
        description="The number of IO qubits of a custom function"
    )
