import sys
import fenics as fe
import ThermoMecaFractureSolver as mdl
from importMesh import readMesh


steel = mdl.Material(
    exp_data_folder = "data",
    exp_data_list = ["pcT"],
    Emod = 1e9,
    nu = 0.07,
    alpha = 1,
    Gc = 10,
    lsp = 0.001,
    eta0 = 1e5,
    tau = 0.05,
    pc0 = 350e6,
    Omega = 0.01,
    Mbp = 1,
    alpbp = 0.1,
    mbp = 2,
    betbp = 0.7,
    gambp = 0.7,
    Ak = 10e9,
    delta0 = 500
)

# import mesh, boundary markers and cell markers
mesh, boundaries, materials = readMesh("./Meshes/", "tpb.inp")

# define the boundary conditions with format: (domain_ID, ux, uy)
bcs = [ 
    [1, 0, 0],
    [2, "free", -0.005],
    [3, "free", 0]
]

# define the problem
pb = mdl.Problem(
    "TPB",
    mesh,
    materials,
    boundaries,
    { 0 : steel },
    bcs,
    dt_min = 0.001, 
    dt_max = 0.1, 
    dt_initial = 0.01,  
    fixed_dump_interval = 0.1,
    # adaptive_mesh_refinement_flag = 0,
    mechanical_flag = 1,
    plasticity_flag = 1,
    # phase_field_damage_flag = 1,
    copy_for_forensic_flag = 1
)

# launch the solver
pb.run_simulation()