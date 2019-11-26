# -*- coding: utf-8 -*-
"""
This file contains the main loop for the DGLAP calculations.

"""
import logging
import numpy as np

from eko import t_float
import eko.alpha_s as alpha_s
import eko.splitting_functions_LO as sf_LO
import eko.interpolation as interpolation
import eko.mellin as mellin
from eko.constants import Constants

logObj = logging.getLogger(__name__)

def _get_xgrid(setup):
    """Compute input grid

    Parameters
    ----------
    setup : dict
        a dictionary with the theory parameters for the evolution

    Returns
    -------
        xgrid : array
            input grid
    """
    xgrid = np.array([])
    # grid type
    xgrid_type = setup.get("xgrid_type", "Chebyshev@log")
    if xgrid_type == "custom": # custom grid
        if "xgrid_custom" not in setup:
            raise ValueError("'xgrid_type' is 'custom', but 'xgrid_custom' is not given")
        xgrid = np.array(setup["xgrid_custom"])
    else: # auto-generated grid
        # read params
        xgrid_size = setup["xgrid_size"]
        xgrid_min = setup.get("xgrid_min", 1e-7)
        # generate
        if xgrid_type == "Chebyshev@log":
            xgrid = interpolation.get_xgrid_Chebyshev_at_log(xgrid_size, xgrid_min)
        elif xgrid_type == "linear@log":
            xgrid = interpolation.get_xgrid_linear_at_log(xgrid_size, xgrid_min)
        else:
            raise ValueError("Unkonwn 'xgrid_type'")
    unique_xgrid = np.unique(xgrid)
    if not len(unique_xgrid) == len(xgrid):
        raise ValueError("given 'xgrid' is not unique!") # relax to warning?
    return unique_xgrid


def _get_evoultion_params(setup):
    """Compute evolution parameters

    Parameters
    ----------
    setup: dict
        a dictionary with the theory parameters for the evolution

    Returns
    -------
        delta_t : t_float
            scale difference
    """
    # setup constants
    nf = setup["NfFF"]
    # setup inital+final scale
    # TODO iterate Q2grid
    qref2 = setup["Qref"] ** 2
    pto = setup["PTO"]
    alphas = setup["alphas"]
    # Generate the alpha_s functions
    a_s = alpha_s.alpha_s_generator(alphas, qref2, nf, "analytic")
    a0 = a_s(pto, setup["Q0"]**2)
    a1 = a_s(pto, setup["Q2grid"][0])
    # evolution parameters
    t0 = np.log(1.0 / a0)
    t1 = np.log(1.0 / a1)
    return t1 - t0

def _run_nonsinglet(setup,constants,delta_t,is_log_interpolation,basis_function_coeffs,ret):
    """Solves the non-singlet case.

    This method updates the `ret` parameter instead of returning something.

    Parameters
    ----------
        setup : dict
            a dictionary with the theory parameters for the evolution
        constants : Constants
            used set of constants
        delta_t : t_float
            evolution step
        is_log_interpolation : bool
            use a logarithmic interpolation
        basis_function_coeffs : array
            coefficient list for the basis functions
        ret : dict
            a dictionary for the output
    """
    # setup constants
    xgrid = ret["xgrid"]
    targetgrid = ret["targetgrid"]
    targetgrid_size = len(targetgrid)
    nf = setup["NfFF"]
    beta0 = alpha_s.beta_0(nf, constants.CA, constants.CF, constants.TF)

    # prepare
    def get_kernel_ns(j,lnx):
        """return non-siglet integration kernel"""
        current_coeff = basis_function_coeffs.basis[j]
#         if is_log_interpolation:
#             fN = interpolation.evaluate_Lagrange_basis_function_log_N
#         else:
#             fN = interpolation.evaluate_Lagrange_basis_function_N
        def ker(N):
            """non-siglet integration kernel"""
            ln = -delta_t * sf_LO.gamma_ns_0(N, nf, constants.CA, constants.CF) / beta0
            #interpoln = interpolation.get_Lagrange_interpolators_log_N(N, xgrid, j)
            interpoln = current_coeff.evaluate_N(N, j, lnx)
#             fN(N,current_coeff,lnx)
            return np.exp(ln) * interpoln

        return ker

    # perform
    xgrid_size = len(xgrid)
    void = np.zeros((targetgrid_size, xgrid_size), dtype=t_float)
    op_ns = np.copy(void)
    op_ns_err = np.copy(void)
    #path, jac = mellin.get_path_Talbot()
    logPre = "computing NS operator - "
    logObj.info(logPre+"...")
    for k,xk in enumerate(targetgrid):
        #path,jac = mellin.get_path_line(path_length)
        if False and xk < 1e-3:
            cut = 0.1
            gamma = 2.0
        else:
            cut = 1e-2
            gamma = 1.0
        path,jac = mellin.get_path_Cauchy_tan(gamma,1.0)
        for j in range(xgrid_size):
            res = mellin.inverse_mellin_transform(
                get_kernel_ns(j,np.log(xk)), path, jac, cut
            )
            op_ns[k, j] = res[0]
            op_ns_err[k, j] = res[1]
        logObj.info(logPre+" %d/%d",k+1,targetgrid_size)
    logObj.info(logPre+"done.")

    # insert operators
    ret["operators"]["NS"] = op_ns
    ret["operator_errors"]["NS"] = op_ns_err


def _run_singlet(setup,constants,delta_t,is_log_interpolation,basis_function_coeffs,ret):
    """Solves the singlet case.

    This method updates the `ret` parameter instead of returning something.

    Parameters
    ----------
        setup : dict
            a dictionary with the theory parameters for the evolution
        constants : Constants
            used set of constants
        delta_t : t_float
            evolution step
        is_log_interpolation : bool
            use a logarithmic interpolation
        basis_function_coeffs : array
            coefficient list for the basis functions
        ret : dict
            a dictionary for the output
    """
    # setup constants
    xgrid = ret["xgrid"]
    targetgrid = ret["targetgrid"]
    targetgrid_size = len(targetgrid)
    nf = setup["NfFF"]
    beta0 = alpha_s.beta_0(nf, constants.CA, constants.CF, constants.TF)

    # prepare
    def get_kernels_s(j,lnx):
        """return siglet integration kernels"""
        current_coeff = basis_function_coeffs[j]
        if is_log_interpolation:
            fN = interpolation.evaluate_Lagrange_basis_function_log_N
        else:
            fN = interpolation.evaluate_Lagrange_basis_function_N
        def get_ker(k,l):
            def ker(N):
                """singlet integration kernel"""
                l_p,l_m,e_p,e_m = sf_LO.get_Eigensystem_gamma_singlet_0(N,nf,constants.CA,constants.CF)
                ln_p = - delta_t * l_p  / beta0
                ln_m = - delta_t * l_m  / beta0
                interpoln = fN(N,current_coeff,lnx)
                return (e_p[k][l] * np.exp(ln_p) + e_m[k][l] * np.exp(ln_m)) * interpoln
            return ker

        return get_ker(0,0), get_ker(0,1), get_ker(1,0), get_ker(1,1)

    # perform
    xgrid_size = len(xgrid)
    void = np.zeros((targetgrid_size, xgrid_size), dtype=t_float)
    op_s_qq = np.copy(void)
    op_s_qg = np.copy(void)
    op_s_gq = np.copy(void)
    op_s_gg = np.copy(void)
    op_s_qq_err = np.copy(void)
    op_s_qg_err = np.copy(void)
    op_s_gq_err = np.copy(void)
    op_s_gg_err = np.copy(void)
    #path, jac = mellin.get_path_Talbot()
    logPre = "computing singlet operator - "
    logObj.info(logPre+"...")
    for k,xk in enumerate(targetgrid):
        #path,jac = mellin.get_path_line(path_length)
        if False and xk < 1e-3:
            cut = 0.1
            gamma = 2.0
        else:
            cut = 1e-2
            gamma = 1.0
        path,jac = mellin.get_path_Cauchy_tan(gamma,1.0)
        for j in range(xgrid_size):
            # iterate all matrix elements
            ker_qq,ker_qg,ker_gq,ker_gg = get_kernels_s(j,np.log(xk))
            for ker,op,op_err in [
                    (ker_qq,op_s_qq,op_s_qq_err),(ker_qg,op_s_qg,op_s_qg_err),
                    (ker_gq,op_s_gq,op_s_gq_err),(ker_gg,op_s_gg,op_s_gg_err)
                ]:
                res = mellin.inverse_mellin_transform(ker, path, jac, cut)
                op[k, j] = res[0]
                op_err[k, j] = res[1]
        logObj.info(logPre+" %d/%d",k+1,targetgrid_size)
    logObj.info(logPre,"done.")

    # insert operators
    ret["operators"]["S_qq"] = op_s_qq
    ret["operators"]["S_qg"] = op_s_qg
    ret["operators"]["S_gq"] = op_s_gq
    ret["operators"]["S_gg"] = op_s_gg
    ret["operator_errors"]["S_qq"] = op_s_qq_err
    ret["operator_errors"]["S_qg"] = op_s_qg_err
    ret["operator_errors"]["S_gq"] = op_s_gq_err
    ret["operator_errors"]["S_gg"] = op_s_gg_err

def run_dglap(setup):
    r"""This function takes a DGLAP theory configuration dictionary
    and performs the solution of the DGLAP equations.

    The EKO :math:`\hat O_{k,j}^{(0)}(t_1,t_0)` is determined in order
    to fullfill the following evolution

    .. math::
        f^{(0)}(x_k,t_1) = \hat O_{k,j}^{(0)}(t_1,t_0) f^{(0)}(x_j,t_0)

    Parameters
    ----------
    setup: dict
        a dictionary with the theory parameters for the evolution

        =============== ==========================================================================
        key             description
        =============== ==========================================================================
        'PTO'           order of perturbation theory: ``0`` = LO, ...
        'alphas'        reference value of the strong coupling :math:`\alpha_s(\mu_0^2)`
        'xgrid_size'    size of the interpolation grid
        'xgrid_min'     lower boundry of the interpolation grid - defaults to ``1e-7``
        'xgrid_type'    generating function for the interpolation grid - see below
        'targetgrid'    list of x-values which are computed - defaults to ``xgrid``, if not given
        =============== ==========================================================================

    Returns
    -------
    ret: dict
        a dictionary with a defined set of keys

        ============  ============================================================================
        key           description
        ============  ============================================================================
        'xgrid'       list of x-values which build the support of the interpolation
        'targetgrid'  list of x-values which are computed
        'operators'   list of computed operators
        ============  ============================================================================

    Notes
    -----

    * xgrid_type
        - ``linear@log``: nodes distributed linear in log-space
        - ``custom``: custom xgrid, supplied by the key ``xgrid_custom``

    """

    # print theory id setup
    logObj.info("setup: %s",setup)

    # return dictionay
    # TODO decide on which level to iterate Q2
    ret = {}

    # evolution parameters
    delta_t = _get_evoultion_params(setup)

    # setup input grid: xgrid
    xgrid = _get_xgrid(setup)
    ret["xgrid"] = xgrid
    polynom_rank = setup.get("xgrid_polynom_rank",4)
    is_log_interpolation = not setup.get("xgrid_interpolation","log") == "id"
    basis_function_dispatcher = interpolation.InterpolatorDispatcher(xgrid, polynom_rank, is_log_interpolation)
    if is_log_interpolation:
        basis_function_coeffs = interpolation.get_Lagrange_basis_functions_log(xgrid,polynom_rank)
    else:
        basis_function_coeffs = interpolation.get_Lagrange_basis_functions(xgrid,polynom_rank)
    logObj.info("is_log_interpolation = %s",is_log_interpolation)

    # setup output grid: targetgrid
    targetgrid = setup.get("targetgrid", xgrid)
    ret["targetgrid"] = targetgrid

    # prepare return of operators
    ret["operators"] = {"NS": None,"S_qq": None,"S_qg": None,"S_gq": None,"S_gg": None}
    ret["operator_errors"] = {"NS": None,"S_qq": None,"S_qg": None,"S_gq": None,"S_gg": None}

    # load constants
    constants = Constants()

    # run non-singlet
    _run_nonsinglet(setup,constants,delta_t,is_log_interpolation,basis_function_dispatcher,ret)

    # run singlet
    _run_singlet(setup,constants,delta_t,is_log_interpolation,basis_function_coeffs,ret)

    #   Points to be implemented:
    #   TODO implement NLO
    return ret
