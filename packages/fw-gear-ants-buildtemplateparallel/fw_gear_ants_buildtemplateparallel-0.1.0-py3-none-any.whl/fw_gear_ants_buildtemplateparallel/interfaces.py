"""The interfaces module.

Redefining BuildTemplateParallel here because the NiPype implementation which is
in the legacy module has the following issues:
  1) missing the template input
  2) missing a few option for the transformation_model
"""
from nipype.interfaces.ants.legacy import (
    buildtemplateparallel,
    buildtemplateparallelInputSpec,
)
from nipype.interfaces.base import traits
from nipype.interfaces.base.traits_extension import File, InputMultiPath


class buildtemplateparallelEnhancedInputSpec(buildtemplateparallelInputSpec):

    template = InputMultiPath(
        File(exists=True),
        mandatory=False,
        argstr="-z %s",
        desc="Use this this volume as the target of all inputs. When not used, the "
        "script will create an unbiased starting point by averaging all inputs",
    )

    # redefining because buildtemplateparrallel does not support full paths
    in_files = traits.List(
        str,
        mandatory=True,
        desc="list of images to generate template from",
        argstr="%s",
        position=-1,
    )

    transformation_model = traits.Enum(
        "GR",
        "EL",
        "SY",
        "S2",
        "EX",
        "DD",
        "RI",
        "RA",
        argstr="-t %s",
        usedefault=True,
        desc=(
            "Type of transformation model used for registration "
            "(EL = elastic transformation model, SY = SyN with time, "
            "arbitrary number of time points, S2 =  SyN with time "
            "optimized for 2 time points, GR = greedy SyN, EX = "
            "exponential, DD = diffeomorphic demons style exponential "
            "mapping, RI = purely rigid, RA = Affine rigid)"
        ),
    )


class buildtemplateparallelEnhanced(buildtemplateparallel):

    input_spec = buildtemplateparallelEnhancedInputSpec
