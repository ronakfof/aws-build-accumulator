# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.


import dataclasses
import json
import pathlib

import jinja2
import yaml

from lib import litani_report


def load_file(path, as_text=False):
    path = pathlib.Path(path)
    with open(path) as handle:
        if as_text:
            return handle.read()
        if path.suffix == ".json":
            return json.load(handle)
        if path.suffix == ".yaml":
            return yaml.safe_load(handle)
    raise UserWarning("Pass 'as_text' to this function to load a text file")


async def compare_runs(args):
    base_run_file = pathlib.Path(args.base_run).resolve()
    second_run_file = pathlib.Path(args.second_run).resolve()
    template_dir = pathlib.Path("templates")
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(template_dir)),
        autoescape=jinja2.select_autoescape(
            enabled_extensions=('html'),
            default_for_string=True))
    gnuplot = litani_report.Gnuplot()
    base_run = load_file(base_run_file)
    stage2_run = load_file(second_run_file)
    svgs = litani_report.get_comparison_svgs(base_run, stage2_run, env, gnuplot)
    report_templ = env.get_template("comparison_report.jinja.html")
    page = report_templ.render(
      base_run=base_run_file,
      stage2_run=second_run_file,
      svgs=svgs)
    with open("tmp/index.html", "w") as handle:
        print(page, file=handle)