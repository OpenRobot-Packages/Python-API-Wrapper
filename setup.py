from setuptools import setup

import re

requirements = []
with open('requirements.txt') as f:
  requirements = f.read().splitlines()

with open('openrobot/api_wrapper/__init__.py') as f:
    try:
        version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)
    except:
        raise RuntimeError('version not set')

readme = ''
with open('README.md') as f:
    readme = f.read()

packages = [
    'openrobot.api_wrapper'
]

setup(
    name='OpenRobot-API-Wrapper',
    author='OpenRobot',
    url='https://github.com/OpenRobot/Packages/tree/API-Wrapper',
    version=version,
    packages=packages,
    license='MIT',
    description='A API wrapper for https://api.openrobot.xyz/',
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.7',
    classifiers=[]
)