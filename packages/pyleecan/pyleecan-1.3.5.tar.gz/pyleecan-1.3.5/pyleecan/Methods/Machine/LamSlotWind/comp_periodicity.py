# -*- coding: utf-8 -*-
from ....Classes.Winding import Winding
from ....Classes.Conductor import Conductor


def comp_periodicity(self, p=None):
    """Compute the periodicity factor of the lamination

    Parameters
    ----------
    self : LamSlotWind
        A LamSlotWind object

    Returns
    -------
    per_a : int
        Number of spatial periodicities of the lamination
    is_antiper_a : bool
        True if an spatial anti-periodicity is possible after the periodicities
    per_t : int
        Number of time periodicities of the lamination
    is_antiper_t : bool
        True if an time anti-periodicity is possible after the periodicities
    """

    if self.winding is not None and self.winding.conductor is not None:
        sym_a, is_antisym_a = self.winding.get_periodicity()
    else:
        sym_a, is_antisym_a = 1, False

    if is_antisym_a:
        sym_a /= 2

    return int(sym_a), bool(is_antisym_a), int(sym_a), bool(is_antisym_a)
