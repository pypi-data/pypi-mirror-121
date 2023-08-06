#!/bin/bash

function errexit(){
  echo "$@" >&2
  exit 1
}

SCRIPT=$(readlink -f "$0")
FOLDER=$(dirname "$SCRIPT")
VENV="${FOLDER}/py3venv"
cd "${FOLDER}" || errexit "FATAL BUG: script exists but parent directory doesn't."



function run(){
  if [ "$1" == "--append" ]; then
    local append=1
    shift
  else
    local append=0
  fi
  local action="$1"
  shift
  echo "ACTION: ${action}"
  echo "  RUN:  $*"
  if [ "$append" == "1" ]; then
    touch ./op.log
    echo "*** RUN:  $*" >> ./op.log
    "$@" >> ./op.log 2>&1
  else
    "$@" &> ./op.log
  fi
  local rc=$?
  pwd

  if [ "$rc" == 0 ]; then
    echo "  RESULT: success"
  else
    echo "  RESULT: error (RC=$rc)"
    sed 's/^/  | /' ./op.log
    errexit "Error: action '$action' failed."
  fi
}

function usage(){
  cat <<EOF
Usage:
    ops.sh COMMAND [arg [arg [...]]]

Where COMMAND is one of:
  build-venv   - Build the development environment.
  rebuild-venv - Delete and reuild the development environment.
  test                - Run tox testing (Note 1).
  test-envs           - Run tox testing on specified environments (Note 2).
  test-py-all         - Run tox testing on python unit test environments (Note 1).
  test-style-quality  - Run tox testing on style and quality test environments (Note 1).
  test-coverage       - Run tox testing on coverage test environment (Note 1).
  unit-test           - Run unit testing directly in current environment (Note 3).
  coverage            - Generate code coverage data (Note 3).
  docs                - Generate documentation (Note 4,5)
  quality             - Run code quality analysis (Note 4,6)
  style               - Run code style analysis and tests (Note 6)
  -h|--help|help      - Display this help and exit.

Notes:
1) additional args passed directly to tox
2) additional args specify desired tox test environments to run
3) additional args passed directly to pytest
4) automatically generates coverage data first
5) additional args passed directly to setup.py
6) extra args ignored.
EOF
  exit 0
}

function activate_venv(){
  # shellcheck disable=SC1091
  if ! . "${VENV}/bin/activate"; then
    errexit "Error: can't activate python3 environment."
  fi
}
function has_untracked_files(){
  [ "$(git status --porcelain 2>/dev/null | grep -Ec '^(M| [MD]|\?\?|u) ')" != 0 ]
}
function require_working_directory_clean(){
  if has_untracked_files; then
    echo "Working directory is not clean." 1>&2
    git status
    false
  else
    true
  fi
}
function fix_wheel(){
  # shellcheck disable=SC2155
  local wheel=$( readlink -f "${1}")
  if [ ! -f "$wheel" ]; then
    echo "Wheel file $wheel does not exist!" 1>&2
    return 1
  fi
  
  # shellcheck disable=SC2155
  local wheel_base=$(basename "$wheel")
  local zip_base="${wheel_base/.whl/.zip}"
  # shellcheck disable=SC2155
  local workdir=$(mktemp -d)
  local zipfile="${workdir}/${zip_base}"
  echo "* Copying wheel to temporary directory."
  if ! cp -v "${wheel}" "${zipfile}"; then
    echo "Unable to copy wheel file." 1>&2
    return 1
  fi
  echo "* Entering temporary directory."
  if ! pushd "${workdir}" &> /dev/null; then
    echo "Unable to enter temporary directory." 1>&2
    return 1
  fi
  echo "* Extracting wheel zip file."
  if ! unzip "${zipfile}"; then
    echo "Unable to extract wheel contents." 1>&2
    # shellcheck disable=SC2164
    popd
    return 1
  fi
  echo "* Finding and updating nspkg.pth files."
  if ! find . -iname '*-nspkg.pth' -exec sed -i 's/;/\n/g' '{}' \;; then
    echo "Can not modify nspkg.pth files." 1>&2
    # shellcheck disable=SC2164
    popd
    return 1
  fi
  echo "* Removing the copied wheel archive."
  if ! rm "${zipfile}"; then
    echo "Unable to remove no-longer-needed zipfile." 1>&2
    # shellcheck disable=SC2164
    popd
    return 1
  fi
  echo "* Zipping up fixed wheel contents."
  if ! zip -r "${zip_base}" .; then
    echo "Unable to archive fixed wheel contents." 1>&2
    # shellcheck disable=SC2164
    popd
    return 1
  fi
  echo "* Copying fixed wheel zip file back to it's original location."
  if ! cp -v "${zipfile}" "${wheel}" ; then
    echo "Unable to copy the fixed wheel to it's original location." 1>&2
    # shellcheck disable=SC2164
    popd
    return 1
  fi
  echo "* Removing the working directory."
  if ! rm -rfv "${workdir}"; then
    echo "Unable to remove temporary directory." 1>&2
    # shellcheck disable=SC2164
    popd
    return 1
  fi

  # shellcheck disable=SC2164
  popd
  return 0
}

function do_action(){
  case "$1" in
    fix-wheel)
      shift
      run "Fix wheel NSPKG.pth format." fix_wheel "$@"
    ;;
    fix-wheels)
      for filename in dist/*.whl; do
        do_action fix-wheel "$filename"
      done
    ;;
    rebuild-venv)
      local interpreter=${2-python3}
      run "Delete python3 environment." rm -rf "${VENV}"
      "${SCRIPT}" build-venv "${interpreter}"
    ;;

    build-venv)
      local interpreter=${2-python3}
      if [ ! -d "${VENV}" ]; then
        run "Create python3 environment" "${interpreter}" -m venv "${VENV}"
      fi
      activate_venv
      run "Upgrade python3 pip"                pip install --upgrade pip
      run "Install development requirements"   pip install -r "requirements-dev.txt"
      run "Install runtime requirements"       pip install -r "requirements.txt"
      run "Install python project"             python "${FOLDER}/setup.py" develop
    ;;

    test)
      shift
      tox -vv "$@"
    ;;

    test-envs)
      shift
      envs="$*"
      # shellcheck disable=SC2086
      tox -vv -e ${envs// /,}
    ;;

    test-py-all)
      shift
      tox -vv "$@" -e py36,py37,py38,py39
    ;;

    test-style-quality)
      shift
      tox -vv "$@" -e style,quality
    ;;

    test-coverage)
      shift
      tox -vv "$@" -e coverage
    ;;

    unit-test)
      shift
      activate_venv
      export PYTHONUNBUFFERED=yes
      pytest -vv --basetemp="${FOLDER}/tests" "$@"
    ;;

    coverage)
      shift
      activate_venv
      run "Generate Coverage Data" pytest --cov-config=./.coveragerc --cov=pt.ptutils --cov-report html -vv --basetemp="${FOLDER}/src" "$@"
    ;;

    docs)
      shift
      if [ "$1" == "--no-coverage" ]; then
        shift
      else
        do_action coverage
      fi
      run "Clean autogenerated doc stubs" rm -rf "${FOLDER}/docs/_autosummary"
      run "Clean previously built docs" rm -rf "${FOLDER}/docs/build"
      run "Build Documentation" python3 setup.py build_sphinx "$@"
    ;;

    quality)
      shift
      if [ "$1" == "--no-coverage" ]; then
        shift
      else
        do_action coverage
      fi
      rm ./op.log
      touch ./op.log
      run --append "Compute Cyclomatic Complexity (CC)" radon cc -s -i '__pending*' ./src
      run --append "Compute Maintainability Index (MI)" radon mi -s -i '__pending*' ./src
      run --append "Compute raw statistics (RAW)" radon raw -s -i '__pending*' ./src
      run --append "Analyze Code Quality" xenon -b C -m A -a A -i '__pending*' ./src
    ;;

    style)
      shift
      activate_venv
      export PYTHONUNBUFFERED=yes
      run "Check Source code Style Compliance" flake8 --max-line-length=120 --ignore=E201,E202,E401,E221,E241,E251,W504 --exclude '__pending*' src
    ;;
    -h|--help|help)
      usage
    ;;

    prerelease)
      run "Ensure working directory is clean." require_working_directory_clean
      do_action unit-test
      do_action coverage
      do_action quality --no-coverage
      do_action style
      do_action docs --no-coverage
    ;;

    release-major)
      do_action prerelease
      run "Increment the version number (major)." bumpversion major
      run "Push changes" git push
      run "Push tags"    git push --tags
    ;;

    release-minor)
      do_action prerelease
      run "Increment the version number (minor)." bumpversion minor
      run "Push changes" git push
      run "Push tags"    git push --tags
    ;;

    release-patch)
      do_action prerelease
      run "Increment the version number (patch)." bumpversion patch
      run "Push changes" git push
      run "Push tags"    git push --tags
    ;;

    *)
      errexit "Unknown action '$1'. Try '$0 --help' for more information."
    ;;
  esac
}

do_action "$@"
