from setuptools import setup

setup(
    name='varify-client',
    version='0.0a1',
    packages=['varify-client'],
    description="an HTTP client and supporting utilities for the Varify API",
    entry_points={
        "console_scripts": ['fetchVCF = varify_client._fetchVCF:runCommandLine']
    },
    url='https://github.com/awenocur/varify_client',
    install_requires=["PyVCF"]
)