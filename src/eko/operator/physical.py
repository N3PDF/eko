# -*- coding: utf-8 -*-
import numpy as np

from .. import basis_rotation as br
from . import flavors


class PhysicalOperator:
    """
    This is exposed to the outside world.

    This operator is computed via the composition method of the
    :class:`Operator` class.


    Parameters
    ----------
        op_members : dict
            list of all members
        q2_final : float
            final scale
    """

    def __init__(self, op_members, q2_final):
        self.op_members = op_members
        self.q2_final = q2_final

    @classmethod
    def ad_to_evol_map(cls, op_members, nf, q2_final, is_vfns, intrinsic_range=None):
        """
        Obtain map between the 3-dimensional anomalous dimension basis and the
        4-dimensional evolution basis.

        .. todo:: update docs, in VFNS sometimes IC is irrelevant if nf>=4
                explain which to keep and which to hide

        Parameters
        ----------
            op_members : dict
                operator members in anomalous dimension basis
            nf : int
                number of active light flavors
            is_vfns : bool
                is |VFNS|?
            intrinsic_range : sequence
                intrinsic heavy flavours

        Returns
        -------
            m : dict
                map
        """
        # constant elements
        m = {
            "S.S": op_members["S_qq"],
            "S.g": op_members["S_qg"],
            "g.g": op_members["S_gg"],
            "g.S": op_members["S_gq"],
            "V.V": op_members["NS_v"],
        }
        # add elements which are already active
        for f in range(2, nf + 1):
            n = f ** 2 - 1
            m[f"V{n}.V{n}"] = op_members["NS_m"]
            m[f"T{n}.T{n}"] = op_members["NS_p"]
        # activate one higher element, i.e. where the next heavy quark could participate,
        # but actually it is trivial
        if is_vfns:
            n = (nf + 1) ** 2 - 1
            # without this new heavy quark Vn = V and Tn = S
            m[f"V{n}.V"] = op_members["NS_v"]
            m[f"T{n}.S"] = op_members["S_qq"]
            m[f"T{n}.g"] = op_members["S_qg"]
        # deal with intrinsic heavy quark pdfs
        if intrinsic_range is not None:
            hqfl = "cbt"
            for f in intrinsic_range:
                hq = hqfl[f - 4]  # find name
                # intrinsic means no evolution, i.e. they are evolving with the identity
                op_id = np.eye(op_members["NS_v"].shape[0])
                if f > nf + 1:  # keep the higher quarks as they are
                    m[f"{hq}+.{hq}+"] = op_id
                    m[f"{hq}-.{hq}-"] = op_id
                elif f == nf + 1:  # next is comming hq?
                    n = f ** 2 - 1
                    if is_vfns:
                        # e.g. T15 = (u+ + d+ + s+) - 3c+
                        m[f"V{n}.{hq}-"] = -(f - 1) * op_id
                        m[f"T{n}.{hq}+"] = -(f - 1) * op_id
                    else:
                        m[f"{hq}+.{hq}+"] = op_id
                        m[f"{hq}-.{hq}-"] = op_id
                else:  # f <= nf
                    if not is_vfns:
                        raise ValueError(
                            f"{hq} is perturbative inside FFNS{nf} so can NOT be intrinsic"
                        )
        opms = {}
        for k, v in m.items():
            opms[flavors.MemberName(k)] = v.copy()
        return cls(opms, q2_final)

    def to_flavor_basis_tensor(self):
        """
        Convert the computations into an rank 4 tensor over flavor operator space and
        momentum fraction operator space

        Returns
        -------
            tensor : numpy.ndarray
                EKO
        """
        nf_in, nf_out = flavors.get_range(self.op_members.keys())
        len_pids = len(br.flavor_basis_pids)
        len_xgrid = list(self.op_members.values())[0].value.shape[0]
        # dimension will be pids^2 * xgrid^2
        value_tensor = np.zeros((len_pids, len_xgrid, len_pids, len_xgrid))
        error_tensor = value_tensor.copy()
        for n, op in self.op_members.items():
            in_pids = flavors.pids_from_intrinsic_evol(n.input, nf_in)
            out_pids = flavors.pids_from_intrinsic_evol(n.target, nf_out)
            for out_pid, out_weight in out_pids.items():
                for in_pid, in_weight in in_pids.items():
                    # keep the outer index to the left as we're mulitplying from the right
                    value_tensor[
                        br.flavor_basis_pids.index(out_pid),
                        :,  # output momentum fraction
                        br.flavor_basis_pids.index(in_pid),
                        :,  # input momentum fraction
                    ] = out_weight * (op.value * in_weight)
                    error_tensor[
                        br.flavor_basis_pids.index(out_pid),
                        :,  # output momentum fraction
                        br.flavor_basis_pids.index(in_pid),
                        :,  # input momentum fraction
                    ] = out_weight * (op.error * in_weight)
        return value_tensor, error_tensor

    def __matmul__(self, other):
        """
        Multiply ``other`` to self.

        Parameters
        ----------
            other : PhysicalOperator
                second factor with a lower initial scale

        Returns
        -------
            p : PhysicalOperator
                self @ other
        """
        if not isinstance(other, PhysicalOperator):
            raise ValueError("Can only multiply with another PhysicalOperator")
        # prepare paths
        new_oms = {}
        for my_key, my_op in self.op_members.items():
            for other_key, other_op in other.op_members.items():
                # ops match?
                if my_key.input != other_key.target:
                    continue
                new_key = flavors.MemberName(my_key.target + "." + other_key.input)
                # new?
                if new_key not in new_oms:
                    new_oms[new_key] = my_op @ other_op
                else:  # add element
                    new_oms[new_key] += my_op @ other_op
        return self.__class__(new_oms, self.q2_final)
