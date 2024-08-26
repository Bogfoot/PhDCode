import time
from ast import literal_eval as ltv

import numpy as np
import QuantumTomography as qlib
import traits
from mayavi import mlab
from mayavi.core.api import PipelineBase
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, SceneEditor
from traits.api import HasTraits, Instance, Range, on_trait_change
from traitsui.api import Group, Item, View


def base_ball(state, N=100, sigma=0.025, multi=5):
    "takes a vector of a state on the surface of the poincare sphere and makes a point cloud around it"
    "will need longer for high N, high sigma and xyz close to surface"
    if len(state.shape) < 2:
        state = qlib.toDensity(state)
    if all(np.isreal(qlib.get_stokes_parameters(state))):
        x, y, z = qlib.get_stokes_parameters(state).real[1:]
        pcloud = np.array(
            [
                np.random.normal(0, sigma, multi * N),
                np.random.normal(0, sigma, multi * N),
                np.random.normal(0, sigma, multi * N),
            ]
        )
        pcloud_shiftd = pcloud + np.array([[x, y, z]]).T
        pcloud_filtrd = np.array(
            [vec for vec in pcloud_shiftd.T if np.linalg.norm(vec) < 1]
        ).T
        if pcloud_filtrd.shape[1] > N:
            return pcloud_filtrd[:, :N]
        else:
            print("se en krog")
            return base_ball(state, N=N, sigma=sigma, multi=10 * multi)
    else:
        return base_ball(np.array([[1, 0j], [0, 1]]), N=N, sigma=1e-6)


def density_from_stokes(stokes_vec):
    dim = int(np.log(stokes_vec.shape[0]) / np.log(4))
    basis = qlib.generalized_pauli_basis(dim)
    return (1 / 2**dim) * np.einsum("i, ikl -> kl", stokes_vec, basis)


def rotate_muh_balls(
    pcloud, theta_q=0, theta_h=0, q=False, h=False, flip=False, cartesian_input=True
):
    if cartesian_input:
        dmats = np.array([density_from_stokes(np.r_[1, vec]) for vec in pcloud.T])
    elif len(pcloud.shape) == 2:
        dmats = np.array([pcloud])
    else:
        dmats = np.array(pcloud)

    if not q:
        QWP = np.eye(2)
    # this minus in the next row is to agree with bsaic calculations and Bedirs "known examples", in the end depends on how you orient the wp
    else:
        QWP = qlib.quarterWavePlate(-theta_q)
    if not h:
        HWP = np.eye(2)
    else:
        HWP = qlib.halfWavePlate(theta_h)
    if flip:
        U = HWP @ QWP
    else:
        U = QWP @ HWP

    return np.array(
        [qlib.get_stokes_parameters(U @ dmat @ U.conj().T) for dmat in dmats]
    )[:, 1:].real.T


class poincare3Dwithplates(HasTraits):
    QWP_angle = Range(-np.pi, np.pi, 0)
    HWP_angle = Range(-np.pi, np.pi, 0)
    flipper = traits.api.Bool(label=" QWP, then HWP", default_value=True)
    qwp_on = traits.api.Bool(label="qwp on", default_value=True)
    hwp_on = traits.api.Bool(label="hwp on", default_value=True)
    state = traits.api.String(
        "[1+0j, 0],[0,0]", label=" input state", auto_set=False, enter_set=True
    )
    out_state = traits.api.Str("[0+0j,0],[0,0]", label=" output state")
    scene = Instance(MlabSceneModel, ())
    start_plot, rot_plot = Instance(PipelineBase), Instance(PipelineBase)

    def __init__(self):
        # init and setup
        HasTraits.__init__(self)
        u, v = np.radians(np.linspace(0, 360, 90)), np.radians(np.linspace(0, 180, 90))
        zz = np.zeros_like(u)
        xs, ys, zs = (
            np.outer(np.cos(u), np.sin(v)),
            np.outer(np.sin(u), np.sin(v)),
            np.outer(np.ones_like(u), np.cos(v)),
        )
        self.scene.background = (1, 1, 1)
        self.scene.foreground = (0, 0, 0)

        # draw sphere
        self.scene.mlab.mesh(xs, ys, zs, color=(0.0, 0.5, 0.5), opacity=0.1)
        # axes
        self.scene.mlab.plot3d(
            [-1.2, 1.2], [0, 0], [0, 0], color=(0, 0, 0), tube_radius=0.005
        )
        self.scene.mlab.plot3d(
            [0, 0], [-1.2, 1.2], [0, 0], color=(0, 0, 0), tube_radius=0.005
        )
        self.scene.mlab.plot3d(
            [0, 0], [0, 0], [-1.2, 1.2], color=(0, 0, 0), tube_radius=0.005
        )
        # circumferences
        self.scene.mlab.plot3d(
            np.sin(u), np.cos(u), zz, color=(0, 0, 0), tube_radius=0.005
        )
        self.scene.mlab.plot3d(
            np.sin(u), zz, np.cos(u), color=(0, 0, 0), tube_radius=0.005
        )
        self.scene.mlab.plot3d(
            zz, np.sin(u), np.cos(u), color=(0, 0, 0), tube_radius=0.005
        )
        [
            self.scene.mlab.plot3d(
                np.cos(sub * np.pi / 6) * np.sin(u),
                np.cos(u),
                np.sin(sub * np.pi / 6) * np.sin(u),
                color=(0, 0, 0),
                tube_radius=0.0025,
            )
            for sub in [1, 2, 4, 5]
        ]
        # set start state
        self.pcloud = base_ball(np.array(ltv(self.state)), sigma=0.1, N=100)

    @on_trait_change("scene.activated")
    def annotate(self):
        # doesnt work in init for low level reason i suppose; also seems to not support the entire unicode, so if we wanted pretty labels, have to import pngs of text
        coords, labels = [
            (1.25, 0, 0),
            (0, 1.25, 0),
            (0, 0, 1.25),
            (-1.25, 0, 0),
            (0, -1.25, 0),
            (0, 0, -1.25),
        ], ["|D>", "|R>", "|H>", "|A>", "|L>", "|V>"]
        for coord, label in zip(coords, labels):
            self.scene.mlab.text3d(*coord, label, color=(0, 0, 0), scale=0.11)

    @on_trait_change("state,QWP_angle,HWP_angle,flipper,qwp_on,hwp_on,scene.activated")
    def update_plot(self):
        try:
            proxstate = np.array(ltv(self.state))
            if len(proxstate.shape) < 2:
                proxstate = qlib.toDensity(proxstate)
        except:
            proxstate = np.array([[0, 0 + 0j], [0, 0]])
            time.sleep(1)
            pass
        self.pcloud = base_ball(proxstate, sigma=0.1, N=100)
        rpcloud = rotate_muh_balls(
            self.pcloud,
            self.QWP_angle,
            self.HWP_angle,
            self.qwp_on,
            self.hwp_on,
            self.flipper,
        )
        prox_out = density_from_stokes(
            np.r_[
                1,
                rotate_muh_balls(
                    proxstate,
                    self.QWP_angle,
                    self.HWP_angle,
                    self.qwp_on,
                    self.hwp_on,
                    self.flipper,
                    cartesian_input=False,
                ).squeeze(),
            ]
        )
        prox_out = np.array2string(
            prox_out,
            precision=2,
            sign=" ",
            floatmode="fixed",
            suppress_small=True,
            separator=", ",
        )
        self.out_state = prox_out

        if self.start_plot is None:
            self.start_plot = self.scene.mlab.points3d(
                *self.pcloud, scale_factor=0.05, color=(1, 0, 0)
            )
        else:
            self.start_plot.mlab_source.trait_set(
                x=self.pcloud[0], y=self.pcloud[1], z=self.pcloud[2]
            )

        if self.rot_plot is None:
            self.rot_plot = self.scene.mlab.points3d(
                *rpcloud, scale_factor=0.05, color=(0, 1, 0)
            )
        else:
            self.rot_plot.mlab_source.trait_set(
                x=rpcloud[0], y=rpcloud[1], z=rpcloud[2]
            )

    view = View(
        Item(
            "scene",
            editor=SceneEditor(scene_class=MayaviScene),
            height=250,
            width=300,
            show_label=False,
        ),
        Group(
            Item(
                "QWP_angle",
                format_str="%.2f",
                editor_args={"low_label": "-π", "high_label": " π"},
            ),
            Item(
                "HWP_angle",
                format_str="%.2f",
                editor_args={"low_label": "-π", "high_label": " π"},
            ),
            "_",
        ),
        Group("flipper", "qwp_on", "hwp_on", "_", columns=1),
        Group(
            Item("state"),
            Item("out_state", style="readonly", width=0.50, padding=5),
            "_",
            columns=2,
        ),
        resizable=True,
    )


if __name__ == "__main__":
    my_model = poincare3Dwithplates()
    my_model.configure_traits()
