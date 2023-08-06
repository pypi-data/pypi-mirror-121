from pydantic import conlist

from ..base import ReportIFPE, Resendable, Sendable, Updateable
from .commons import InformacionFinanciera


class Reporte13221(ReportIFPE, Resendable, Sendable, Updateable):
    _resource = '/IFPE/R13/13221'

    informacion_financiera: conlist(InformacionFinanciera, min_items=1)
