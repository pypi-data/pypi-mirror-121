# -*- coding: utf-8 -*-


def comp_periodicity(self, p=None):
    """Compute the periodicity factor of the lamination

    Parameters
    ----------
    self : LamSlotMulti
        A LamSlotMulti object

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

    if self.sym_dict_enforced is not None:
        self.get_logger().debug("Enforcing symmetry for LamSlotMulti")
        return (
            self.sym_dict_enforced["per_a"],
            self.sym_dict_enforced["is_antiper_a"],
            self.sym_dict_enforced["per_t"],
            self.sym_dict_enforced["is_antiper_t"],
        )
    else:
        Zs = self.get_Zs()
        is_aper = False
        # TODO compute it
        self.get_logger().debug("Symmetry not available yet for LamSlotMulti")
        return 1, is_aper, 1, is_aper
