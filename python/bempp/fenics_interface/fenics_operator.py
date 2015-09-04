import dolfin as _dolfin
import numpy as _np

class FenicsOperator(object):

    def __init__(self,fenics_weak_form):

        self._fenics_weak_form = fenics_weak_form

    def weak_form(self):

        # Currently have to assemble using uBLAS
        # Therefore need to save current backend and restore
        # after assembly.

        from bempp.assembly.discrete_boundary_operator import SparseDiscreteBoundaryOperator
        
        backend = _dolfin.parameters['linear_algebra_backend']
        _dolfin.parameters['linear_algebra_backend'] = 'uBLAS'
        sparse_mat = _dolfin.assemble(self._fenics_weak_form).sparray()
        _dolfin.parameters['linear_algebra_backend'] = backend

        return SparseDiscreteBoundaryOperator(sparse_mat)
