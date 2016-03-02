from IPython import embed
def rt0_dofs_to_boundary_vertex_pairs(space):
    """Return permutation matrix that maps from dofs to grid insertion edge indices."""
    import numpy as np

    from scipy.sparse import coo_matrix

    grid = space.grid
    edge_count = space.global_dof_count

    dof_to_vertices_map = np.zeros((edge_count,2), dtype=np.int64)

    i_s = grid.leaf_view.index_set()

    for element in grid.leaf_view.entity_iterator(0):
        g_d = space.get_global_dofs(element)
        vs = [i_s.entity_index(v) for v in element.sub_entity_iterator(2)]
        for i,e in enumerate([(0,1),(0,2),(1,2)]):
            dof_to_vertices_map[g_d[i],0] = vs[e[0]]
            dof_to_vertices_map[g_d[i],1] = vs[e[1]]

    return dof_to_vertices_map


def n1curl_to_rt0_tangential_trace(fenics_space):
    import dolfin
    from .coupling import fenics_space_info
    from bempp.api import function_space, grid_from_element_data
    import numpy as np

    family, degree = fenics_space_info(fenics_space)
    if not (family == 'Nedelec 1st kind H(curl)' and degree == 1):
        raise ValueError("fenics_space must be an order 1 Nedelec 1st kind H(curl) space")

    mesh = fenics_space.mesh()

    fenics_dim = fenics_space.dim()

    bm = dolfin.BoundaryMesh(mesh, "exterior", False)
    bm_nodes = bm.entity_map(0).array().astype(np.int64)
    bm_coords = bm.coordinates()
    bm_cells = bm.cells()
    bempp_boundary_grid = grid_from_element_data(bm_coords.transpose(), bm_cells.transpose())

    # First get trace space 
    space = function_space(bempp_boundary_grid, "RT", 0)

    # Now compute the mapping from BEM++ dofs to FEniCS dofs
    # Overall plan:
    #   bempp_dofs <- bd_vertex_pairs <- all_vertex_pairs <- all_edges <- fenics_dofs

    # First the BEM++ dofs to the boundary edges
    #   bempp_dofs <- bd_vertex_pairs
    from scipy.sparse import coo_matrix

    dof_to_vertices_map = rt0_dofs_to_boundary_vertex_pairs(space)

    # Now the boundary triangle edges to the tetrahedron faces
    #   bd_vertex_pairs <- all_vertex_pairs
    # is bm_nodes

    #   all_vertex_pairs <- all_edges
    all_vertices_to_all_edges = {}
    for edge in dolfin.entities(mesh,1):
        i = edge.index()
        ent = edge.entities(0)
        all_vertices_to_all_edges[(max(ent),min(ent))] = i
    
    # Make matrix bempp_dofs <- all_edges
    bempp_dofs_to_all_edges_map = np.zeros(space.global_dof_count,dtype=np.int64)
    for bd_e,v in enumerate(dof_to_vertices_map):
        v2 = bm_nodes[v]
        v2 = (max(v2),min(v2))
        all_e = all_vertices_to_all_edges[v2]
        bempp_dofs_to_all_edges_map[bd_e] = all_e
        p = list(dolfin.vertices(mesh))[v2[0]].point()
        p = list(dolfin.vertices(mesh))[v2[1]].point()

    bempp_dofs_from_all_edges = coo_matrix((
        np.ones(space.global_dof_count), (np.arange(space.global_dof_count), bempp_dofs_to_all_edges_map)),
        shape=(space.global_dof_count, fenics_dim), dtype='float64').tocsc()

    # Finally the edges to FEniCS dofs
    #   all_edges <- fenics_dofs
    dofmap = fenics_space.dofmap()
    dof_to_edge_map = np.zeros(fenics_dim,dtype=np.int64)
    for cell in dolfin.cells(mesh):
        c_d = dofmap.cell_dofs(cell.index())
        c_e = cell.entities(1)
        for d,e in zip(c_d,c_e):
            dof_to_edge_map[d] = e

    all_edges_from_fenics_dofs = coo_matrix((
        np.ones(fenics_dim), (dof_to_edge_map, np.arange(fenics_dim))),
        shape=(fenics_dim, fenics_dim), dtype='float64').tocsc()

    # Get trace matrix by multiplication
    #   bempp_dofs <- bd_edges <- all_edges <- fenics_dofs
    trace_matrix = bempp_dofs_from_all_edges * all_edges_from_fenics_dofs

    # Now return everything
    return space, trace_matrix
