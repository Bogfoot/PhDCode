TITLE = "Laser beam and vendor lenses"
DESCRIPTION = """
It is possible to propagate gaussian beams using a LaserPath instead of an imaging
path.  The formalism makes use of the same matrices, but the GaussianBeam is
different from a ray: it is a complex radius of curvature (q), but all the complexity
is hidden in the GaussianBeam class (although you can access q, w, zo, etc..).
Note that any diffraction of the beam from edges of element is not considered
because the formalism does not allow it: a gaussian beam remains a gaussian beam
and therefore will not be clipped by lenses.
"""

from raytracing import *


def SagnacWaistEvolution(comments=None):
    # Demo #18: Laser beam and vendor lenses
    path = LaserPath()
    path.label = TITLE
    path.append(Space(d=50))
    path.append(Lens(f=250, diameter=25.4, label="Pump Lens"))
    path.append(Space(d=240))
    path.append(DielectricSlab(n=2.14, thickness=50, diameter=1, label="LiNbO3 PPLN"))
    path.append(Space(d=175))
    path.append(Lens(f=200, diameter=25.4, label="SPDC Lens"))
    path.append(Space(d=50))
    # (self, q: complex = None, w: float = None, R: float = inf, n: float = 1.0, wavelength=0.0006328, z=0)
    path.display(
        beams=[GaussianBeam(wavelength=780.24e-9, w=3.6, z=1)], comments=comments
    )


if __name__ == "__main__":
    SagnacWaistEvolution()
