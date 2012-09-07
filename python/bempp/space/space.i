%{
#include "space/space.hpp"
#include <complex>
%}

%shared_ptr(Bempp::Space<float>);
%shared_ptr(Bempp::Space<double>);
%shared_ptr(Bempp::Space<std::complex<float> >);
%shared_ptr(Bempp::Space<std::complex<double> >);

// TODO
// %include "space_docstrings.i"

namespace Bempp 
{

template<typename BasisFunctionType> class Space;

%extend Space
{

// this function is only for internal use
%ignore basis;

// this function is only for internal use
%ignore shapeFunctionValue;

// to be wrapped later...
%ignore setElementVariant;

// to be wrapped later...
%ignore elementVariant;

%ignore getGlobalDofs;

%ignore global2localDofs;
%ignore flatLocal2localDofs;

// this function is only for internal use
%ignore getGlobalDofPositions;
%ignore getFlatLocalDofPositions;

%ignore dumpClusterIds;
}

BEMPP_EXTEND_CLASS_TEMPLATED_ON_BASIS(Space);

} // namespace Bempp

#define shared_ptr boost::shared_ptr
%include "space/space.hpp"
#undef shared_ptr

namespace Bempp
{
BEMPP_INSTANTIATE_SYMBOL_TEMPLATED_ON_BASIS(Space);
}

