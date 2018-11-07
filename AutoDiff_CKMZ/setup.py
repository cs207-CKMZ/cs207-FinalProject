import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fh:
    requirements = fh.read().splitlines()

setuptools.setup(
        name='AutoDiff_CKMZ',
        version='0.0.1',
        author='CKMZ',
        description='Automatic Differentiation package',
        long_description=long_description,
        long_description_content_type='text/markdown',
        packages=setuptools.find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
        install_requires=requirements

    )
