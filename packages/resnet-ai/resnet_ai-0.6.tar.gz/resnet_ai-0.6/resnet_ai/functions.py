import math


def Pii():
    Pii = math.pi

    return Pii


def Log10(x):
    """ Returns log base 10 of x """

    Log10 = math.log(x, 10)

    return Log10


def LnX(x):
    """ Returns natural log of x """

    LnX = math.log(x)

    return LnX


def rrTc_R(GasGravity, CO2_Percent, H2S_Percent):
    """
    Pseudo Critical Temperature for Miscellaneous Gases
    Reference: McCain, Jr., W.D.: The Properties of Petroleum Fluids, Second
    Pseudo critical temperature - Pg 512, Eq. B-16
    Correction factor, Epsilon - Pg 512, Eq. B-17
    Correction factor, Application - Pg 112, Eq. 3-44
    Units in degrees Rankine

    """

    YCO2 = CO2_Percent / 100
    YH2S = H2S_Percent / 100

    a = YCO2 + YH2S
    b = YH2S

    Epsilon = 120 * (a ** 0.9 - a ** 1.6) + 15 * (b ** 0.5 - b ** 4)

    pTc = 169.2 + 349.5 * GasGravity - GasGravity ** 2
    rrTc_R = pTc - Epsilon

    return rrTc_R


def rrPc_psi(GasGravity, CO2_Percent, H2S_Percent):
    """
        Pseudo Critical Temperature for Miscellaneous Gases
        Reference: McCain, Jr., W.D.: The Properties of Petroleum Fluids, Second
        Pseudo critical temperature - Pg 512, Eq. B-16
        Correction factor, Epsilon - Pg 512, Eq. B-17
        Correction factor, Application - Pg 112, Eq. 3-44
        Units in degrees Rankine

    """

    SG = GasGravity
    YCO2 = CO2_Percent / 100
    YH2S = H2S_Percent / 100
    a = YCO2 + YH2S
    B = YH2S
    Epsilon = 120 * (a ** 0.9 - a ** 1.6) + 15 * (B ** 0.5 - B ** 4)

    pTca = 169.2 + 349.5 * SG - 74 * SG ** 2
    pTc = pTca - Epsilon

    pPca = 756.8 - 131 * SG - 3.6 * SG ** 2
    rrPc_psi = (pPca * pTc) / (pTca + YH2S * (1 - YH2S) * Epsilon)

    return rrPc_psi


def rrZFactor(Pressure_psia, Temperature_F, GasGravity,
              CO2_Percent, H2S_Percent):
    """Source: Deliverability Testing of Natural Gas Wells - State of Texas, prepared for Texas RRC
    James W. Jennings, Bobby D. Poe, jr., David K. Gold, Richard J. Ryan and Ronald D. Oden,
    Appendix E, pgs. 241-242.
    Reference: McCain, Jr., W.D.: The Properties of Petroleum Fluids, Second Edition
    Pg 510, Eq. B-10 and B-11
    Pressure_psia - evaluated pressure
    Temperature_F - evaluated temperature
    """

    A1 = 0.3265
    A2 = -1.07
    A3 = -0.5339
    A4 = 0.01569
    A5 = -0.05165
    A6 = 0.5475
    A7 = -0.7361
    A8 = 0.1844
    A9 = 0.1056
    A10 = 0.6134
    A11 = 0.721
    MaxIter = 100

    rrZFactor = 0

    bLowRange = False
    bOutOfRange = False
    bIterOut = False
    CO2 = CO2_Percent / 100
    H2S = H2S_Percent / 100
    t = Temperature_F + 459.67
    P = Pressure_psia

    fTpr = t / rrTc_R(GasGravity, CO2_Percent, H2S_Percent)
    fPpr = P / rrPc_psi(GasGravity, CO2_Percent, H2S_Percent)
    fDR = 0
    fPRS = 0

    C0 = A7 + A8 / fTpr
    C1 = A1 * fTpr + A2 + A3 / (fTpr ** 2) + A4 / (fTpr ** 3) + A5 / (fTpr ** 4)
    C2 = A6 * fTpr + C0
    C3 = -A9 * C0
    C4 = A10 / (fTpr ** 2)

    if (CO2 + H2S) < 0 or (CO2 + H2S) > 0.85:
        if bOutOfRange:  # Error Found
            rrZFactor = -1000
        if bIterOut:
            rrZFactor = -1001
    elif fPpr >= 0.2 and fPpr < 30 and fTpr > 1 and fTpr <= 3:
        i = 1
        for i in range(MaxIter):  # Calculate_Zfactor loop
            fDR0 = fDR
            C5 = A11 * (fDR ** 2)
            fP = (fTpr + C1 * fDR + C2 * (fDR ** 2) + C3 * (fDR ** 5)) * fDR + C4 * (fDR ** 3) * (1 + C5) * math.exp(
                -C5)
            fDP = fTpr + 2 * C1 * fDR + 3 * C2 * (fDR ** 2) + 6 * C3 * (
                    fDR ** 5) + 3 * C4 * (fDR ** 2) * math.exp(-C5) * (1 + C5 - 2 * (C5 ** 2) / 3)
            fDR = fDR0 - (fP - 0.27 * fPpr) / fDP

            if fDR <= 0:
                fDR = 0.5 * fDR0
            if fDR >= 2.2:
                fDR = fDR0 + 0.9 * (2.2 - fDR0)
            if abs(fDR - fDR0) < 0.0000001:
                break
        if i >= MaxIter:
            bIterOut = True
            if bOutOfRange:  # ErrorFound
                rrZFactor = -1000
            if bIterOut:
                rrZFactor = -1001

        rrZFactor = 0.27 * fPpr / (fDR * fTpr)

        if bLowRange:
            fPpr = fPRS
            rrZFactor = 1 + 5 * fPpr * (rrZFactor - 1)
    elif fPpr > 0 and fPpr < 1 and fTpr > 0.7 and fTpr <= 1:
        i = 1
        for i in range(MaxIter):  # Calculate_Zfactor loop
            fDR0 = fDR
            C5 = A11 * (fDR ** 2)
            fP = (fTpr + C1 * fDR + C2 * (fDR ** 2) + C3 * (fDR ** 5)) * fDR + C4 * (fDR ** 3) * (1 + C5) * math.exp(
                -C5)
            fDP = fTpr + 2 * C1 * fDR + 3 * C2 * (fDR ** 2) + 6 * C3 * (
                    fDR ** 5) + 3 * C4 * (fDR ** 2) * math.exp(-C5) * (1 + C5 - 2 * (C5 ** 2) / 3)
            fDR = fDR0 - (fP - 0.27 * fPpr) / fDP

            if fDR <= 0:
                fDR = 0.5 * fDR0
            if fDR >= 2.2:
                fDR = fDR0 + 0.9 * (2.2 - fDR0)
            if abs(fDR - fDR0) < 0.0000001:
                break
        if i >= MaxIter:
            bIterOut = True
            if bOutOfRange:  # ErrorFound
                rrZFactor = -1000
            if bIterOut:
                rrZFactor = -1001
        rrZFactor = 0.27 * fPpr / (fDR * fTpr)

        if bLowRange:
            fPpr = fPRS
            rrZFactor = 1 + 5 * fPpr * (rrZFactor - 1)
    elif fPpr > 0 and fPpr < 0.2 and fTpr > 1 and fTpr <= 3:
        bLowRange = True
        fPRS = fPpr
        fPpr = 0.2
        i = 1
        for i in range(MaxIter):  # Calculate_Zfactor loop
            fDR0 = fDR
            C5 = A11 * (fDR ** 2)
            fP = (fTpr + C1 * fDR + C2 * (fDR ** 2) + C3 * (fDR ** 5)) * fDR + C4 * (fDR ** 3) * (1 + C5) * math.exp(
                -C5)
            fDP = fTpr + 2 * C1 * fDR + 3 * C2 * (fDR ** 2) + 6 * C3 * (
                    fDR ** 5) + 3 * C4 * (fDR ** 2) * math.exp(-C5) * (1 + C5 - 2 * (C5 ** 2) / 3)
            fDR = fDR0 - (fP - 0.27 * fPpr) / fDP

            if fDR <= 0:
                fDR = 0.5 * fDR0
            if fDR >= 2.2:
                fDR = fDR0 + 0.9 * (2.2 - fDR0)
            if abs(fDR - fDR0) < 0.0000001:
                break
        if i >= MaxIter:
            bIterOut = True
            if bOutOfRange:  # ErrorFound
                rrZFactor = -1000
            if bIterOut:
                rrZFactor = -1001
        rrZFactor = 0.27 * fPpr / (fDR * fTpr)

        if bLowRange:
            fPpr = fPRS
            rrZFactor = 1 + 5 * fPpr * (rrZFactor - 1)
    else:
        bOutOfRange = True
        if bOutOfRange:  # ErrorFound
            rrZFactor = -1000
        if bIterOut:
            rrZFactor = -1001
    return rrZFactor


def rrGasViscosity_cp(Pressure_psia, Temperature_F, GasGravity, Z):
    """ Gas Viscosity for Miscellaneous Gases from McCain
    Reference: McCain, Jr., W.D.: The Properties of Petroleum Fluids, Second Edition
    Page 514, Eq. B-26 to B-29 """

    P = Pressure_psia  # Pressure that viscosity is evaluated at, psia
    t = Temperature_F + 459.67  # Temperature that viscosity is evaluated at, degrees F
    SG = GasGravity

    MW = 28.97 * SG

    a = (9.379 + 0.01607 * MW) * t ** 1.5 / (209.2 + 19.26 * MW + t)
    B = 3.448 + 986.4 / t + 0.01009 * MW
    c = 2.447 - 0.2224 * B

    Rho = P * MW / Z / 669.8 / t

    rrGasViscosity_cp = (a * math.exp(B * Rho ** c)) / 10000

    return rrGasViscosity_cp


def rrReynolds(FluidType, FlowRate, FluidGravity, Diameter_inches, Viscosity_cp):
    """
    Calculates the Reynold's Number to determine whether fluid flow is laminar or turbulent
    Laminar Flow: NRe <= 2100
    Turbulent Flow: NRe > 2100
    Gas = 0, Liquid = 1
    Gas Units: mscf/day
    Liquid Units: bbl/day
    """

    Q = FlowRate
    SG = FluidGravity
    d = Diameter_inches
    Visc = Viscosity_cp

    if FluidType == 0:
        rrReynolds = 20.09 * Q * SG / (d * Visc)
    elif FluidType == 1:
        rrReynolds = 92.3224 * Q * SG / (d * Visc)
    else:
        rrReynolds = 2100

    # Default to laminar flow

    return rrReynolds


def rrFanning(NRe, Epsilon):
    rrFanning = 0
    if NRe <= 2100:
        rrFanning = 16 / NRe
    elif NRe > 2100:
        Ff_Sqr = -4 * Log10(
            Epsilon / 3.7065 - (5.0452 / NRe) * Log10((Epsilon ** 1.1098) / 2.8257 + (7.149 / NRe) ** 0.8981))
        rrFanning = Ff_Sqr ** (-2)

    return rrFanning


def rrDP_Friction_psia(FlowRate, FlowLength_ft, Diameter_inches, FluidGravity, FrictionFactor, Fluid, Pressure_psia,
                       Temperature_F, Z):
    """
    Gas = 0, Liquid = 1
    'Gas Units: mscf/day
    'Liquid Units: bbl/day
    """
    SG = FluidGravity
    Q = FlowRate
    L = FlowLength_ft
    Ff = FrictionFactor
    t = Temperature_F + 459.67
    P = Pressure_psia
    Rho = 0

    d = Diameter_inches / 12

    Area = Pii() * d ** 2 * 0.25

    if Fluid == 0:
        Q = FlowRate * 1000 / 86400
        Rho = P * 28.97 * SG / (Z * 10.37 * t)
        Rho = Rho * (14.7 / P) * (t / 520) * Z
    elif Fluid == 1:
        Q = FlowRate * 5.615 / 86400
        Rho = SG * 62.38

    Vel = (Q / Area)

    rrDP_Friction_psia = 2 * Ff * Rho * Vel ** 2 * L / (32.174 * d * 144)

    return rrDP_Friction_psia


def rrCg(Pressure_psia, Temperature_F, GasGravity, CO2_Percent, H2S_Percent):
    # Gas Compressibility for Miscellaneous Gases from McCain
    P = Pressure_psia
    t = Temperature_F + 459.67
    SG = GasGravity
    TR = t / rrTc_R(SG, CO2_Percent, H2S_Percent)
    PR = P / rrPc_psi(SG, CO2_Percent, H2S_Percent)
    a = 0.064225133
    B = 0.53530771 * TR - 0.61232032
    c = 0.31506237 * TR - 1.0467099 - 0.57832729 / TR ** 2
    d = TR
    e = 0.68157001 / TR ** 2
    f = 0.68446549
    g = 0.27 * PR
    Rho = 0.27 * PR / TR
    # Initial guess
    RhoOld = Rho
    i = 1
    for i in range(1000):
        i += 1
        FRho = a * Rho ** 6 + B * Rho ** 3 + c * Rho ** 2 + d * Rho + e * Rho ** 3 * (1 + f * Rho ** 2) * math.exp(
            -f * Rho ** 2) - g
        DFRho = 6 * a * Rho ** 5 + 3 * B * Rho ** 2 + 2 * c * Rho + d + e * Rho ** 2 * (
                    3 + f * Rho ** 2 * (3 - 2 * f * Rho ** 2)) * math.exp(-f * Rho ** 2)
        Rho = Rho - FRho / DFRho
        Test = abs((Rho - RhoOld) / Rho)
        if Test < 0.00001:
            break
        RhoOld = Rho

    ZM = 0.27 * PR / Rho / TR
    DER = 1 / Rho / TR * (5 * a * Rho ** 5 + 2 * B * Rho ** 2 + c * Rho + 2 * e * Rho ** 2 * (
                1 + f * Rho ** 2 - f ** 2 * Rho ** 4) * math.exp(-f * Rho ** 2))
    CR = 1 / PR / (1 + Rho / ZM * DER)

    rrCg = CR / rrPc_psi(SG, CO2_Percent, H2S_Percent)

    return rrCg


def rrCt(Pressure_psia, Temperature_F, GasGravity, WatSat_percent, CO2_Percent, H2S_Percent):
    # Total Compressibility: Accounts for water saturation, but not water or formation compressibility, which should be added to the output

    Sw = WatSat_percent / 100  # Water saturation
    Cg = rrCg(Pressure_psia, Temperature_F, GasGravity, CO2_Percent, H2S_Percent)
    rrCt = Cg * (1 - Sw)

    return rrCt


def rrBg(Pressure_psia, Temperature_F, GasGravity, CO2_Percent, H2S_Percent):
    """
    Formation volume factor at a specific pressure and temperature using a gas gravity correlation
    Reference: McCain, Jr., W.D.: The Properties of Petroleum Fluids, Second Edition Pg 169, Eq. 6-2
    Psc = Pressure at standard conditions, assumed to be 14.65 psia
    Tsc = Temperature at standard conditions, assumed to be 60 deg F
    Conv = Converts from cubic feet to barrels (5.615 cu ft/bbl)
    Bg is in rcf/scf
    """
    Psc = 14.65
    Tsc = 60

    P = Pressure_psia
    t = Temperature_F
    SG = GasGravity
    Z = rrZFactor(P, t, SG, CO2_Percent, H2S_Percent)
    t = Temperature_F + 459.67

    rrBg = (Z * t * Psc) / (P * (Tsc + 459.67))

    return rrBg


def rrMpp(Pressure_psia, Temperature_F, GasGravity, CO2_Percent, H2S_Percent):
    # Pseudopressure function for Miscellaneous Gas
    P = Pressure_psia  # Pressure that pseudo-pressure is evaluated at, psia
    t = Temperature_F  # Temperature that pseudo-pressure is evaluated at, degrees F
    SG = GasGravity
    rrMpp = 0
    Pold = 0
    Xold = 0
    Pstep = P / 100

    n = 1
    while n <= 100:
        n += 1
        Pnew = Pold + Pstep
        Xnew = 2 * Pnew / (rrZFactor(Pnew, t, SG, CO2_Percent, H2S_Percent) * rrGasViscosity_cp(Pnew, t, SG,
                                                                                                rrZFactor(Pnew, t, SG,
                                                                                                          CO2_Percent,
                                                                                                          H2S_Percent)))
        rrMpp = rrMpp + (Xold + Xnew) / 2 * Pstep
        Pold = Pnew
        Xold = Xnew

    rrMpp = rrMpp  # is this needed in Python?

    return rrMpp


def rrPseudoTime(Time_Days, Pressure_psia, Temperature_F, GasGravity, CO2_Percent, H2S_Percent, InitialPressure_psia,
                 Cm_1Overpsia, Sw_Percent):
    """
    Pseudotime function for Miscellaneous Gas
    Need to change from gas compressibility to total compressibility
    """
    Time = Time_Days
    P = Pressure_psia
    Temp = Temperature_F
    SG = GasGravity
    rrPseudoTime = 0
    Told = 0
    Xold = 0
    Tstep = Time / 100
    P_init = InitialPressure_psia
    Cm = Cm_1Overpsia
    Sw = Sw_Percent

    Visc_init = rrGasViscosity_cp(P_init, Temp, SG, rrZFactor(P_init, Temp, SG, CO2_Percent, H2S_Percent))
    Ct_init = rrCt(P_init, Temp, SG, Sw, CO2_Percent, H2S_Percent) + Cm + 0.00003 * Sw
    P_avg = (P_init + P) / 2

    ViscCt_init = Visc_init * Ct_init

    n = 0
    while (n <= Time):  # Changed from for loop to while loop to use Time variable as input
        n += 1
        Tnew = Told + Tstep
        Visc = rrGasViscosity_cp(P_avg, Temp, SG, rrZFactor(P_avg, Temp, SG, CO2_Percent, H2S_Percent))
        Ct = rrCt(P_avg, Temp, SG, Sw, CO2_Percent, H2S_Percent) + Cm + 0.00003 * Sw
        ViscCt = Visc * Ct
        Xnew = ViscCt_init / (ViscCt)
        rrPseudoTime = rrPseudoTime + (Xold + Xnew) / 2 * Tstep
        Told = Tnew
        Xold = Xnew

    rrPseudoTime = rrPseudoTime

    return rrPseudoTime


def rrPfromMP(PseudoPressure, Temperature_F, GasGravity, CO2_Percent, H2S_Percent):
    """
    Calculation of Pressure fom Gas Psuedopressure for Miscellaneous Gases
    'rrPfromMP = the actual pressure in psia that you want to calculate for a given pseudo -pressure
    """

    MP2 = PseudoPressure  # Pseodo-Pressure that you want real pressure for
    t = Temperature_F  # Temperature that pseudo-pressure is evaluated at, Degrees F
    SG = GasGravity
    NewP = 5000
    OldPhigh = 13000
    OldPlow = 50
    n = 1

    while n <= 50:
        NewMP = rrMpp(NewP, t, SG, CO2_Percent, H2S_Percent)
        ErrorCheck = abs((NewMP - MP2) / NewMP)
        if ErrorCheck < 0.1:
            break
        if NewMP > MP2:
            OldPhigh = NewP
        if NewMP < MP2:
            OldPlow = NewP
        NewP = (OldPlow + OldPhigh) / 2

    rrPfromMP = NewP

    return rrPfromMP


def rrQgChoke_Mmcfd(Pressure_psia, GasGravity, Choke_inches, Temperature_F):
    """
    Calculates absolute open-flow Gas Flow Rate for gas flowing through choke
    Pressure is the upstream pressure before the choke, psia
    Choke is the size of the positive choke, inches
    Temperature is the flowing surface temperature ahead of the choke, degrees F
    Note: Formula to calculate the coefficieint, "Coeff", based on a best-fit linear regression acquired from published choke table data
    Reference: Haliburton Red Book, Pg 120
    Calculated gas rate will be in Mcf/day
    Choke, inches Coef.

    ======Published Choke Coefficients========
    1/8 = 6.25
    3/16 = 14.44
    1/4 = 26.51
    5/16 = 43.64
    3/8 = 61.21
    7/16 = 85.13
    1/2 = 112.72
    5/8 = 179.74
    3/4 = 260.99
    """

    P = Pressure_psia  # Flowing surface pressure upstream of the choke, psia
    SG = GasGravity
    t = Temperature_F + 459.67  # Flowing Surface Temp, degrees R
    Coeff = 478.3 * Choke_inches ** 2.0852  # Best-fit linear regression of the above data

    rrQgChoke_Mcfd = (Coeff * P) / (SG * t) ** 0.5

    return rrQgChoke_Mcfd


def rrBHP_psia(FlowType, GasRate_Mcfd, WGR_stb_mmcf, Pressure_Surf_psia, GasGravity, Temp_Surf_F, Temp_BH_F, TVD_ft,
               FlowLength_ft, \
               ID_Tbg_inches, OD_Tbg_inches, ID_Csg_inches, CO2_Percent, H2S_Percent):
    """
    Calclates Bottomhole Pressure from Surface Pressure using the modified Cullender and Smith method
    Reference: "Deliverability Testing of Natural Gas Wells - State of Texas", TX RRC
    Pg 17-18 and Appendix E, Pg 238-241
    Flow Types:
    0 = Tubing or Casing flow
    1 = Tubing/Casing annular flow
    """

    Qg = GasRate_Mcfd  # Gas Rate in Mcf/day
    Temp_Surf_R = Temp_Surf_F + 459.67
    Temp_BH_R = Temp_BH_F + 459.67
    L = FlowLength_ft
    H = TVD_ft
    d = ID_Tbg_inches
    D1 = OD_Tbg_inches
    D2 = ID_Csg_inches
    SG = GasGravity  # Specific gravity of gas at the wellhead
    WGR = WGR_stb_mmcf / 1000000  # Converts WGR from STB/MMcf to STB/scf
    XIBH = 0
    XIMP = 0


    # Initialize tubing diameter for flow up the tubing
    if FlowType == 0:  # FlowType = 0 for flow up the tubing or casing, = 1 for flow up the tubing/casing annulus
        DPL = d
        DM = d
        DE5 = d ** 5
    # Initialize equivalent flow diameters for flow up the tubing/casing annulus
    else:
        DPL = D2 + D1
        DM = D2 - D1
        DE5 = (DM ** 3) * (DPL ** 2)

    # Evaluate the integral I at wellhead conditions
    Z = rrZFactor(Pressure_Surf_psia, Temp_Surf_F, SG, CO2_Percent, H2S_Percent)

    # Calculate ALPHA
    ALPHA = (SG / 53.34 + WGR * 86.27) * L

    # Calculate OMEGA at wellhead conditions
    ViscG = rrGasViscosity_cp(Pressure_Surf_psia, Temp_Surf_F, SG, Z)
    if Qg == 0:
        OMEGAWH = 0
    else:
        NRe = 20.011 * SG * Qg / (ViscG * DPL)
        RR = 0.0023 / DM
        f = 1 / ((2.28 - 4 * Log10(RR + 21.25 / (NRe ** 0.9)))) ** 2
        OMEGAWH = 0.0026665 * f * Qg ** 2 / DE5

    PTZ = Pressure_Surf_psia / (Temp_Surf_R * Z)
    XIWH = (199.3 * WGR * PTZ ** 2 + PTZ) / (OMEGAWH + (PTZ ** 2) * H / L)

    # Calculate the first estimate of midpoint pressure
    PMP = Pressure_Surf_psia + (ALPHA / (XIWH + XIWH))

    # Evaluate the intergral I at the midpoint conditions
    i = 1
    for i in range(100):
        TMPF = (Temp_Surf_F + Temp_BH_F) / 2
        TMPR = TMPF + 459.67
        Z = rrZFactor(PMP, TMPF, SG, CO2_Percent, H2S_Percent)
        ViscG = rrGasViscosity_cp(PMP, TMPF, SG, Z)
        if Qg == 0:
            OMEGAMP = 0
        else:
            NRe = 20.011 * SG * Qg / (ViscG * DPL)
            RR = 0.0023 / DM
            f = 1 / ((2.28 - 4 * Log10(RR + 21.25 / (NRe ** 0.9)))) ** 2
            OMEGAMP = 0.0026665 * f * Qg ** 2 / DE5

        PTZ = PMP / (TMPR * Z)
        XIMP = (199.3 * WGR * PTZ ** 2 + PTZ) / (OMEGAMP + (PTZ ** 2) * H / L)

        # Recalculate the midpoint pressure until convergence by iteration
        PMPN = ALPHA / (XIMP + XIWH) + Pressure_Surf_psia
        DP = PMP - PMPN
        PMP = PMPN

        if abs(DP) < 0.00001:
            break
    # Calculate a first estimate of bottomhole pressure
    Pwf = PMP + (ALPHA / (XIMP + XIMP))

    # Evaluate the integral I at bottomhole conditions
    j = 1
    for j in range(100):
        Z = rrZFactor(Pwf, Temp_BH_F, GasGravity, CO2_Percent, H2S_Percent)
        ViscG = rrGasViscosity_cp(Pwf, Temp_BH_F, SG, Z)
        if Qg == 0:
            OMEGABH = 0
        else:
            NRe = 20.011 * SG * Qg / (ViscG * DPL)
            RR = 0.0023 / DM
            f = 1 / ((2.28 - 4 * Log10(RR + 21.25 / (NRe ** 0.9)))) ** 2
            OMEGABH = 0.0026665 * f * Qg ** 2 / DE5

        PTZ = Pwf / (Temp_BH_R * Z)
        XIBH = (199.3 * WGR * PTZ ** 2 + PTZ) / (OMEGABH + (PTZ ** 2) * H / L)

        # Recalculate the bottomhole pressure until convergence by iteration
        PBHN = ALPHA / (XIBH + XIMP) + PMP
        DP = Pwf - PBHN
        Pwf = PBHN
        if abs(DP) < 0.00001:
            break

    # Apply Simpsons rule to obtain a more accurate estimate of bottomhole pressure
    Pwf = Pressure_Surf_psia + (6 * ALPHA) / (XIWH + 4 * XIMP + XIBH)

    rrBHP_psia = Pwf

    return rrBHP_psia


def rrFTPfromFBHP_psia(FlowType, GasRate_Mcfd, WGR_stb_mmcf, FBHP_psia, \
                       GasGravity, Temp_Surf_F, Temp_BH_F, TVD_ft, FlowLength_ft, \
                       ID_Tbg_inches, OD_Tbg_inches, ID_Csg_inches, CO2_Percent, H2S_Percent):
    """"
    Calculates surface pressure from bottomhole Pressure
    Essentially, reverses the rrBHPRESS function above
    """

    NewFTP = 5500
    OldFTPhigh = 13000
    OldFTPlow = 50

    for n in range(30):
        NewPwf = rrBHP_psia(FlowType, GasRate_Mcfd, WGR_stb_mmcf, NewFTP, GasGravity, Temp_Surf_F, Temp_BH_F, TVD_ft, \
                            FlowLength_ft, ID_Tbg_inches, OD_Tbg_inches, ID_Csg_inches, CO2_Percent, H2S_Percent)
        ErrorCheck = Abs((NewPwf - FBHP_psia) / NewPwf)
        if ErrorCheck < 0.0001:
            break
        if NewPwf > FBHP_psia:
            OldFTPhigh = NewFTP
        if NewPwf < FBHP_psia:
            OldFTPlow = NewFTP
        NewFTP = (OldFTPlow + OldFTPhigh) / 2

    rrFTPfromFBHP_psia = NewFTP

    return rrFTPfromFBHP_psia


def rrOnePoint_md(ResPress_psia, Temp_Res_F, GasGravity, GasRate_Mcfd, \
                  FlowTime_hrs, FlowingBHP_psia, Pay_feet, Porosity_percent, WatSat_percent, \
                  WellRadius_ft, Skin, CO2_Percent, H2S_Percent):
    """"
    Calculates effective formation permeabililty from a single rate data point obtained from a flow test
    Reference: SPE 012847 "Estimating Formation Permeability From Single-Point Flow Data" 1984 - Lee, Holditch, and McVay
    """
    Knew = 0
    Pi = ResPress_psia  # Initial reservor pressure, psia
    TresR = Temp_Res_F + 459.67  # Reservoir temperature, R
    SG = GasGravity
    Qg = GasRate_Mcfd  # Gas rate, Mcf/d
    TimeHrs = FlowTime_hrs  # Length of flow time, hours
    Pwf = FlowingBHP_psia  # Flowing bottomhole pressure, psia
    Pay = Pay_feet  # Net Pay, feet
    Porosity = Porosity_percent / 100  # Porosity as a fraction
    Sw = WatSat_percent / 100  # Water saturation as a fraction
    Rw = WellRadius_ft  # Wellbore radius, feet
    MPi = rrMpp(Pi, Temp_Res_F, SG, CO2_Percent, H2S_Percent)  # Pseudo-pressure of initial reservoir pressure
    MPwf = rrMpp(Pwf, Temp_Res_F, SG, CO2_Percent, H2S_Percent)
    Z = rrZFactor(Pwf, Temp_Res_F, SG, CO2_Percent, H2S_Percent)  # Pseudo-pressure of flowing bottomhole pressure
    UGi = rrGasViscosity_cp(Pi, Temp_Res_F, SG, Z)  # Viscosity of gas at inital reservoir pressure
    Cti = rrCt(Pi, Temp_Res_F, SG, WatSat_percent, CO2_Percent, \
               H2S_Percent)  # Total compressibiility at initial reservoir pressure

    Kold = 1  # Initial guess for permeability
    for i in range(100):
        Rd = ((Kold * TimeHrs) / (377 * Porosity * UGi * Cti)) ** 0.5
        ONE = 1422 * Qg * TresR
        TWO = Pay * (MPi - MPwf)
        THREE = LnX(Rd / Rw) - 0.75 + Skin
        Knew = (ONE / TWO) * THREE
        Kdiff = Abs((Knew - Kold) / Knew)
        if Kdiff < 0.00001:
            break
        Kold = Knew

    rrOnePoint_md = Knew

    return rrOnePoint_md


def rrRwa_ft(WellRadius_ft, Skin):
    """
    Calculates the radius of the damaged or stimulated zone in feet
    Skin can be either positive (damaged) or negative (stimulated)
    rrRwa is in feet
    """
    Rw = WellRadius_ft  # wellbore radius in feet
    rrRwa_ft = Rw * math.exp(-Skin)  # rwa in feet

    return rrRwa_ft


def rrSkin2Perm_md(ResPerm_md, WellRadius_ft, Skin, DamageDist_ft):
    """"
    Calculates the permeability of the damaged or stimulated zone
    DamageDist_ft: for a positive skin, pick the distance you think the damage
    Extends beyond the wellbore, usually several inches to several feet
    DamageDist_ft: for a negative skin, calculate the stimulated distance using the
    Skin can be either positive (damaged) or negative (stimulated)
    rrSkin2Perm is in md
    """

    Rw = WellRadius_ft  # Wellbore Radius in feet

    if DamageDist_ft < 0.01:  # I arbitrarily limit the Damage Distance from the wellbore to a minimum of 0.01 feet
        Rd = Rw + 0.01
    else:
        Rd = DamageDist_ft + Rw

    if Skin == 0:
        rrSkin2Perm_md = ResPerm_md
    else:
        rrSkin2Perm_md = ResPerm_md / (1 + Skin / LnX(Rd / Rw))

    if rrSkin2Perm_md < 0:
        rrSkin2Perm_md = 9999  # Assume Infinite Conductivity through stimulated zone

    return rrSkin2Perm_md


def rrSkin2Lf_ft(WellRadius_ft, Skin):
    """"
    Calculates the equivalent infinite conductivity fracture half-length for a given skin factor
    Approximately = 2 x rwa
    NOTE: Enter skin as a negative number to represent stimulation
    NOTE: If skin is entered as a 0, then rrSkin2Lf_ft defaults to rw
    NOTE: If skin is entered as a positive number, representing damage, then rrSkin2Lf_ft defaults to "ERROR" indicating there is an error
    """

    Rw = WellRadius_ft  # wellbore radius in feet
    Lf = 2 * Rw * math.exp(-Skin)  # equivalent infinite conductivity fracture half-length for a given skin factor

    rrSkin2Lf_ft = Lf

    if Skin == 0:
        rrSkin2Lf_ft = Rw
    if Skin > 0:
        rrSkin2Lf_ft = "ERROR"

    return rrSkin2Lf_ft


def rrLf2Skin(WellRadius_ft, FracHalfLen_ft):
    """Calculates the equivalent skin factor of an infinite conductivity fracture"""

    Lf = FracHalfLen_ft  # Fracture half-length in feet
    Rw = WellRadius_ft  # Wellbore radius in feet

    if Lf == 0:
        Skin = 0
    else:
        Skin = -LnX(Lf / (2 * Rw))  # Calculated equivalent skin factor of an infinite conductivity fracture

    rrLf2Skin = Skin

    return rrLf2Skin


def rrQgPSS_Mcfd(ResPress_psi, ResTemp_F, GasGravity, FlowBHP_psi, \
                 Perm_md, Pay_feet, Porosity_percent, WatSat_percent, Skin, \
                 DamageRadius_ft, WellRadius_ft, DrainArea_ac, CO2_Percent, H2S_Percent):
    """Pseudosteady-state flow equation for a gas well """

    Pbar = ResPress_psi  # Average reservor pressure, psia
    TresR = ResTemp_F + 459.67  # Reservoir temperature, R
    SG = GasGravity
    Pwf = FlowBHP_psi  # Flowing bottomhole pressure, psia
    Pay = Pay_feet  # Net Pay, feet
    Porosity = Porosity_percent / 100  # Porosity as a fraction
    Sw = WatSat_percent / 100  # Water saturation as a fraction
    Rw = WellRadius_ft  # Wellbore radius, feet
    Mpbar = rrMpp(Pbar, ResTemp_F, SG, \
                  CO2_Percent, H2S_Percent)  # Pseudo-pressure of the average reservoir pressure
    MPwf = rrMpp(Pwf, ResTemp_F, SG, \
                 CO2_Percent, H2S_Percent)
    Z = rrZFactor(Pwf, ResTemp_F, SG, \
                  CO2_Percent, H2S_Percent)  # Pseudo-pressure of flowing bottomhole pressure
    UgPwf = rrGasViscosity_cp(Pwf, ResTemp_F, \
                              SG, Z)  # Viscosity of gas at flowing bottomhole pressure
    Re = (
                     DrainArea_ac * 43560 / Pii()) ** 0.5  # Radius of the reservoir's drainage area assuming a circular area in feet
    Ks = rrSkin2Perm_md(Perm_md, WellRadius_ft, \
                        Skin, DamageRadius_ft)  # Permeability of the damaged zone in md
    Dee = (0.00006 * SG * (Ks ** -0.1) * Pay) / (UgPwf * Rw * Pay ** 2)
    d = (1424 * TresR * Dee) / (Perm_md * Pay)
    c = (1424 * TresR / (Perm_md * Pay)) * (LnX(Re / Rw) - 0.75 + Skin)

    rrQgPSS_Mcfd = (-c + (c ** 2 + 4 * d * (Mpbar - MPwf)) ** 0.5) / (2 * d)

    return rrQgPSS_Mcfd


def rrPwfPSS(QG_Mcfd, ResPress_psi, ResTemp_F, GasGravity, Perm_md, \
             Pay_feet, Porosity_percent, WatSat_percent, Skin, DamageRadius_ft, \
             WellRadius_ft, DrainArea_ac, CO2_Percent, H2S_Percent):
    """
    Calculates Pwf (flowing bottomhole pressure) for a gas well using the PSS flow equation
    """
    NewPwf = 2500
    OldPwfHigh = 13000
    OldPwfLow = 50

    for n in range(50):
        NewQg = rrQgPSS_Mcfd(ResPress_psi, ResTemp_F, GasGravity, NewPwf, Perm_md, Pay_feet, Porosity_percent,
                             WatSat_percent, Skin, DamageRadius_ft, WellRadius_ft, DrainArea_ac, CO2_Percent,
                             H2S_Percent)
        Check = abs((NewQg - QG_Mcfd) / NewQg)

        if Check <= 0.000001:
            break
        if NewQg <= QG_Mcfd:
            OldPwfHigh = NewPwf
        if NewQg >= QG_Mcfd:
            OldPwfLow = NewPwf

        NewPwf = (OldPwfLow + OldPwfHigh) / 2

    rrPwfPSS = NewPwf

    return rrPwfPSS


def rrPbarPSS(QG_Mcfd, FlowBHP_psi, ResTemp_F, GasGravity, Perm_md, \
              Pay_feet, Porosity_percent, WatSat_percent, Skin, DamageRadius_ft, \
              WellRadius_ft, DrainArea_ac, CO2_Percent, H2S_Percent):
    """
    Calculates average reservoir pressure, Pbar, for a gas well using the PSS flow equation
    """

    NewPbar = 5500
    OldPbarhigh = 13000
    OldPbarlow = 50

    for n in range(30):
        NewQg = rrQgPSS_Mcfd(NewPbar, ResTemp_F, GasGravity, FlowBHP_psi, Perm_md, Pay_feet, Porosity_percent,
                             WatSat_percent, Skin, DamageRadius_ft, WellRadius_ft, DrainArea_ac, CO2_Percent,
                             H2S_Percent)
        Check = Abs((NewQg - QG_Mcfd) / NewQg)

        if Check < 0.0001:
            break
        if NewQg > QG_Mcfd:
            OldPbarhigh = NewPbar
        if NewQg < QG_Mcfd:
            OldPbarlow = NewPbar

        NewPbar = (OldPbarlow + OldPbarhigh) / 2

    rrPbarPSS = NewPbar

    return rrPbarPSS


def rrBo(SGg, SGo, Pb, Rsb, Ct, t, Peval):
    """
    Oil formation volume factor correlation estimate
    """

    Ppoi = 52.8 - 0.01 * Rsb
    Ppai = -49.389 + 85.0149 * SGg - 3.70373 * SGg * Ppoi + 0.047982 * SGg * Ppoi ** 2 + 2.98914 * Ppoi - 0.035689 * Ppoi ** 2
    Ppoii = (Rsb * SGg + 4600 * SGo) / (73.71 + Rsb * SGo / Ppai)
    Ppaii = -49.389 + 85.0149 * SGg - 3.70373 * SGg * Ppoii + 0.047982 * SGg * Ppoii ** 2 + 2.98914 * Ppoii - 0.035689 * Ppoii ** 2
    Ppoiii = (Rsb * SGg + 4600 * SGo) / (73.71 + Rsb * SGo / Ppaii)
    RhoBP = Ppoiii + (0.167 + 16.181 * 10 ** (-0.0425 * Ppoiii)) * Pb / 1000 - 0.01 * (
            0.299 + 263 * 10 ** (-0.0603 * Ppoiii)) * (Pb / 1000) ** 2
    RhoT = RhoBP - (0.0032 + 1.505 * RhoBP ** -0.951) * (t - 60) ** -0.938 - (
            0.0216 - 0.0233 * 10 ** (-0.0161 * RhoBP)) * (t - 60) ** 0.475
    RhoRes = RhoT * math.exp(Ct * (Peval - Pb))
    rrBo = (SGo * 62.371 + 0.01357 * Rsb * SGg) / RhoRes

    return rrBo


def rrDCA_Hyp2Exp(TimeUnits, InitialRate_Mscfpd, NominalDecline_PercentPerYear, BFactor, TerminalDecline_PercentPerYear,
                  Time):
    """"
    TimeUnits = 0, refers to time units in days
    TimeUnits = 1, refers to time units in months
    """
    IP = InitialRate_Mscfpd
    NomDec = NominalDecline_PercentPerYear
    TermDec = TerminalDecline_PercentPerYear
    BFac = BFactor
    t = Time

    if TimeUnits == 0:
        conv = 365.25
    else:
        conv = 12

    transition = ((NomDec / conv) / (TermDec / conv) - 1) / (BFac * NomDec / conv)

    if abs(BFac - 1) <= 0.001:
        Q_trans = IP / (1 + NomDec / conv * (transition))
    else:
        Q_trans = IP * (1 + BFac * NomDec / conv * (transition)) ** (-1 / BFac)

    if abs(BFac - 1) <= 0.001:
        Q_hyp = IP / (1 + NomDec / conv * (t))
    else:
        Q_hyp = IP * (1 + BFac * NomDec / conv * (t)) ** (-1 / BFac)

    Q_exp = Q_trans * math.exp(-1 * TermDec / conv * (t - transition))

    if t < transition:
        Qg = Q_hyp
    else:
        Qg = Q_exp

    rrDCA_Hyp2Exp = Qg

    return rrDCA_Hyp2Exp


def rrDCA_Hyp2Exp_FlatTime(TimeUnits, InitialRate_Mscfpd, FlatTime_TimeUnits, NominalDecline_PercentPerYear, \
                           BFactor, TerminalDecline_PercentPerYear, Time):
    """
    TimeUnits = 0, refers to time units in days
    TimeUnits = 1, refers to time units in months
    """

    IP = InitialRate_Mscfpd
    FlatTime = FlatTime_TimeUnits
    NomDec = NominalDecline_PercentPerYear
    TermDec = TerminalDecline_PercentPerYear
    BFac = BFactor
    t = Time

    if TimeUnits == 0:
        conv = 365.25
    else:
        conv = 12

    transition = ((NomDec / conv) / (TermDec / conv) - 1) / (BFac * NomDec / conv)

    if abs(BFac - 1) <= 0.001:
        Q_trans = IP / (1 + NomDec / conv * (transition - FlatTime))
    else:
        Q_trans = IP * (1 + BFac * NomDec / conv * (transition - FlatTime)) ** (-1 / BFac)

    Q_flat = IP

    if abs(BFac - 1) <= 0.001:
        Q_hyp = IP / (1 + NomDec / conv * (t - FlatTime))
    elif t <= FlatTime:
        Q_hyp = Q_flat
    else:
        Q_hyp = IP * (1 + BFac * NomDec / conv * (t - FlatTime)) ** (-1 / BFac)

    Q_exp = Q_trans * math.exp(-1 * TermDec / conv * (t - transition))

    if t <= FlatTime:
        Qg = Q_flat
    elif t < transition:
        Qg = Q_hyp
    else:
        Qg = Q_exp

    rrDCA_Hyp2Exp_FlatTime = Qg

    return rrDCA_Hyp2Exp_FlatTime


def rrDCA_Prod_Hyp2Exp_FlatTime(TimeUnits, InitialRate_Mscfpd, FlatTime_TimeUnits, NominalDecline_PercentPerYear, \
                                BFactor, TerminalDecline_PercentPerYear, Time):
    """"
    TimeUnits = 0, refers to time units in days
    TimeUnits = 1, refers to time units in months
    """

    startTime = 0
    endTime = Time

    prodPrev = 0
    prodNow = prodPrev

    if TimeUnits == 0:
        convTime = 1
    else:
        convTime = 365.25 / 12

    i = startTime
    for i in range(endTime):
        if i == 0:
            prodNow = 0
        else:
            prodNow = rrDCA_Hyp2Exp_FlatTime(TimeUnits, InitialRate_Mscfpd, FlatTime_TimeUnits,
                                             NominalDecline_PercentPerYear,
                                             BFactor, TerminalDecline_PercentPerYear, i)
        prodNow = prodNow * convTime + prodPrev

        prodPrev = prodNow

    rrDCA_Prod_Hyp2Exp_FlatTime = prodNow

    return rrDCA_Prod_Hyp2Exp_FlatTime


def rrDCA_Prod_Hyp2Exp(TimeUnits, InitialRate_Mscfpd, NominalDecline_PercentPerYear, BFactor,
                       TerminalDecline_PercentPerYear, Time):
    """
    TimeUnits = 0, refers to time units in days
    TimeUnits = 1, refers to time units in months
    """

    startTime = 0
    endTime = Time

    prodPrev = 0
    prodNow = prodPrev

    if TimeUnits == 0:
        convTime = 1
    else:
        convTime = 365.25 / 12

    i = startTime
    for i in range(endTime):
        if i == 0:
            prodNow = 0
        else:
            prodNow = rrDCA_Hyp2Exp(TimeUnits, InitialRate_Mscfpd, NominalDecline_PercentPerYear, BFactor,
                                    TerminalDecline_PercentPerYear, i)

        prodNow = prodNow * convTime + prodPrev

        prodPrev = prodNow

    rrDCA_Prod_Hyp2Exp = prodNow

    return rrDCA_Prod_Hyp2Exp


def rr_BHP_GasEstimate(GasRate_Mcfd, Pressure_Surf_psia, GasGravity, Temp_Surf_F, Temp_BH_F, \
                       TVD_ft, TMD_ft, Epsilon, ID_Tbg_inches, OD_Tbg_inches, HoleDia_inches, CO2_Percent, H2S_Percent):
    SG = GasGravity
    P1 = Pressure_Surf_psia
    P2 = P1
    Temp_Grad = (Temp_BH_F - Temp_Surf_F) / (TVD_ft / 100)

    # Number of Segments that Flow Length will be discretized into:
    Segments = 10
    # Length of each segment:
    SegmentLength = TMD_ft / Segments

    i = 1

    for i in range(Segments):
        L = SegmentLength * i
        if i == 1:
            T1 = Temp_Surf_F
        # At the first step, T1 is the temperature at the surface
        else:
            T1 = Temp_Grad * (L - 1) / 100 + Temp_Surf_F
        # Calculate the temp at the top of each segment

        T2 = Temp_Grad * L / 100 + Temp_Surf_F
        # Calculate the temperature at the bottom of the first segment

        Tavg = (T2 + T1) / 2
        Pavg = (P1 + P2) / 2

        # Calculate fluid properties in each segment
        Z = rrZFactor(Pavg, Tavg, SG, CO2_Percent, H2S_Percent)
        Visc_Gas = rrGasViscosity_cp(Pavg, Tavg, SG, Z)

        NRe = rrReynolds(0, GasRate_Mcfd, SG, ID_Tbg_inches, Visc_Gas)
        Ff = rrFanning(NRe, Epsilon)
        s = -0.0375 * SG * math.sin(3.14156 / 2) * SegmentLength / (Z * Tavg)
        P2 = -math.exp(-s) * P1 ** 2 - 0.000667 * Ff * (math.exp(-s) - 1) * (Tavg * Z * GasRate_Mcfd) ** 2 / (
                Sin(3.14156 / 2) * ID_Tbg_inches ** 5)
        P2 = Abs(P2) ** 0.5
        P1 = P2

    rr_BHP_GasEstimate = P2

    return rr_BHP_GasEstimate


def rrPTA_M(FlowRegime, T_hrs, DeltaP_Prime):
    """
    1 = Bilinear
    2 = Linear
    3 = PseudoRadial
    4 = Pseudosteady State
    """
    rrPTA_M = 0
    if FlowRegime == 1:
        rrPTA_M = 4 * DeltaP_Prime / (T_hrs ** (1 / 4))
    elif FlowRegime == 2:
        rrPTA_M = 2 * DeltaP_Prime / (T_hrs ** (1 / 2))
    elif FlowRegime == 3:
        rrPTA_M = DeltaP_Prime * LnX(10)
    elif FlowRegime == 4:
        rrPTA_M = DeltaP_Prime / T_hrs

    return rrPTA_M


def rrPTA_K_fromReal(Q_mscfpd, Bg_rc_scf, M_IARF, H_ft, Visc_cp):
    conv = 5.615
    PreFactor = 162.6

    Q = Q_mscfpd / conv
    B = Bg_rc_scf
    H = H_ft
    u = Visc_cp
    M = M_IARF

    rrPTA_K_fromReal = (PreFactor * Q * B * u) / (M * H)

    return rrPTA_K_fromReal


def rrPTA_XfSqrK_fromReal(Q_mscfpd, Bg_rc_scf, M_lf, H_ft, Visc_cp, Phi, Ct):
    conv = 5.615
    PreFactor = 4.064

    Q = Q_mscfpd / conv
    B = Bg_rc_scf
    H = H_ft
    u = Visc_cp
    M = M_lf

    rrPTA_XfSqrK_fromReal = (PreFactor * Q * B) / (M * H) * (math.sqrt(u / (Phi * Ct)))

    return rrPTA_XfSqrK_fromReal


def rrPTA_FC_fromReal(Q_mscfpd, Bg_rc_scf, M_lf, H_ft, Visc_cp, Phi, Ct):
    conv = 5.615
    PreFactor = 44.1

    Q = Q_mscfpd / conv
    B = Bg_rc_scf
    H = H_ft
    u = Visc_cp
    M = M_lf

    rrPTA_FC_fromReal = ((PreFactor * Q * B) / (M * H) ** 2) * (math.sqrt(1 / (u * Phi * Ct)))

    return rrPTA_FC_fromReal


def rrPTA_SRV_fromReal(Temp_BH_F, Visc_cp, ZFactor, Ct, M_PSS):
    conv = 460
    PreFactor = 0.234

    t = Temp_BH_F + 460
    u = Visc_cp
    Z = ZFactor
    M = M_PSS

    rrPTA_SRV_fromReal = (PreFactor * t) / (u * Z * Ct * M)

    return rrPTA_SRV_fromReal


def rrPTA_K_fromMpp(T_hrs, Phi, Visc_cp, Ct, StageLength_ft):
    conv = 5.615
    PreFactor = 948

    t = T_hrs
    u = Visc_cp
    xS = StageLength_ft

    rrPTA_K_fromMpp = (PreFactor * Phi * u * xS ** 2) / (16 * t)

    return rrPTA_K_fromMpp


def rrPTA_XfSqrK_fromMPP(T_hrs, Phi, Visc_cp, Ct, Stages, H_ft, M_lf):
    conv = 5.615
    PreFactor = 40.93

    t = T_hrs
    u = Visc_cp
    H = H_ft

    rrPTA_XfSqrK_fromMPP = (PreFactor * t) / (M_lf * H) * math.sqrt(1 / (Phi * u * Ct))

    return rrPTA_XfSqrK_fromMPP


def rrLFA_TDXF(Time_Days, K_nd, Xf_ft, Phi, Visc_cp, Ct):
    """Linear Flow Approximation Analysis: Dimensionless Time with respect to fracture half length:
    SPE 39931
    """

    t = Time_Days + 0.5
    # Assume that flow rate and pressure measurements are average measurements, with average time set to mid-day
    K = K_nd / 1000000
    Xf = Xf_ft
    Ui = Visc_cp
    Cti = Ct

    TDXF = 0.0063288 * t * K / (Phi * Ui * Cti * Xf ** 2)

    rrLFA_TDXF = TDXF

    return rrLFA_TDXF


def rrLFA_TDYE(FracHalfLength_ft, ClusterSpacing_ft, TDXF):
    """Linear Flow Approximation Analysis: Dimensionless Time with respect to fracture interference perpendicular to the fracture half-length
    First interference occurs when TDye = 0.25, which correlates to 0.25/(Xf/Ye)^2
    Following this dimensionless time, following interference occurs when interference occurs from the extent of the formation thickness

    Ye_ft represents the horizontal perpendicular distance to the fracture (cluster spacing / or stage lengths depending on theoretical model)
    H_ft represents the vertical perpendicular distance to the fracture (formation thickness - assuming that well is centered)

    SPE 39931
    """

    Xf = FracHalfLength_ft
    Ye = ClusterSpacing_ft

    TDYE_Ye = (Xf / Ye) ** 2 * TDXF

    rrLFA_TDYE = TDYE_Ye

    return rrLFA_TDYE


def rrLFA_QdExp(TDYE):
    Integral = 0
    Integral_Prev = math.exp(-Pii() ** 2 * TDYE / 4)
    Integral_Next = 0
    n = 1
    for n in range(10):
        Integral_Prev = math.exp(-(2 * n - 1) ** 2 * Pii() ** 2 * TDYE / 4)
        Integral = Integral + (Integral_Next + Integral_Prev)
        Integral_Next = Integral_Prev

    rrLFA_QdExp = Integral

    return rrLFA_QdExp


def rrLFA_Qd(ConstantRateDuration_days, Time_Days, Fractures, FracHalfLength_ft, ClusterSpacing_ft, TDYE, TDXF):
    Tk = ConstantRateDuration_days
    t = Time_Days
    Xf = FracHalfLength_ft
    Ye = ClusterSpacing_ft
    Qd_CP = 0
    Qd_CR = 0
    Qd = 0

    # Ye = Sqr(Ye * Xf / Pii())

    DE_Solution = 1  # Default to Constant Rate Case

    if t <= Tk:
        DE_Solution = 1
    else:
        DE_Solution = 2

    # Diffusivity Equation Solutions depending on dimensionless time

    if DE_Solution == 1:
        if TDYE < 0.5:
            Qd_CR = Fractures * ((math.sqrt(Pii() * TDXF)) ** -1)
        else:
            Qd_CR = Fractures * ((Pii() / 2 * (Xf / Ye) * TDXF + Pii() / 6 * (Ye / Xf)) ** -1)

    elif DE_Solution == 2:
        if TDYE < 0.25:
            Qd_CP = Fractures * (((Pii() / 2) * math.sqrt(Pii() * TDXF)) ** -1)
        else:
            TDYE = TDYE
            Qd_CP = Fractures * (((Pii() / 4) * (Ye / Xf) * math.exp((Pii() ** 2 * TDYE / 4))) ** -1)

    # Special Case: Average of Constant Rate and Constant Pressure Solutions

    Qd_Avg = (Qd_CP + Qd_CR) / 2

    if DE_Solution == 1:
        Qd = Qd_CR
    elif DE_Solution == 2:
        Qd = Qd_CP
    elif DE_Solution == 3:
        Qd = Qd_Avg

    rrLFA_Qd = Qd

    return rrLFA_Qd
