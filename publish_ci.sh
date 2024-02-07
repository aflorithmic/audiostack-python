# You can find the token to publish to pypi here 
# https://eu-west-1.console.aws.amazon.com/systems-manager/parameters/pypi-m2m-token/description?region=eu-west-1&tab=Table#list_parameter_filters=Name:Contains:py
# run `PIP_AUDIOSTACK_TOKEN=<<token>>` before executing this script

rm -rf audiostack.egg-info build dist
pip3 install twine wheel
python3 setup.py sdist bdist_wheel
echo '============'
echo 'In order to obtain the username/pass; contact Core team devs'
echo '%%%%%%%%%%%%'
python3 -m twine upload dist/* -u __token__ -p $PIP_AUDIOSTACK_TOKEN
