function deploy {
    rm -rf audiostack.egg-info build dist
    pip3 install twine wheel
    python3 setup.py sdist bdist_wheel
    echo '============'
    echo 'In order to obtain the username/pass; contact Core team devs'
    echo '%%%%%%%%%%%%'
    python3 -m twine upload dist/*
    python3 -m twine upload dist/* -u __token__ -p $PIP_AUDIOSTACK_TOKEN

}