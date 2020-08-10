# -*- coding: utf-8 -*-
"""
    This file contains the next-to-leading-order Altarelli-Parisi splitting kernels.

    These expression have been obtained using the procedure described in the
    `wiki <https://github.com/N3PDF/eko/wiki/Parse-NLO-expressions>`_
    involving ``FormGet`` :cite:`Hahn:2016ebn`.
"""

import numpy as np
import numba as nb

from eko import ekomath


@nb.njit
def gamma_nsm_1(n, nf: int, CA: float, CF: float):
    """
        Computes the next-to-leading-order valence-like non-singlet anomalous dimension.

        Implements Eq. (3.5) of :cite:`Moch:2004pa`.

        Parameters
        ----------
            n : complex
                Mellin moment
            nf : int
                Number of active flavours
            CA : float
                Casimir constant of adjoint representation
            CF : float
                Casimir constant of fundamental representation

        Returns
        -------
            gamma_nsm_1 : complex
                Next-to-leading-order valence-like non-singlet anomalous dimension
                :math:`\\gamma_{ns,-}^{(1)}(N)`
    """
    S1 = ekomath.harmonic_S1(n)
    S2 = ekomath.harmonic_S2(n)
    # Here, Sp refers to S' ("s-prime") (german: "s-strich" or in Pegasus language: SSTR)
    # of :cite:`Gluck:1989ze` and NOT to the Spence function a.k.a. dilogarithm
    Sp1m = ekomath.harmonic_S1((n - 1) / 2)
    Sp2m = ekomath.harmonic_S2((n - 1) / 2)
    Sp3m = ekomath.harmonic_S3((n - 1) / 2)
    g3n = ekomath.mellin_g3(n)
    zeta2 = ekomath.zeta2
    zeta3 = ekomath.zeta3
    # fmt: off
    gqq1m_cfca = 16*g3n - (144 + n*(1 + n)*(156 + n*(340 + n*(655 + 51*n*(2 + n)))))/(18.*np.power(n,3)*np.power(1 + n,3)) + (-14.666666666666666 + 8/n - 8/(1 + n))*S2 - (4*Sp2m)/(n + np.power(n,2)) + S1*(29.77777777777778 + 16/np.power(n,2) - 16*S2 + 8*Sp2m) + 2*Sp3m + 10*zeta3 + zeta2*(16*S1 - 16*Sp1m - (16*(1 + n*np.log(2)))/n) # pylint: disable=line-too-long
    gqq1m_cfcf = -32*g3n + (24 - n*(-32 + 3*n*(-8 + n*(3 + n)*(3 + np.power(n,2)))))/(2.*np.power(n,3)*np.power(1 + n,3)) + (12 - 8/n + 8/(1 + n))*S2 + S1*(-24/np.power(n,2) - 8/np.power(1 + n,2) + 16*S2 - 16*Sp2m) + (8*Sp2m)/(n + np.power(n,2)) - 4*Sp3m - 20*zeta3 + zeta2*(-32*S1 + 32*Sp1m + 32*(1/n + np.log(2))) # pylint: disable=line-too-long
    gqq1m_cfnf = (-12 + n*(20 + n*(47 + 3*n*(2 + n))))/(9.*np.power(n,2)*np.power(1 + n,2)) - (40*S1)/9. + (8*S2)/3. # pylint: disable=line-too-long
    # fmt: on
    result = CF * (CA * gqq1m_cfca + CF * gqq1m_cfcf + nf * gqq1m_cfnf)
    return result


@nb.njit
def gamma_nsp_1(n, nf: int, CA: float, CF: float):
    """
        Computes the next-to-leading-order singlet-like non-singlet anomalous dimension.

        Implements Eq. (3.5) of :cite:`Moch:2004pa`.

        Parameters
        ----------
            n : complex
                Mellin moment
            nf : int
                Number of active flavours
            CA : float
                Casimir constant of adjoint representation
            CF : float
                Casimir constant of fundamental representation

        Returns
        -------
            gamma_nsp_1 : complex
                Next-to-leading-order singlet-like non-singlet anomalous dimension
                :math:`\\gamma_{ns,+}^{(1)}(N)`
    """
    S1 = ekomath.harmonic_S1(n)
    S2 = ekomath.harmonic_S2(n)
    Sp1p = ekomath.harmonic_S1(n / 2)
    Sp2p = ekomath.harmonic_S2(n / 2)
    Sp3p = ekomath.harmonic_S3(n / 2)
    g3n = ekomath.mellin_g3(n)
    zeta2 = ekomath.zeta2
    zeta3 = ekomath.zeta3
    # fmt: off
    gqq1p_cfca = -16*g3n + (132 - n*(340 + n*(655 + 51*n*(2 + n))))/(18.*np.power(n,2)*np.power(1 + n,2)) + (-14.666666666666666 + 8/n - 8/(1 + n))*S2 - (4*Sp2p)/(n + np.power(n,2)) + S1*(29.77777777777778 - 16/np.power(n,2) - 16*S2 + 8*Sp2p) + 2*Sp3p + 10*zeta3 + zeta2*(16*S1 - 16*Sp1p + 16*(1/n - np.log(2))) # pylint: disable=line-too-long
    gqq1p_cfcf = 32*g3n - (8 + n*(32 + n*(40 + 3*n*(3 + n)*(3 + np.power(n,2)))))/(2.*np.power(n,3)*np.power(1 + n,3)) + (12 - 8/n + 8/(1 + n))*S2 + S1*(40/np.power(n,2) - 8/np.power(1 + n,2) + 16*S2 - 16*Sp2p) + (8*Sp2p)/(n + np.power(n,2)) - 4*Sp3p - 20*zeta3 + zeta2*(-32*S1 + 32*Sp1p + 32*(-(1/n) + np.log(2))) # pylint: disable=line-too-long
    gqq1p_cfnf = (-12 + n*(20 + n*(47 + 3*n*(2 + n))))/(9.*np.power(n,2)*np.power(1 + n,2)) - (40*S1)/9. + (8*S2)/3. # pylint: disable=line-too-long
    # fmt: on
    result = CF * (CA * gqq1p_cfca + CF * gqq1p_cfcf + nf * gqq1p_cfnf)
    return result


@nb.njit
def gamma_ps_1(n, nf: int, CA: float, CF: float):  # pylint: disable=unused-argument
    """
        Computes the next-to-leading-order pure-singlet quark-quark anomalous dimension.

        Implements Eq. (3.6) of :cite:`Vogt:2004mw`.

        Parameters
        ----------
            n : complex
                Mellin moment
            nf : int
                Number of active flavours
            CA : float
                Casimir constant of adjoint representation
            CF : float
                Casimir constant of fundamental representation

        Returns
        -------
            gamma_ps_1 : complex
                Next-to-leading-order pure-singlet quark-quark anomalous dimension
                :math:`\\gamma_{ps}^{(1)}(N)`
    """
    # fmt: off
    gqqps1_nfcf = (-4*(2 + n*(5 + n))*(4 + n*(4 + n*(7 + 5*n))))/((-1 + n)*np.power(n,3)*np.power(1 + n,3)*np.power(2 + n,2)) # pylint: disable=line-too-long
    # fmt: on
    result = nf * CF * gqqps1_nfcf
    return result


@nb.njit
def gamma_qg_1(n, nf: int, CA: float, CF: float):
    """
        Computes the next-to-leading-order quark-gluon singlet anomalous dimension.

        Implements Eq. (3.7) of :cite:`Vogt:2004mw`.

        Parameters
        ----------
            n : complex
                Mellin moment
            nf : int
                Number of active flavours
            CA : float
                Casimir constant of adjoint representation
            CF : float
                Casimir constant of fundamental representation

        Returns
        -------
            gamma_qg_1 : complex
                Next-to-leading-order quark-gluon singlet anomalous dimension
                :math:`\\gamma_{qg}^{(1)}(N)`
    """
    S1 = ekomath.harmonic_S1(n)
    S2 = ekomath.harmonic_S2(n)
    Sp2p = ekomath.harmonic_S2(n / 2)
    # fmt: off
    gqg1_nfca = (-4*(16 + n*(64 + n*(104 + n*(128 + n*(85 + n*(36 + n*(25 + n*(15 + n*(6 + n))))))))))/((-1 + n)*np.power(n,3)*np.power(1 + n,3)*np.power(2 + n,3)) - (16*(3 + 2*n)*S1)/np.power(2 + 3*n + np.power(n,2),2) + (4*(2 + n + np.power(n,2))*np.power(S1,2))/(n*(2 + 3*n + np.power(n,2))) - (4*(2 + n + np.power(n,2))*S2)/(n*(2 + 3*n + np.power(n,2))) + (4*(2 + n + np.power(n,2))*Sp2p)/(n*(2 + 3*n + np.power(n,2))) # pylint: disable=line-too-long
    gqg1_nfcf = (-2*(4 + n*(8 + n*(1 + n)*(25 + n*(26 + 5*n*(2 + n))))))/(np.power(n,3)*np.power(1 + n,3)*(2 + n)) + (8*S1)/np.power(n,2) - (4*(2 + n + np.power(n,2))*np.power(S1,2))/(n*(2 + 3*n + np.power(n,2))) + (4*(2 + n + np.power(n,2))*S2)/(n*(2 + 3*n + np.power(n,2))) # pylint: disable=line-too-long
    # fmt: on
    result = nf * (CA * gqg1_nfca + CF * gqg1_nfcf)
    return result


@nb.njit
def gamma_gq_1(n, nf: int, CA: float, CF: float):
    """
        Computes the next-to-leading-order gluon-quark singlet anomalous dimension.

        Implements Eq. (3.8) of :cite:`Vogt:2004mw`.

        Parameters
        ----------
            n : complex
                Mellin moment
            nf : int
                Number of active flavours
            CA : float
                Casimir constant of adjoint representation
            CF : float
                Casimir constant of fundamental representation

        Returns
        -------
            gamma_gq_1 : complex
                Next-to-leading-order gluon-quark singlet anomalous dimension
                :math:`\\gamma_{gq}^{(1)}(N)`
    """
    S1 = ekomath.harmonic_S1(n)
    S2 = ekomath.harmonic_S2(n)
    Sp2p = ekomath.harmonic_S2(n / 2)
    # fmt: off
    ggq1_cfcf = (-8 + 2*n*(-12 + n*(-1 + n*(28 + n*(43 + 6*n*(5 + 2*n))))))/((-1 + n)*np.power(n,3)*np.power(1 + n,3)) - (4*(10 + n*(17 + n*(8 + 5*n)))*S1)/((-1 + n)*n*np.power(1 + n,2)) + (4*(2 + n + np.power(n,2))*np.power(S1,2))/(n*(-1 + np.power(n,2))) + (4*(2 + n + np.power(n,2))*S2)/(n*(-1 + np.power(n,2))) # pylint: disable=line-too-long
    ggq1_cfca = (-4*(144 + n*(432 + n*(-152 + n*(-1304 + n*(-1031 + n*(695 + n*(1678 + n*(1400 + n*(621 + 109*n))))))))))/(9.*np.power(n,3)*np.power(1 + n,3)*np.power(-2 + n + np.power(n,2),2)) + (4*(-12 + n*(-22 + 41*n + 17*np.power(n,3)))*S1)/(3.*np.power(-1 + n,2)*np.power(n,2)*(1 + n)) + ((8 + 4*n + 4*np.power(n,2))*np.power(S1,2))/(n - np.power(n,3)) + ((8 + 4*n + 4*np.power(n,2))*S2)/(n - np.power(n,3)) + (4*(2 + n + np.power(n,2))*Sp2p)/(n*(-1 + np.power(n,2))) # pylint: disable=line-too-long
    ggq1_cfnf = (8*(16 + n*(27 + n*(13 + 8*n))))/(9.*(-1 + n)*n*np.power(1 + n,2)) - (8*(2 + n + np.power(n,2))*S1)/(3.*n*(-1 + np.power(n,2))) # pylint: disable=line-too-long
    # fmt: on
    result = CF * (CA * ggq1_cfca + CF * ggq1_cfcf + nf * ggq1_cfnf)
    return result


@nb.njit
def gamma_gg_1(n, nf: int, CA: float, CF: float):
    """
        Computes the next-to-leading-order gluon-gluon singlet anomalous dimension.

        Implements Eq. (3.9) of :cite:`Vogt:2004mw`.

        Parameters
        ----------
            n : complex
                Mellin moment
            nf : int
                Number of active flavours
            CA : float
                Casimir constant of adjoint representation
            CF : float
                Casimir constant of fundamental representation

        Returns
        -------
            gamma_gg_1 : complex
                Next-to-leading-order gluon-gluon singlet anomalous dimension
                :math:`\\gamma_{gg}^{(1)}(N)`
    """
    S1 = ekomath.harmonic_S1(n)
    Sp1p = ekomath.harmonic_S1(n / 2)
    Sp2p = ekomath.harmonic_S2(n / 2)
    Sp3p = ekomath.harmonic_S3(n / 2)
    g3n = ekomath.mellin_g3(n)
    zeta2 = ekomath.zeta2
    zeta3 = ekomath.zeta3
    # fmt: off
    ggg1_caca = 16*g3n - (2*(576 + n*(1488 + n*(560 + n*(-1248 + n*(-1384 + n*(1663 + n*(4514 + n*(4744 + n*(3030 + n*(1225 + 48*n*(7 + n))))))))))))/(9.*np.power(-1 + n,2)*np.power(n,3)*np.power(1 + n,3)*np.power(2 + n,3)) + S1*(29.77777777777778 + 16/np.power(-1 + n,2) + 16/np.power(1 + n,2) - 16/np.power(2 + n,2) - 8*Sp2p) + (16*(1 + n + np.power(n,2))*Sp2p)/(n*(1 + n)*(-2 + n + np.power(n,2))) - 2*Sp3p - 10*zeta3 + zeta2*(-16*S1 + 16*Sp1p + 16*(-(1/n) + np.log(2))) # pylint: disable=line-too-long
    ggg1_canf = (8*(6 + n*(1 + n)*(28 + n*(1 + n)*(13 + 3*n*(1 + n)))))/(9.*np.power(n,2)*np.power(1 + n,2)*(-2 + n + np.power(n,2))) - (40*S1)/9. # pylint: disable=line-too-long
    ggg1_cfnf = (2*(-8 + n*(-8 + n*(-10 + n*(-22 + n*(-3 + n*(6 + n*(8 + n*(4 + n)))))))))/(np.power(n,3)*np.power(1 + n,3)*(-2 + n + np.power(n,2))) # pylint: disable=line-too-long
    # fmt: on
    result = CA * CA * ggg1_caca + nf * (CA * ggg1_canf + CF * ggg1_cfnf)
    return result