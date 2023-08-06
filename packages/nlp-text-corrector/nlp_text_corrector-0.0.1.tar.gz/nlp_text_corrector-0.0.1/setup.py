from setuptools import find_packages, setup
setup(
    name='nlp_text_corrector',
    packages=find_packages(include=['nlp_text_corrector']),
    version='0.0.1',
    description='IAMAI ASR Post Process Library',
    url='https://github.com/iAmPlus/nlp-text-corrector',
    author='Manoj Preveen',
    author_email='manoj.velusamy@iamplus.com',
    license='MIT',
    install_requires=[],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)