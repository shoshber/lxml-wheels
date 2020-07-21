#!/usr/bin/env bash
# Define custom utilities
# Test for OSX with [ -n "$IS_OSX" ]
#function pre_build {
#    if [ -n "$IS_OSX" ]; then
#        if [ ${MB_PYTHON_VERSION} == 2.6 ]; then
#            yes | pip uninstall pip
#            easy_install pip==1.2.1
#        fi
#    fi
#    pip --version
#}

function bdist_with_static_deps {
    local abs_wheelhouse=$1
    python setup.py clean
    make wheel_static
    cp dist/*.whl $abs_wheelhouse
}

function build_wheel {
    build_wheel_cmd "bdist_with_static_deps" $@
}

function run_tests {
    # Runs tests on installed distribution from an empty directory
    python --version
    python -c 'import sys; import lxml.etree, lxml.objectify'
}
