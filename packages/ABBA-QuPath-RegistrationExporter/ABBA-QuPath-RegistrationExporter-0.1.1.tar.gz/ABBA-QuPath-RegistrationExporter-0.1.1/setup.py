from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

with open('README.md') as f:
    long_description = f.read()

setup(
    name='ABBA-QuPath-RegistrationExporter',
    version='0.1.1',
    packages=find_packages(),
    url='',
    license='MIT',
    author='Nicholas A. Del Grosso',
    author_email='delgrosso.nick@gmail.com',
    description='A QuPath-Abba Registration Exporter Application for Mouse Sections',
    long_description=long_description,
    install_requires=requirements,
    entry_points={'console_scripts':[
        "regexport=regexport.app:main"
    ]}
)
