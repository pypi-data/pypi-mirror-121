from pydantic import conlist

from ..base import ReportIFPE, Resendable, Sendable, Updateable
from .commons import InformacionFinancieraBase


class Reporte13211(ReportIFPE, Resendable, Sendable, Updateable):
    _resource = '/IFPE/R13/13211'

    informacion_financiera: conlist(InformacionFinancieraBase, min_items=1)
