from setuptools import find_packages, setup

VERSION = "0.0.3"

def readme():
    with open("README.rst", encoding="utf-8") as f:
        return f.read()

setup(
    name='nlp_text_corrector',
    packages=find_packages(include=['nlp_text_corrector']),
    version=VERSION,
    description='IAMAI ASR Post Process Library',
    long_description=readme(),
    url='https://github.com/iAmPlus/nlp-text-corrector',
    author='Manoj Preveen',
    author_email='manoj.velusamy@iamplus.com',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)