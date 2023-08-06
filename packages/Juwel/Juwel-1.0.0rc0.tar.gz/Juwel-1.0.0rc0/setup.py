from setuptools import setup, find_packages

setup(
   name='Juwel',
   license='GNU',
   version='1.0.0.rc.0',
   description='Sidecar file generator',
   author='Marco Tenderra',
   author_email='tenderra.git@gmail.com',
   packages=find_packages(),
   install_requires=['tk', 'tkcalendar'],

   include_package_data=True,
   package_data={'Juwel': ['config/*.json', 'config/*.txt']},

   entry_points={
        'console_scripts': [
            'juwel=Juwel.main:main',
        ],
    },
)
