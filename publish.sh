# You can find the token to publish to pypi here 
# https://eu-west-1.console.aws.amazon.com/systems-manager/parameters/pypi-m2m-token/description?region=eu-west-1&tab=Table#list_parameter_filters=Name:Contains:py
# run `PIP_AUDIOSTACK_TOKEN=<<token>>` before executing this script

function deploy {
    rm -rf audiostack.egg-info build dist
    pip3 install twine wheel
    python3 setup.py sdist bdist_wheel
    echo '============'
    echo 'In order to obtain the username/pass; contact Core team devs'
    echo '%%%%%%%%%%%%'
    python3 -m twine upload dist/*
}

while true; do
    read -p "Do you wish to publish a new version $(sed -n '6p' < audiostack/__init__.py | cut -d '"' -f 2) to PyPI? " yn
    case $yn in
        [Yy]* ) deploy; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
