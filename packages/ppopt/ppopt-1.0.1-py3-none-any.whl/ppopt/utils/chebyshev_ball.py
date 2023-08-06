import numpy
from typing import Iterable

from ..solver_interface.solver_interface import solve_milp, solve_lp
from ..utils.constraint_utilities import constraint_norm
from ..utils.general_utils import make_column


def chebyshev_ball(A: numpy.ndarray, b: numpy.ndarray, equality_constraints: Iterable[int] = None,
                   bin_vars: Iterable[int] = None, deterministic_solver='glpk'):
    """
    Chebyshev ball finds the largest ball inside of a polytope defined by Ax <= b
    This is solved by the following LP

    min{x,r} -r

    st:
            Ax + ||A_i||r <= b

            A_{eq}*x = b_{eq}

            r >=0

    :param A: LHS Constraint Matrix
    :param b: RHS Constraint column vector
    :param equality_constraints: indices of rows that have strict equality A[eq] @ x = b[eq]
    :param bin_vars: indices of binary variables
    :param deterministic_solver: The underlying Solver to use, eg. gurobi, ect
    :return: the SolverOutput object, None if infeasible
    """

    if bin_vars is None:
        bin_vars = []

    if equality_constraints is None:
        equality_constraints = []

    # shortcut for chebyshev ball of facet of 1D region
    # if A.shape == 1 and len(equality_constraints) == 1:
    #     x_star = b[equality_constraints[0]]
    #     is_feasible = numpy.all((A@x_star - b) <= 0)
    #     if is_feasible:
    #         return SolverOutput(0, numpy.array([x_star, [0]]), )
    #     else:
    #         return None

    c = numpy.zeros((A.shape[1] + 1, 1))
    c[A.shape[1]][0] = -1

    const_norm = constraint_norm(A)
    const_norm = make_column(
        [const_norm[i][0] if i not in equality_constraints else 0 for i in range(numpy.size(A, 0))])

    A_ball = numpy.block([[A, const_norm], [c.T]])

    b_ball = numpy.concatenate((b, numpy.zeros((1, 1))))

    if len(bin_vars) == 0:
        return solve_lp(c, A_ball, b_ball, equality_constraints, deterministic_solver=deterministic_solver)
    else:
        return solve_milp(c, A_ball, b_ball, equality_constraints, bin_vars, deterministic_solver=deterministic_solver)


# noinspection PyUnusedLocal
def chebyshev_ball_max(A: numpy.ndarray, b: numpy.ndarray, equality_constraints: Iterable[int] = None,
                       bin_vars: Iterable[int] = (), deterministic_solver='glpk'):
    """

    Chebyshev ball finds the smallest l-infinity ball the contains the polytope defined by Ax <= b. Where A has n hyper planes and d dimensions.

    This is solved by the following LP

    .. math::

        \min_{x_{c} ,r ,y_{j} ,u_{j}} \quad r


    st:
            A^Ty_{j} = e_{j}, \forall j \in {1, .., d}
            A^Tu_{j} = -e_{j}, \forall j \in {1, .., d}

            -x_c[j] + b.T@y_{j} \leq r
            x_c[j] + b.T@u_{j} \leq r

            r >=0
            y_{j} >= 0
            u_{j} >= 0

            r \in R
            y_{j} \in R^n
            u_{j} \in R^n
            x_c \in R^d

    Source: Simon Foucart's excellent book

    :param A: LHS Constraint Matrix
    :param b: RHS Constraint column vector
    :param equality_constraints: indices of rows that have strict equality A[eq] @ x = b[eq]
    :param bin_vars: indices of binary variables
    :param deterministic_solver: The underlying Solver to use, eg. gurobi, ect
    :return: the SolverOutput object, None if infeasible
    """
    pass
