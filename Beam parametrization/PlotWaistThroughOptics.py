import plotly.graph_objects as go
import numpy as np


class GaussianBeam:
    def __init__(self, wavelength):
        self.wavelength = wavelength

    @staticmethod
    def Mfree(L):
        return [[1, L], [0, 1]]

    @staticmethod
    def Mlens(focus):
        return [[1, 0], [-1 / focus, 1]]

    @staticmethod
    def MRef(n1, n2):
        return [[1, 0], [0, n1 / n2]]

    def qNew(self, A, qOld):
        return (A[0][0] * qOld + A[0][1]) / (A[1][0] * qOld + A[1][1])

    def w(self, q):
        zR = np.imag(q)
        w0 = self.w0(zR)
        return w0 * np.sqrt(1 + (np.real(q) / np.imag(q)) ** 2)

    def w0(self, zR):
        return np.sqrt((self.wavelength * zR) / np.pi)

    def zR(self, w0):
        return (np.pi * w0**2) / self.wavelength


# Create the GaussianBeam instance
wavelength = 780e-9
beam = GaussianBeam(wavelength)

# Define the parameters
w0initial = 0.0006042744933010027
zwaist = 1.3271969822526328
zRayleighInitial = beam.zR(w0initial)

qOld = complex(0 - zwaist, zRayleighInitial)
print(qOld)
q1new = beam.qNew(beam.Mfree(0), qOld)
print(q1new)

z1mm = 150
z1 = z1mm * 1e-3
q2new = beam.qNew(beam.Mfree(z1), q1new)
z1plotmm = -2000
z1plot = z1plotmm * 1e-3
q2newplot = beam.qNew(beam.Mfree(z1plot - 0), q1new)
print(q2newplot)

focus1mm = 100
focus1 = focus1mm * 1e-3
q3new = beam.qNew(beam.Mlens(focus1), q2new)
print(q3new)

z2mm = 300
z2 = z2mm * 1e-3
q4new = beam.qNew(beam.Mfree(z2), q3new)
z2plotmm = z1mm
z2plot = z2plotmm * 1e-3
q4newplot = beam.qNew(beam.Mfree(z2plot - z1), q3new)
print(q4newplot)

# Generate the data
z = np.linspace(-150, z1mm + z2mm, 1000)
waist1 = [
    beam.w(beam.qNew(beam.Mfree(z_val), q1new)) * 1e3 for z_val in z if z_val <= z1mm
]
waist2 = [
    beam.w(beam.qNew(beam.Mfree(z_val - z1), q3new)) * 1e3
    for z_val in z
    if z_val >= z1mm
]

# Create the plot
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=z[: len(waist1)],
        y=waist1,
        mode="lines",
        name="First part of the plot (q2newplot)",
        line=dict(color="blue"),
    )
)

fig.add_trace(
    go.Scatter(
        x=z[len(waist1) :],
        y=waist2,
        mode="lines",
        name="Second part of the plot (q4newplot)",
        line=dict(color="red"),
    )
)

fig.update_layout(
    xaxis=dict(title="z (mm)"),
    yaxis=dict(title="waist (mm)"),
    title="Putting two plots together",
    showlegend=True,
    legend=dict(x=0.7, y=0.9),
    plot_bgcolor="white",
)

fig.add_shape(
    type="line",
    x0=-400,
    y0=-0.3,
    x1=0,
    y1=-0.3,
    line=dict(color="black", width=2, dash="dash"),
)

fig.add_shape(
    type="line",
    x0=z1mm,
    y0=-0.3,
    x1=z1mm + z2mm,
    y1=-0.3,
    line=dict(color="black", width=2, dash="dash"),
)

fig.add_annotation(
    text="start of the plot (q1new)", x=-400, y=1.8, ax=0, ay=0.75, arrowhead=2
)

fig.add_annotation(text="lens f1", x=z1mm, y=1.8, ax=z1mm, ay=0.8, arrowhead=2)

fig.add_annotation(text="z1", x=z1mm / 2, y=-0.3)

fig.add_annotation(text="z2", x=z1mm + z2mm / 2, y=-0.3)

fig.show()
