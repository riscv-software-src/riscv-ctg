# See LICENSE.incore for details

"""The setup script."""

from setuptools import setup, find_packages

# Base directory of package
here = os.path.abspath(os.path.dirname(__file__))


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()
def read_requires():
    with open(os.path.join(here, "riscv_ctg/requirements.txt"),"r") as reqfile:
        return reqfile.read().splitlines()

#Long Description
with open("README.rst", "r") as fh:
    readme = fh.read()

setup_requirements = [ ]

test_requirements = [ ]

setup(
    name='riscv_ctg',
    version='0.1.0',
    description="RISC-V Compliance Test Generator",
    long_description=readme + '\n\n',
    classifiers=[
          "Programming Language :: Python :: 3.6",
          "License :: OSI Approved :: BSD License",
          "Development Status :: 4 - Beta"
    ],
    url='https://gitlab.com/incoresemi/riscv-compliance/riscv_ctg//riscv_ctg',
    author="InCore Semiconductors Pvt. Ltd.",
    author_email='incorebot@gmail.com',
    license="MIT license",
    packages=find_packages(),
    package_dir={'riscv_ctg': 'riscv_ctg'},
    package_data={
        riscv_ctg: [
            'requirements.txt'
            ]
        },
    install_requires=read_requires(),
    python_requires='>=3.6.0',
    entry_points={
        'console_scripts': [
            'riscv_ctg=riscv_ctg.main:riscv_ctg',
        ],
    },
    include_package_data=True,
    keywords='riscv_ctg',
    test_suite='tests',
    tests_require=test_requirements,
    zip_safe=False,
)
