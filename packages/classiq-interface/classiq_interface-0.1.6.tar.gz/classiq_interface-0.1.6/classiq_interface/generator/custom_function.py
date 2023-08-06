from enum import Enum
from typing import Type, List

import pydantic
from classiq_interface.generator.custom_function_data import CustomFunctionData
from classiq_interface.generator.custom_implementation import CustomImplementation
from classiq_interface.generator.function_params import FunctionParams


class CustomFunctionInputs(Enum):
    CUSTOM_FUNCTION_INPUT = "CUSTOM_FUNCTION_INPUT"


class CustomFunctionOutputs(Enum):
    CUSTOM_FUNCTION_OUTPUT = "CUSTOM_FUNCTION_OUTPUT"


class CustomFunction(FunctionParams):
    """
    Facilitates the creation of a user-defined custom function
    """

    custom_function_data: CustomFunctionData = pydantic.Field(
        description="This is a private attribute",
    )

    custom_implementations: List[CustomImplementation] = pydantic.Field(
        default=[],
        description="The implementations of a custom function",
    )

    authorize_synthesis_with_stub: bool = pydantic.Field(
        default=False,
        description="Authorize automatic generation of identity gates for stub functions",
    )

    _input_names: Type[Enum] = pydantic.PrivateAttr(default=CustomFunctionInputs)
    _output_names: Type[Enum] = pydantic.PrivateAttr(default=CustomFunctionOutputs)

    def add_implementation_to_custom_function(
        self,
        custom_quantum_circuit_qasm_string: str,
        implementation_name: str = None,
    ) -> CustomImplementation:
        """Adds an implementation to the custom function.

        Args:
            custom_quantum_circuit_qasm_string (str): A QASM code of the implementation.
            implementation_name (:obj:`str`, optional): The name of the implementation.

        Returns:
            The custom function parameters.
        """

        custom_implementation = CustomImplementation(
            name=implementation_name,
            custom_quantum_circuit_qasm_string=custom_quantum_circuit_qasm_string,
            custom_function_data=self.custom_function_data,
        )
        self.custom_implementations.append(custom_implementation)
        return custom_implementation

    @property
    def name(self):
        """The name of a custom function"""
        return self.custom_function_data.name

    @property
    def num_io_qubits(self):
        """The number of IO qubits of a custom function"""
        return self.custom_function_data.num_io_qubits

    @property
    def is_stub(self) -> bool:
        return not len(self.custom_implementations) > 0
