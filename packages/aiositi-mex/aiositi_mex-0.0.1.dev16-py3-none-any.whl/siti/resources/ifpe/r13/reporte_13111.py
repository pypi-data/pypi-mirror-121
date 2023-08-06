from pydantic import conlist

from ..base import ReportIFPE, Resendable, Sendable, Updateable
from .commons import InformacionFinanciera


class Reporte13111(ReportIFPE, Resendable, Sendable, Updateable):
    _resource = '/IFPE/R13/13111'

    informacion_financiera: conlist(InformacionFinanciera, min_items=1)
