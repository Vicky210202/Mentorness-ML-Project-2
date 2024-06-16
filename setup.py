from setuptools import find_packages, setup
from typing import List

e_dot = '-e .'

def get_requirements(file_path:str)->List[str]:
    '''This functions returns the list of requirements'''
    requirements = list()
    with open(file_path) as req_file:
        requirements = req_file.readlines()
        requirements = [reqmt.replace('\n', '') for reqmt in requirements]

        if e_dot in requirements:
            requirements.remove(e_dot)

    return requirements    

setup(
    name = 'Fastag Fraud Detection - Mentorness Internship',
    version = '1.0.0',
    author = 'Vignesh S',
    author_email = 'vivic210202@gmail.com',
    packages = find_packages(),
    install_requires = get_requirements('requirements.txt')
)
