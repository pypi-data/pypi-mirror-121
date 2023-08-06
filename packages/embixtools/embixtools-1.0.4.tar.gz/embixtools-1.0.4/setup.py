from setuptools import setup

setup(
    name = 'embixtools',
    version = '1.0.4',
    description = 'EMBIX tools',
    packages = ['embixtools'],
    install_requires = [
        'pytz', 
        'requests', 
        'oauthlib', 
        'requests_oauthlib',
        'pyyaml'
    ],
)