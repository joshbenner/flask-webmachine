from setuptools import setup, find_packages


setup(
    name='flask_webmachine',
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(),

    description='Webmachine-style resource framework for Flask',
    author='Joshua Benner',
    author_email='josh@bennerweb.com',
    license='Apache',

    install_requires=[
        'six',
        'flask'
    ],
    extras_require={
        'test': [
            'pytest',
            'pytest-cov'
        ]
    }
)
