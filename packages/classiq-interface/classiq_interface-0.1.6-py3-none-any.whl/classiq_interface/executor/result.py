import enum
from typing import Union, Optional, Dict

import pydantic


class ExecutionStatus(str, enum.Enum):
    SUCCESS = "success"
    ERROR = "error"


class VaRResult(pydantic.BaseModel):
    var: float = None
    alpha: float = None


class FinanceSimulationResults(pydantic.BaseModel):
    var_results: Optional[VaRResult] = None
    result: Optional[float] = None


class GroverSimulationResults(pydantic.BaseModel):
    result: Dict[str, Union[float, int]]


class ExecutionDetails(pydantic.BaseModel):
    vendor_format_result: Dict = pydantic.Field(
        ..., description="Result in proprietary vendor format"
    )


class ExecutionResult(pydantic.BaseModel):
    status: ExecutionStatus
    details: Union[
        ExecutionDetails, FinanceSimulationResults, GroverSimulationResults, str
    ]
