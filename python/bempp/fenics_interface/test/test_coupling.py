from unittest import TestCase
import bempp
import numpy as np

if bempp.HAVE_DOLFIN:

    class TestP1Coupling(TestCase):
        def test_dolfin_p1_identity_equals_bempp_p1_identity(self):

            import dolfin
            from bempp.fenics_interface import fenics_to_bempp_trace_data
            from bempp.fenics_interface import FenicsOperator

            mesh = dolfin.UnitCubeMesh(5, 5, 5)
            V = dolfin.FunctionSpace(mesh, "CG", 1)

            space, trace_matrix = fenics_to_bempp_trace_data(V)

            u = dolfin.TestFunction(V)
            v = dolfin.TrialFunction(V)
            a = dolfin.inner(u, v) * dolfin.ds
            fenics_mass = FenicsOperator(a).weak_form().sparse_operator
            actual = trace_matrix * fenics_mass * trace_matrix.transpose()

            from bempp.operators.boundary import sparse

            expected = sparse.identity(space, space, space).weak_form().sparse_operator
            diff = actual - expected
            self.assertAlmostEqual(np.max(np.abs(diff.data)), 0)


if __name__ == "__main__":
    from unittest import main

    main()
