"""Custom function library module, implementing facilities for adding user defined functions to the Classiq platform."""

from typing import Tuple, Dict

from classiq_interface.generator.custom_function import CustomFunction
from classiq_interface.generator.custom_function_data import CustomFunctionData
from classiq_interface.generator.custom_implementation import CustomImplementation


class CustomFunctionLibrary:
    """Facility to manage user-defined custom functions."""

    def __init__(self, name: str = None):
        self._custom_functions_dict: Dict[CustomFunction] = dict()
        self._name: str = name

    def get_custom_function(self, function_name: str):
        """Gets a function from the function library.

        Args:
            function_name (str): The name of the custom function.
        """
        if function_name not in self._custom_functions_dict:
            raise ValueError("Cannot fetch non-existing custom functions.")
        return self._custom_functions_dict[function_name]

    def add_custom_function_to_library(
        self,
        function_name: str,
        num_io_qubits: int = None,
        custom_quantum_circuit_qasm_string: str = None,
        implementation_name: str = None,
        override_existing_custom_functions: bool = False,
        authorize_synthesis_with_stub: bool = False,
    ) -> CustomFunction:
        """Adds a function to the function library.

        Args:
            function_name (str): The name of the custom function.
            num_io_qubits (:obj:`int`, optional): The number of IO qubits of the custom function.
            custom_quantum_circuit_qasm_string (:obj:`str`, optional): A QASM code of the custom function.
            implementation_name (:obj:`str`, optional): The name of the implementation.
            override_existing_custom_functions (:obj:`bool`, optional): Defaults to False.
            authorize_synthesis_with_stub (:obj:`bool`, optional): Defaults to False.

        Returns:
            The custom function parameters.
        """
        if (
            not override_existing_custom_functions
            and function_name in self._custom_functions_dict
        ):
            raise ValueError("Cannot override existing custom functions.")

        if num_io_qubits is None:
            num_io_qubits = CustomImplementation.get_num_qubits_in_qasm(
                qasm_string=custom_quantum_circuit_qasm_string
            )

        custom_function = CustomFunction(
            custom_function_data=CustomFunctionData(
                name=function_name,
                num_io_qubits=num_io_qubits,
            ),
            authorize_synthesis_with_stub=authorize_synthesis_with_stub,
        )
        if custom_quantum_circuit_qasm_string is not None:
            custom_function.add_implementation_to_custom_function(
                custom_quantum_circuit_qasm_string=custom_quantum_circuit_qasm_string,
                implementation_name=implementation_name,
            )
        elif implementation_name is not None:
            raise ValueError(
                "An explicit implementation name requires an explicit QASM string."
            )

        self._custom_functions_dict[custom_function.name] = custom_function
        return custom_function

    def remove_custom_function_from_library(self, function_name: str) -> None:
        """Removes a function from the function library.

        Args:
            function_name (str): The name of the custom function.
        """
        if function_name in self._custom_functions_dict:
            del self._custom_functions_dict[function_name]
        else:
            raise ValueError("Cannot remove non-exisiting custom functions.")

    @property
    def name(self) -> str:
        """Get the library name.

        Returns:
            The library name.
        """
        return self._name

    @property
    def custom_function_names(self) -> Tuple[str]:
        """Get a tuple of the names of the custom functions in the library.

        Returns:
            The names of the custom functions in the library.
        """
        return tuple(self._custom_functions_dict.keys())
