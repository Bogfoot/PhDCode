TITLE = "Laser beam and vendor lenses"

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
