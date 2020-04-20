
import math
import libxfoil.dylib


# REFERENCE VALUES #######
# The mars atmosphere values has been approximated to the values of the carbon dioxide (95%)

  g_mars = 3.711  #[m/s^2]
  mu_mars = 13.695  #[microPa*s]
  rho_mars = 0.0198  #[kg/m^3]
  nu_mars = mu_mars * (10 ** (- 6)) / rho_mars  #[m^2/s]

# INPUT PARAMETERS #######

  # DRONE CHARACTERISTICS

  drone_weight = 2  #[kg]
  prop_radio = 0.4  #[m]
  prop_n = 4  #[-]
  prop_blades = 2  #[-]
  prop_rpm = 2300  #[rpm]

    # POWER REQUIREMENTS & SOME CALCULATIONS

    prop_omega = prop_rpm * pi / 30  #[rad/s]
    prop_area = prop_n * pi * prop_radio ** 2  #[m^2]
    v_1 = math.sqrt((2 * drone_weight *g_mars) / (rho_mars * prop_area))  #[m/s]
    power_req = 0.5 * rho_mars * prop_area * v_1 ** 3  #[W]

  # ANALYSIS PARAMETERS

  a_i = 0.01  # By default
  a_step = 0.01  # By default
  cl_i = 1   # By default
  diff_r = prop_radio / 10  # By default


# PROPELLER AIRFOIL CHARACTERIZATION #######

  for diff_r <= prop_radio:

    r = diff_r
    a = a_i
    a_a = 0
    a_max = 0
    a_p_a = 0
    a_p_max =
    G = 0
    G_a = 0
    G_max = 0

    while G = G_a:

      tan_phi = (1 - math.sqrt(1 + 4 * (v_1 / prop_omega * r) ** 2 * a * (a - a))) / (2 * a * v_1 / (prop_omega * r))
      phi = math.atan(tan_phi)
      a_p = (v_1 * (1 - a)) / (prop_omega * r * tan_phi) + 1
      f = (prop_blades * (prop_radio - r)) / (2 * prop_radio * math.sin(phi))
      F = 2 / pi * math.acos( exp( - f ))
      G = F * (1 - a) * a_p

      if G < G_a:
        G_max = G_a
        a_max = a_a
        a_p_max = a_p_a
        break

      else:
        a = a + a_step
        G_a = G
        a_a = a
        a_p_a = a_p

    v_r = math.sqrt(v_1 ** 2 * (1 - a_max) ** 2 + prop_omega ** 2 * r ** 2 * (a_p_max - 1) ** 2)

    # ITERATION & CALL TO XFOIL
      c_l = cl_i

      if

        c = (a_max * 8 * pi * r * math.sin(phi) ** 2) / ((1 - a_max) * prop_blades * c_l * math.cos(phi))
        re = (v_r * c) / (nu_mars)

        # XFOIL #######

        from xfoil import XFoil
        xf = XFoil()

        # Import an airfoil
        from xfoil.test import XXXXX
        xf.airfoil = XXXXX

        # Setting up the analysis parameters
        xf.Re = re
        xf.max_iter = 100
        xf.M = 0.7

        # Obtaining the angle of attack, lift coefficient, drag coefficient and momentum coefficient of the airfoil
        a, cl, cd, cm = xf.aseq(0, 30, 0.5)
















  .
