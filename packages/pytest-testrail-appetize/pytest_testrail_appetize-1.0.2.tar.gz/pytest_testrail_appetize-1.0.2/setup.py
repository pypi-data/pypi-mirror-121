from setuptools import setup


def read_file(fname):
    with open(fname) as f:
        return f.read()


setup(
    name='pytest_testrail_appetize',
    description='pytest plugin for creating TestRail runs and adding results',
    long_description=read_file('README.rst'),
    version='1.0.2',
    author='Appetize',
    author_email='chris.williams@appetize.com',
    download_url='https://github.com/AppetizeAutomation/pytest-testrail/archive/refs/tags/v1.0.2.tar.gz',
    url='https://github.com/AppetizeAutomation/pytest-testrail',
    packages=[
        'pytest_testrail_appetize',
    ],
    package_dir={'pytest_testrail_appetize': 'pytest_testrail_appetize'},
    install_requires=[
        'pytest>=3.6',
        'requests>=2.20.0',
    ],
    include_package_data=True,
    entry_points={'pytest11': ['pytest-testrail-appetize = pytest_testrail_appetize.conftest']},
)
