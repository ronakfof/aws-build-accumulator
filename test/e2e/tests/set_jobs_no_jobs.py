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

import json
import logging
import sys


SLOW = False
PHONY_ADD_JOBS = True


def get_init_args():
    return {
        "kwargs": {
            "project": "foo",
        }
    }


def get_jobs():
    return []


def get_set_jobs_args():
    jobs = [{
            "command": "echo foo",
            "pipeline_name": "foo",
            "ci_stage": "build",
    }]
    return {
        "kwargs": {
            "from_string": json.dumps(jobs)
        }
    }


def get_run_build_args():
    return {}


def check_run(run):
    job = run["pipelines"][0]["ci_stages"][0]["jobs"][0]
    return job["stdout"][0].strip() == "foo"
