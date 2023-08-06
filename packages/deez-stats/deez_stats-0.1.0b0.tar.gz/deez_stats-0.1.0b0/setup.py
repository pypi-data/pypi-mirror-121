import pathlib
from setuptools import setup


# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


setup(
    name='deez_stats',
    version='0.1.0-beta',
    author='Tom Brady',
    author_email='bradyte@gmail.com',
    description='Python bindings to access competitive league stats.',
    license='MIT',
    long_description=README,
    long_description_content_type="text/markdown",
    url='http://github.com/bradyte/deez_stats',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    packages=['deez_stats'],
    include_package_data=True,
    install_requires=['objectpath', 'yahoo_fantasy_api', 'yahoo_oauth'],
    python_requires='>=3'
)
