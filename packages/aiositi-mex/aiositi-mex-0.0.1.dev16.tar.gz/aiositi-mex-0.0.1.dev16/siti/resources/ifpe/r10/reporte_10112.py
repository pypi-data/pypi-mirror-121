from pydantic import conlist

from ..base import ReportIFPE, Resendable, Sendable, Updateable
from .commons import InformacionFinanciera


class Reporte10121(ReportIFPE, Resendable, Sendable, Updateable):
    _resource = '/IFPE/R10/10121'

    informacion_financiera: conlist(InformacionFinanciera, min_items=1)
