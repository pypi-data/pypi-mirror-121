import numpy as np
from scipy import signal


def comp_volt_PWM_NUM(
    Tpwmu,
    freq0,
    fmode,
    fswimode,
    fswi,
    qs,
    Vdc1,
    U0,
    rot_dir,
    type_DPWM: int,
    PF_angle=0,
    is_plot: bool = False,
    is_sin=True,
    fswi_max=0,
    freq0_max=0,
    type_carrier=0,
):
    """
    Generalized DPWM using numerical method according to
    'Impact of Modulation Schemes on DC-Link Capacitor of VSI in HEV Applications'
    Tpwmu : vector
        TIME VECTOR
    freq0: float
        fundamental frequency
    fswi: float
        switching frequency
    qs: int
        number of phases
    Vdc1: float
        bus voltage
    U0: float
        Phase Voltage
    rot_dir: int
        rotation direction
    type_DPWM : int
        0: GDPWM
        1: DPWMMIN
        2: DPWMMAX
        3: DPWM0
        4: DPWM1
        5: DPWM2
        6: DPWM3
        7: SVPWM
        8: SPWM
    type_carrier: int
        type of carrier waveform
    PF_angle: float
        power factor angle
    is_plot: bool
        to plot the pwm
    fswi_max: int
        Maximal switching frequency
    freq0_max: int
        maximal fundamental frequency
    fmode: int
        0: Fixed speed
        1: Varaible speed
    fswimode: int
        0: Fixed fswi
        1: Variable fswi
    """

    Npsim = len(Tpwmu)

    if fmode == 0:  # Fixed speed:
        ws = 2 * np.pi * freq0
    elif fmode == 1:  # Variable speed:
        if type_DPWM == 8:
            freq0_array = (freq0_max - freq0) / Tpwmu[-1] * Tpwmu + freq0 * np.ones(
                Npsim
            )
            ws = np.pi * freq0_array
        else:
            print("ERROR:only SPWM supports the varaible fundamental frequency")
    else:
        pass

    if fswimode == 0:  # Fixed fswi:
        if type_DPWM == 8:
            triangle = Vdc1 / 2 * comp_carrier(Tpwmu, fswi, type_carrier)
        else:
            Th = 1 / fswi
    elif fswimode == 1:  # Variable fswi:
        if type_DPWM == 8:
            wswiT = (
                np.pi * (fswi_max - fswi) / Tpwmu[-1] * Tpwmu ** 2
                + 2 * np.pi * fswi * Tpwmu
            )
            triangle = Vdc1 / 2 * signal.sawtooth(wswiT, 0.5)
        else:
            print("ERROR:only SPWM supports the varaible switching frequency")
    else:
        pass

    M_I = 2 * np.sqrt(2) * U0 / Vdc1  # [0,1]

    k = 1  # 2/sqrt(3)#2/sqrt(3) factor to have higher fundamental compared to SPWM
    if rot_dir == -1:

        Phase = [0, -1, 1]
    else:

        Phase = [0, 1, -1]

    if is_sin:
        Vas = k * M_I * (Vdc1 / 2) * np.sin(ws * Tpwmu + Phase[0] * 2 * np.pi / 3)
        Vbs = k * M_I * (Vdc1 / 2) * np.sin(ws * Tpwmu + Phase[1] * 2 * np.pi / 3)
        Vcs = k * M_I * (Vdc1 / 2) * np.sin(ws * Tpwmu + Phase[2] * 2 * np.pi / 3)

    else:
        Vas = k * M_I * (Vdc1 / 2) * np.cos(ws * Tpwmu + Phase[0] * 2 * np.pi / 3)
        Vbs = k * M_I * (Vdc1 / 2) * np.cos(ws * Tpwmu + Phase[1] * 2 * np.pi / 3)
        Vcs = k * M_I * (Vdc1 / 2) * np.cos(ws * Tpwmu + Phase[2] * 2 * np.pi / 3)

    V_min = np.amin(
        np.concatenate((Vas[:, None], Vbs[:, None], Vcs[:, None]), axis=1), axis=1
    )
    V_max = np.amax(
        np.concatenate((Vas[:, None], Vbs[:, None], Vcs[:, None]), axis=1), axis=1
    )

    alpha_rad = 0

    if type_DPWM == 0:  # GDPWM
        if PF_angle >= -np.pi / 6 and PF_angle <= np.pi / 6:
            alpha_rad = PF_angle
        elif PF_angle > np.pi / 6 and PF_angle <= 5 * np.pi / 12:
            alpha_rad = np.pi / 6
        elif PF_angle >= -5 * np.pi / 12 and PF_angle < -np.pi / 6:
            alpha_rad = -np.pi / 6
        elif PF_angle > 5 * np.pi / 12 and PF_angle <= np.pi / 2:
            alpha_rad = np.pi / 3
        elif PF_angle >= -np.pi / 2 and PF_angle < -5 * np.pi / 12:
            alpha_rad = -np.pi / 3

    elif type_DPWM == 3:  # elif type_waveform==63 #DPWM0
        alpha_rad = -30 * np.pi / 180
    elif type_DPWM == 4:  # elif type_waveform==64 #DPWM1
        alpha_rad = 0
    elif type_DPWM == 5:  # elif type_waveform==65 #DPWM2
        alpha_rad = 30 * np.pi / 180

    if is_sin:
        Vas_g = (
            k
            * M_I
            * (Vdc1 / 2)
            * np.sin(ws * Tpwmu + Phase[0] * 2 * np.pi / 3 - alpha_rad)
        )
        Vbs_g = (
            k
            * M_I
            * (Vdc1 / 2)
            * np.sin(ws * Tpwmu + Phase[1] * 2 * np.pi / 3 - alpha_rad)
        )
        Vcs_g = (
            k
            * M_I
            * (Vdc1 / 2)
            * np.sin(ws * Tpwmu + Phase[2] * 2 * np.pi / 3 - alpha_rad)
        )
    else:
        Vas_g = (
            k
            * M_I
            * (Vdc1 / 2)
            * np.cos(ws * Tpwmu + Phase[0] * 2 * np.pi / 3 - alpha_rad)
        )
        Vbs_g = (
            k
            * M_I
            * (Vdc1 / 2)
            * np.cos(ws * Tpwmu + Phase[1] * 2 * np.pi / 3 - alpha_rad)
        )
        Vcs_g = (
            k
            * M_I
            * (Vdc1 / 2)
            * np.cos(ws * Tpwmu + Phase[2] * 2 * np.pi / 3 - alpha_rad)
        )

    V_offset = np.zeros(Npsim)

    min_abc = np.squeeze(
        np.amin(
            np.concatenate((Vas_g[:, None], Vbs_g[:, None], Vcs_g[:, None]), axis=1),
            axis=1,
        )
    )
    max_abc = np.squeeze(
        np.amax(
            np.concatenate((Vas_g[:, None], Vbs_g[:, None], Vcs_g[:, None]), axis=1),
            axis=1,
        )
    )
    i1 = min_abc + max_abc > 0
    i2 = min_abc + max_abc < 0
    V_offset[i1] = Vdc1 / 2 - V_max[i1]
    V_offset[i2] = -Vdc1 / 2 - V_min[i2]

    # type_DPWM {0, 1, 2, 3, 4, 5, 6, 7} # {GDPWM, DPWMMIN, DPWMMAX, DPWM0, DPWM1, DPWM2, DPWM3, SVPWM)
    if type_DPWM == 1:  # type_waveform==61 #DPWMMIN
        V_offset = -V_min - Vdc1 / 2
    elif type_DPWM == 2:  # elif type_waveform==62 #DPWMMAX
        V_offset = -V_max + Vdc1 / 2
    elif type_DPWM == 6:  # elif type_waveform==66 #DPWM3
        min_abc = np.amin(
            np.concatenate((Vas[:, None], Vbs[:, None], Vcs[:, None]), axis=1), axis=1
        )
        max_abc = np.amax(
            np.concatenate((Vas[:, None], Vbs[:, None], Vcs[:, None]), axis=1), axis=1
        )
        i1 = min_abc + max_abc < 0
        i2 = min_abc + max_abc > 0
        V_offset[i1] = Vdc1 / 2 - V_max[i1]
        V_offset[i2] = -Vdc1 / 2 - V_min[i2]
    elif type_DPWM == 7:  # elif type_waveform==67 #SVPWM
        V_offset = -1 / 2 * (V_max + V_min)
    elif type_DPWM == 8:
        V_offset = 0 * (V_max + V_min)

    Van = Vas + V_offset
    Vbn = Vbs + V_offset
    Vcn = Vcs + V_offset

    if type_DPWM == 8:
        v_pwm = np.ones((qs, Npsim))

        v_pwm[0] = np.where(Vas < triangle, -1, 1)
        v_pwm[1] = np.where(Vbs < triangle, -1, 1)
        v_pwm[2] = np.where(Vcs < triangle, -1, 1)

    else:

        T1 = Th / 4 - Th / (2 * Vdc1) * Van
        T2 = Th / 4 - Th / (2 * Vdc1) * Vbn
        T3 = Th / 4 - Th / (2 * Vdc1) * Vcn
        n = np.floor(Tpwmu / Th).astype(int)
        v_pwm = Vdc1 / 2 * np.ones((qs, Npsim))
        v_pwm[0, Tpwmu < (T1 + n * Th)] = -Vdc1 / 2
        v_pwm[0, Tpwmu > ((n + 1) * Th - T1)] = -Vdc1 / 2
        v_pwm[1, Tpwmu < (T2 + n * Th)] = -Vdc1 / 2
        v_pwm[1, Tpwmu > ((n + 1) * Th - T2)] = -Vdc1 / 2
        v_pwm[2, Tpwmu < (T3 + n * Th)] = -Vdc1 / 2
        v_pwm[2, Tpwmu > ((n + 1) * Th - T3)] = -Vdc1 / 2

    if is_plot:
        fig, axs = plt.subplots(2)
        axs[0].plot(v_pwm[0])
        axs[0].plot(Tpwmu, v_pwm[1])
        axs[0].plot(Tpwmu, v_pwm[2])
        axs[1].plot(Tpwmu, Van)
        axs[1].plot(Tpwmu, V_offset)
        axs[1].plot(Tpwmu, Vas)

        fig.show()
        plt.show()

        if type_DPWM == 8:
            fig, axs = plt.subplots(3)
            axs[0].plot(Tpwmu, Vas, "red", label="Sine wave")
            axs[0].plot(Tpwmu, triangle, "green", label="Carrier wave")
            axs[1].plot(Tpwmu, v_pwm[0], "blue", label="Square wave")
            axs[2].plot(Tpwmu, ws, "blue", label="Square wave")

            axs[0].set_title("SPWM generation")
            axs[0].set_ylabel("Frequency [Hz]")
            axs[0].legend()
            axs[1].set_xlabel("Time [s]")
            axs[1].set_ylabel("Frequency [Hz]")
            axs[1].legend()

            fig.show()
            plt.show()

    return v_pwm, Vas, M_I


def comp_carrier(time, fswi, type_carrier):
    """Function to compute the carrier

    Parameters
    ----------
    time : array
        Time vector
    fswi : array
        Switching frequency
    type_carrier : int
            1: forward toothsaw carrier
        2: backwards toothsaw carrier
        3: toothsaw carrier
        else: symetrical toothsaw carrier

    Returns
    -------
    Y: ndarray
        carrier

    """
    T = 1 / fswi
    time = time % T

    if type_carrier == 1:  # forward toothsaw carrier
        Y = (
            20
            * (
                np.where(time <= 0.5 * T, time, 0) * time
                + np.where(time > 0.5 * T, time, 0) * (time - T)
            )
            / (0.5 * T)
        )
    elif type_carrier == 2:  # backwards toothsaw carrier
        Y = (
            20
            * -(
                np.where(time <= 0.5 * T, time, 0) * time
                + np.where(time > 0.5 * T, time, 0) * (time - T)
            )
            / (0.5 * T)
        )
    elif type_carrier == 3:  # toothsaw carrier
        t1 = (1 + type_carrier) * T / 4
        t2 = T - t1
        Y = (
            np.where(time <= t1, 1, 0) * time / t1
            + np.where(time > t1, 1, 0)
            * np.where(time < t2, 1, 0)
            * (-time + 0.5 * T)
            / (-t1 + 0.5 * T)
            + np.where(time >= t2, 1, 0) * (time - T) / (T - t2)
        )

    else:
        wswiT = 2 * np.pi * time * fswi
        Y = signal.sawtooth(wswiT, 0.5)

    return Y
