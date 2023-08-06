from setuptools import setup

with open('requirements.txt') as f:
    required_packages = f.read().splitlines()

setup(
   name='forecasting-mle-decathlon',
   version='0.1.1',
   author='Rugery Pierrick',
   author_email='rugery.pierrick@fake.com',
   packages=['forecasting_mle_decathlon'],
   description='Package to forecast sales',
   install_requires=required_packages,
)
