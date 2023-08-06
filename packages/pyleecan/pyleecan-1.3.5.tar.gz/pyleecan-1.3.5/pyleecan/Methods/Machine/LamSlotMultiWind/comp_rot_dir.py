from numpy import sign


def comp_rot_dir(self):
    """Compute the rotation direction of the fundamental magnetic field induced by the winding
    WARNING: rot_dir = -1 to have positive rotor rotating direction, i.e. rotor position moves towards positive angle

    Parameters
    ----------
    self : LamSlotMultiWind
        A LamSlotMultiWind object

    Returns
    -------
    rot_dir : int
        -1 or +1
    """
    p = self.get_pole_pair_number()

    # Compute unit mmf
    MMF, _ = self.comp_mmf_unit(
        Nt=20 * p, Na=20 * p
    )  # 20 points per pole over time and space is enough to capture rotating direction of fundamental mmf

    # Extract fundamental from unit mmf
    result_p = MMF.get_harmonics(1, "freqs", "wavenumber=" + str(p))
    result_n = MMF.get_harmonics(1, "freqs", "wavenumber=" + str(-p))

    if result_p["Magnitude"][0] > result_n["Magnitude"][0]:
        result = result_p
    else:
        result = result_n

    # Get frequency and wavenumber of fundamental
    f = result["freqs"][0]
    r = result["wavenumber"][0]

    # Rotating direction is the sign of the mechanical speed of the magnetic field fundamental, i.e frequency over wavenumber
    rot_dir = int(sign(f / r))

    return rot_dir
