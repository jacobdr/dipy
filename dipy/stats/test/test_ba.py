import numpy as np
import nibabel as nib
from numpy.testing import assert_equal, run_module_suite
from dipy.data import get_fnames
from dipy.io.streamline import load_trk, save_trk
from dipy.tracking.streamline import Streamlines
from dipy.segment.metric import AveragePointwiseEuclideanMetric
import os
from dipy.io.image import load_nifti, save_nifti
from nibabel.tmpdirs import TemporaryDirectory
from dipy.stats.analysis import bundle_analysis
from dipy.testing import assert_true


def test_ba():

    with TemporaryDirectory() as dirpath:

        streams, hdr = nib.trackvis.read(get_fnames('fornix'))
        fornix = [s[0] for s in streams]

        f = Streamlines(fornix)

        mb = os.path.join(dirpath, "model_bundles")

        os.mkdir(mb)

        save_trk(os.path.join(mb, "temp.trk"),
                 f, affine=np.eye(4))

        rb = os.path.join(dirpath, "rec_bundles")
        os.mkdir(rb)

        save_trk(os.path.join(rb, "temp.trk"), f,
                 affine=np.eye(4))

        ob = os.path.join(dirpath, "org_bundles")
        os.mkdir(ob)

        save_trk(os.path.join(ob, "temp.trk"), f,
                 affine=np.eye(4))

        dt = os.path.join(dirpath, "dti_measures")
        os.mkdir(dt)

        fa = np.random.rand(255, 255, 255)

        save_nifti(os.path.join(dt, "fa.nii.gz"),
                   fa, affine=np.eye(4))

        out_dir = os.path.join(dirpath, "output")
        os.mkdir(out_dir)

        bundle_analysis(mb, rb, ob, dt, group="patient", subject="10001",
                        no_disks=100, out_dir=out_dir)

        assert_true(os.path.exists(os.path.join(out_dir, 'fa.h5')))


if __name__ == '__main__':

    run_module_suite()
