import numpy as np
from PySDM.physics import si, Formulae, coalescence_kernels, spectra
from pystrict import strict


@strict
class Settings:
    def __init__(self):
        self.formulae = Formulae()
        self.init_x_min = self.formulae.trivia.volume(radius=3.94 * si.micrometre)
        self.init_x_max = self.formulae.trivia.volume(radius=25 * si.micrometres)

        self.n_sd = 2 ** 13
        self.n_part = 239 / si.cm**3
        self.X0 = self.formulae.trivia.volume(radius=10 * si.micrometres)
        self.dv = 1e1 * si.metres**3  # note: 1e6 caused overflows on ThrustRTC (32 bit ints for multiplicities)
        self.norm_factor = self.n_part * self.dv
        self.rho = 1000 * si.kilogram / si.metre**3
        self.dt = 1 * si.seconds
        self.adaptive = False
        self.seed = 44
        self._steps = [200 * i for i in range(10)]
        self.kernel = coalescence_kernels.Geometric(collection_efficiency=1)
        self.spectrum = spectra.Exponential(norm_factor=self.norm_factor, scale=self.X0)

        # Note 220 instead of 200 for smoothing
        self.radius_bins_edges = np.logspace(np.log10(3.94 * si.um), np.log10(220 * si.um), num=100, endpoint=True)

    @property
    def output_steps(self):
        return [int(step / self.dt) for step in self._steps]

