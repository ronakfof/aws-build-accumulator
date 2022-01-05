#!/bin/sh
#
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

LITANI=${LITANI:-litani}

if [ "$1" != "--no-standalone" ]; then
  "${LITANI}" init --project-name "project-1"
fi


# 3 parallel jobs, plus a final one that depends on them


"${LITANI}" add-job \
  --command ">&2 echo foo" \
  --pipeline qux \
  --ci-stage build \
  --phony-outputs foo

"${LITANI}" add-job \
  --command ">&2 echo bar" \
  --pipeline qux \
  --ci-stage build \
  --phony-outputs bar

"${LITANI}" add-job \
  --command ">&2 echo baz" \
  --pipeline qux \
  --ci-stage build \
  --phony-outputs baz

"${LITANI}" add-job \
  --command "sleep 1 && >&2 echo Complete" \
  --pipeline qux \
  --ci-stage build \
  --inputs foo bar baz

if [ "$1" != "--no-standalone" ]; then
  "${LITANI}" run-build
fi
