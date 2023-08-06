from typing import Optional

import pydantic
from classiq_interface.generator.custom_function import CustomFunctionData
from qiskit import circuit as qiskit_circuit
from qiskit import qasm as qiskit_qasm


class CustomImplementation(pydantic.BaseModel):

    name: Optional[str] = pydantic.Field(
        default=None,
        description="The name of a custom function implementation",
    )

    # The number of qubits in the QASM code
    num_qubits_in_qasm: Optional[pydantic.conint(ge=1)] = pydantic.Field(
        default=None,
        alias="_num_qubits_in_qasm",
        description="This is a private attribute",
    )

    custom_quantum_circuit_qasm_string: pydantic.constr(min_length=1) = pydantic.Field(
        description="The QASM code of a custom function implementation",
    )

    custom_function_data: CustomFunctionData = pydantic.Field(
        description="The custom function IO parmeters required for validation",
    )

    @staticmethod
    def get_num_qubits_in_qasm(qasm_string: str) -> int:
        try:
            qc = qiskit_circuit.QuantumCircuit.from_qasm_str(qasm_string)
        except qiskit_qasm.exceptions.QasmError:  # The qiskit error is often extremely uninformative
            raise ValueError("The QASM string is not a valid quantum circuit.")
        return qc.num_qubits

    @pydantic.validator("custom_quantum_circuit_qasm_string")
    def validate_custom_quantum_circuit_qasm_string_and_num_qubits_in_qasm(
        cls, custom_quantum_circuit_qasm_string, values
    ):
        num_qubits_in_qasm = values.get("num_qubits_in_qasm")
        if custom_quantum_circuit_qasm_string is None and num_qubits_in_qasm is None:
            raise ValueError("Not enough input to define a custom implementation.")
        num_qubits_in_quantum_circuit = cls.get_num_qubits_in_qasm(
            qasm_string=custom_quantum_circuit_qasm_string
        )
        if num_qubits_in_qasm is None:
            values["num_qubits_in_qasm"] = num_qubits_in_quantum_circuit
        elif num_qubits_in_qasm != num_qubits_in_quantum_circuit:
            raise ValueError(
                f"The number of qubits in the quantum circuit of the implementation {values.get('name')} is incompatible with the function."
            )
        return custom_quantum_circuit_qasm_string

    @pydantic.validator("custom_function_data")
    def validate_custom_function_data(
        cls, custom_function_data: CustomFunctionData, values
    ):
        if values.get("num_qubits_in_qasm") != custom_function_data.num_io_qubits:
            raise ValueError(
                f"The number of qubits in the quantum circuit of the implementation {values.get('name')} is incompatible with the function {custom_function_data.name}."
            )
        return custom_function_data
