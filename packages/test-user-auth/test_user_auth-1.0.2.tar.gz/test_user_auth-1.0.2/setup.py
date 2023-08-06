from setuptools import setup, find_packages
import os

here=os.path.dirname(os.path.abspath(__file__))

# Get the long description from the README file
long_description = (os.path.join(here, 'README.md'))

setup(

    name='test_user_auth',  # Required
    version='1.0.2',  # Required
    description='User authentication service',  # Optional
    long_description=long_description,  # Optional
    url='https://github.com/michal-nemec/junior_python_dev_oleksandr_leiko/',  # Optional
    author='O.L.',  
    author_email='leiko.oleksandr@gmail.com',  # Optional
    classifiers=[  # Optional

        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    # Required
    packages=find_packages(include=['IdentityService', 'test']),
    python_requires='>=3.6',
    py_modules=["main"],
    install_requires=['pandas','pytest'],  # Optional
    entry_points={  # Optional
        'console_scripts': ['run=main']
        },
   
)