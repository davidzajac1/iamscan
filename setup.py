from setuptools import setup, find_packages
from pathlib import Path
from iamscan import __version__

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="iamscan",
    version=__version__,
    author="David Zajac",
    author_email="davidzajac321@gmail.com",
    description='Checks code for needed AWS IAM Privileges',
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['PyYAML>=5'],
    keywords=['aws', 'python', 'bash', 'aws-cli', 'iam'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
        'console_scripts': [
            'iamscan = iamscan.__main__:main'
        ]
    }
)