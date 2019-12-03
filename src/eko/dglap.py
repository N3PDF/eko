# -*- coding: utf-8 -*-
"""
This file contains the main loop for the DGLAP calculations.

"""
import logging
import joblib
import numpy as np

import eko.alpha_s as alpha_s
import eko.interpolation as interpolation
import eko.mellin as mellin
from eko.kernel_generation import KernelDispatcher
from eko.constants import Constants
import sys

logger = logging.getLogger(__name__)

def _parallelize_on_basis(basis_functions, pfunction, xk, n_jobs=1):
    out = joblib.Parallel(n_jobs=n_jobs)(
        joblib.delayed(pfunction)(fun, xk) for fun in basis_functions
    )
    return out


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
    qref2 = setup["Qref"] ** 2
    pto = setup["PTO"]
    alphas = setup["alphas"]
    # Generate the alpha_s functions
    a_s = alpha_s.alpha_s_generator(alphas, qref2, nf, "analytic")
    a0 = a_s(pto, setup["Q0"] ** 2)
    a1 = a_s(pto, setup["Q2grid"][0])
    # evolution parameters
    t0 = np.log(1.0 / a0)
    t1 = np.log(1.0 / a1)
    return t1 - t0


def _run_nonsinglet(kernel_dispatcher, targetgrid, ret):
    """Solves the non-singlet case.

    This method updates the `ret` parameter instead of returning something.

    Parameters
    ----------
        kernel_dispatcher:
            instance of kerneldispatcher from which compiled kernels can be
            obtained
        targetgrid:
            list of x-values which are computed
        ret : dict
            a dictionary for the output
    """
    # Receive all precompiled kernels
    kernels = kernel_dispatcher.compile_nonsinglet()

    # Setup path
    gamma = 1.0
    cut = 1e-2
    path, jac = mellin.get_path_Cauchy_tan(gamma, 1.0)

    # Generate integrands
    integrands = []
    for kernel in kernels:
        kernel_int = mellin.compile_integrand(kernel, path, jac)
        integrands.append(kernel_int)

    def run_thread(integrand, logx):
        result = mellin.inverse_mellin_transform(integrand, cut, logx)
        return result

    log_prefix = "computing NS operator - %s"
    logger.info(log_prefix, "kernel compiled")
    operators = []
    operator_errors = []

    targetgrid_size = len(targetgrid)
    for k, xk in enumerate(targetgrid):
        out = _parallelize_on_basis(integrands, run_thread, np.log(xk))
        operators.append(np.array(out)[:, 0])
        operator_errors.append(np.array(out)[:, 1])
        log_text = f"{k+1}/{targetgrid_size}"
        logger.info(log_prefix, log_text)
    logger.info(log_prefix, "done.")

    # insert operators #TODO return the operators instead
    ret["operators"]["NS"] = np.array(operators)
    ret["operator_errors"]["NS"] = np.array(operator_errors)


def _run_singlet(kernel_dispatcher, targetgrid, ret):
    """Solves the singlet case.

    Parameters
    ----------
        kernel_dispatcher:
            instance of kerneldispatcher from which compiled kernels can be
            obtained
        targetgrid:
            list of x-values which are computed
        ret : dict
            a dictionary for the output
    """
    # Receive all precompiled kernels
    kernels = kernel_dispatcher.compile_singlet()

    # Setup path
    cut = 1e-2
    gamma = 1.0
    path, jac = mellin.get_path_Cauchy_tan(gamma, 1.0)

    # Generate integrands
    integrands = []
    for kernel_set in kernels:
        kernel_int = []
        for ker in kernel_set:
            kernel_int.append(mellin.compile_integrand(ker, path, jac))
        integrands.append(kernel_int)

    # perform
    log_prefix = "computing singlet operator - "
    logger.info(log_prefix, "kernel compiled")

    def run_thread(integrands, logx):
        """ The output of this function is a list of tuple (result, error)
        for qq, qg, gq, gg in that order """
        all_res = []
        for integrand in integrands:
            result = mellin.inverse_mellin_transform(integrand, cut, logx)
            all_res.append(result)
        return all_res

    all_output = []
    targetgrid_size = len(targetgrid)
    for k, xk in enumerate(targetgrid):
        out = _parallelize_on_basis(integrands, run_thread, np.log(xk))
        all_output.append(out)
        log_text = f"{k+1}/{targetgrid_size}"
        logger.info(log_prefix, log_text)
    logger.info(log_prefix, "done.")

    output_array = np.array(all_output)

    # insert operators
    ret["operators"]["S_qq"] = output_array[:, :, 0, 0]
    ret["operators"]["S_qg"] = output_array[:, :, 1, 0]
    ret["operators"]["S_gq"] = output_array[:, :, 2, 0]
    ret["operators"]["S_gg"] = output_array[:, :, 3, 0]
    ret["operator_errors"]["S_qq"] = output_array[:, :, 0, 1]
    ret["operator_errors"]["S_qg"] = output_array[:, :, 1, 1]
    ret["operator_errors"]["S_gq"] = output_array[:, :, 2, 1]
    ret["operator_errors"]["S_gg"] = output_array[:, :, 3, 1]


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
        'log_interpol'  boolean, whether it is log interpolation or not, defaults to `True`
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
        - ``linear``: nodes distributed linear in linear-space
        - ``log``: nodes distributed linear in log-space
        - ``custom``: custom xgrid, supplied by the key ``xgrid``

    """

    # Print theory id setup
    logger.info("Setup: %s", setup)

    # Load constants and compute parameters
    constants = Constants()
    nf = setup["NfFF"]
    delta_t = _get_evoultion_params(setup)

    # Setup interpolation
    xgrid = interpolation.generate_xgrid(**setup)
    is_log_interpolation = setup.get("log_interpol", True)
    polynom_rank = setup.get("xgrid_polynom_rank", 4)
    logger.info(
        "Interpolation mode: %s", setup["xgrid_type"],
    )
    logger.info("Log interpolation: %s", is_log_interpolation)
    targetgrid = setup.get("targetgrid", xgrid)
    basis_function_dispatcher = interpolation.InterpolatorDispatcher(
        xgrid, polynom_rank, log=is_log_interpolation
    )

    # Start filling the output dictionary
    ret = {
        "xgrid": xgrid,
        "targetgrid": targetgrid,
        "operators": {},
        "operator_errors": {},
    }

    # Setup the kernel dispatcher
    kernel_dispatcher = KernelDispatcher(
        basis_function_dispatcher, constants, nf, delta_t
    )

    # run non-singlet
    _run_nonsinglet(kernel_dispatcher, targetgrid, ret)

    # run singlet
    _run_singlet(kernel_dispatcher, targetgrid, ret)

    return ret


if __name__ == "__main__":
    n = 3
    xgrid_low = interpolation.get_xgrid_linear_at_log(n, 1e-7, 0.1)
    xgrid_mid = interpolation.get_xgrid_linear_at_id(n, 0.1, 1.0)
    xgrid_high = np.array(
        []
    )  # 1.0-interpolation.get_xgrid_linear_at_log(10,1e-3,1.0 - 0.9)
    xgrid = np.unique(np.concatenate((xgrid_low, xgrid_mid, xgrid_high)))
    polynom_rank = 4
    toy_xgrid = np.array([1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 0.1, 0.3, 0.5, 0.7, 0.9])[
        -3:
    ]

    ret1 = run_dglap(
        {
            "PTO": 0,
            "alphas": 0.35,
            "Qref": np.sqrt(2),
            "Q0": np.sqrt(2),
            "NfFF": 4,
            "xgrid_type": "custom",
            "xgrid": xgrid,
            "xgrid_polynom_rank": polynom_rank,
            "xgrid_interpolation": "log",
            "targetgrid": toy_xgrid,
            "Q2grid": [1e4],
        }
    )
