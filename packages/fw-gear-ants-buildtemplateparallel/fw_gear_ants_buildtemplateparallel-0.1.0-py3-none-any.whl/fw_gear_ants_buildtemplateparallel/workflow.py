import os
import shutil
import typing as t
from pathlib import Path

from flywheel_gear_toolkit.context import GearToolkitContext

from fw_gear_ants_buildtemplateparallel.interfaces import buildtemplateparallelEnhanced


def run_workflow(
    in_files: t.List[str],
    data_dir: t.Union[str, Path],
    context: GearToolkitContext,
    target: t.Union[str, Path],
    output_dir: t.Union[str, Path],
):
    """Return Nipype workflow to execute"""

    bpt = buildtemplateparallelEnhanced()
    bpt.inputs.parallelization = 2
    bpt.inputs.num_cores = os.cpu_count() - 1
    bpt.inputs.in_files = in_files
    bpt.inputs.use_first_as_target = False
    bpt.inputs.dimension = context.config["Image Dimension"]
    bpt.inputs.max_iterations = [
        int(el) for el in context.config["Max Iterations"].split("x")
    ]
    bpt.inputs.bias_field_correction = context.config["N4 Bias Field Correction"]
    bpt.inputs.rigid_body_registration = context.config["Rigid-body Registration"]
    bpt.inputs.similarity_metric = context.config["Similarity Metric"]
    bpt.inputs.transformation_model = context.config["Transformation Model"]

    if target:
        bpt.inputs.template = str(target)

    res = bpt.run(cwd=data_dir)

    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    final_template_filename = Path(res.outputs.final_template_file).name
    shutil.copy(res.outputs.final_template_file, output_dir / final_template_filename)
