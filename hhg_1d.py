import math
import numpy

# definitions
l0 = 2.0 * numpy.pi
t0 = l0
fwhm0 = 11.0 * t0
th0 = numpy.pi / 4.0    # laser-target angle
Lsim = 100.0 * l0
# total simulation time : 20.5 + 20.5 + 25 = 66
Tsim = 150.0 * t0
resx = 2048.0
# dt = 0.9 dx
# try other numbers : instabilities vs accuracy vs speed
rest = resx / 0.90
gm = 1./numpy.cos(th0)
# plasma slab : C6+ e-
# max. constant density
ne_0 = 30.0
nC_0 = 5.0
# max. preplasma density
ne_max = 30.0*(gm**3)
nC_max = 30.0*(gm**3)/6.
# number of macro-particles per cell
# try other numbers : instabilities vs accuracy vs speed
mppc = 150

def n_e(x):
    x1 = x / l0
    if x1<50.0:
        return ne_max*numpy.exp( (x1-50.0)/0.01) 
    else :
        return ne_max
def n_C(x):
    x1 = x / l0
    if x1<50.0:
        return nC_max*numpy.exp( (x1-50.0)/0.01) 
    else:
        return nC_max
Main(
    geometry = '1Dcartesian',
    
    interpolation_order = 4 ,
    
    cell_length = [l0 / resx],
    grid_length  = [Lsim],
    
    # try other numbers for speed-up
    number_of_patches = [256],
    
    timestep = t0 / rest,
    simulation_time = Tsim,
     
    EM_boundary_conditions = [ ['silver-muller'] ],
     
    print_every = 2000,
    random_seed = smilei_mpi_rank,
    #clrw = 1
)

Species(
    name = 'C_on',
    position_initialization = 'regular',
    momentum_initialization = 'cold',
    particles_per_cell = mppc,
    mass = 22032.0,
    charge = 6.0,
    number_density = n_C,
    time_frozen = 6.0 * t0,
    mean_velocity = [0.0, -numpy.sin(th0), 0.0],
    temperature = [0.0],
    boundary_conditions = [
        ['remove', 'remove'],
    ],
)

Species(
    name = 'e_on',
    position_initialization = 'regular',
    momentum_initialization = 'cold',
    particles_per_cell = mppc,
    mass = 1.0,
    charge = -1.0,
    number_density = n_e,
    time_frozen = 6.0 * t0,
    mean_velocity = [0.0, -numpy.sin(th0), 0.0],
    temperature = [0.0],
    boundary_conditions = [
        ['remove', 'remove'],
    ],
)

# laser profile : for later use, not used now
def t_prof0(t):
    t_ = t / fwhm0
    if t_ > 2.0:
        return 0.0
    else:
        return numpy.sin(0.5 * t_ * numpy.pi)

a0 = 4.2
Laser(
    box_side       = 'xmin',
    omega          = 1.0,
    time_envelope = tsin2plateau(start = 0.0, fwhm = fwhm0, plateau = None, slope1 = fwhm0, slope2 = fwhm0),
    space_envelope = [0.0, a0],
    phase          = [0.0, numpy.pi],
    delay_phase    = [0.0, -numpy.pi]
)


# t0 = 1138 steps
# data dump every cycle, t > 20
from numpy import s_

# electron density 21 < t < 45, 16 < x < 30
# data dump every 1/8 cycle
'''
DiagFields(
    every = [rest*0, rest*150, 200],
    flush_every = rest*2,
    fields = ['Rho_e_on'],
)
'''
DiagProbe(
    every = [rest*1, rest*150, 1],
    flush_every = rest*2,
    origin = [10.0 * l0],
    fields = ['Ey']
)

