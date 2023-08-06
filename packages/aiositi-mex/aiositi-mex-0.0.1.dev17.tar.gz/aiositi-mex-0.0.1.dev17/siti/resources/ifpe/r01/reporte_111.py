from pydantic import Field, conlist

from ...base import REGEX_NUMERIC, Resource
from ..base import ReportIFPE, Resendable, Sendable, Updateable


class InformacionFinanciera(Resource):
    concepto: str = Field(
        ..., min_length=12, max_length=12, regex=REGEX_NUMERIC
    )
    moneda: str = Field(..., max_length=2, regex=REGEX_NUMERIC)
    dato: float


class Reporte111(ReportIFPE, Sendable, Updateable, Resendable):
    _resource = '/IFPE/R01/111'

    informacion_financiera: conlist(  # type: ignore[valid-type]
        InformacionFinanciera, min_items=1
    )
