from setuptools import setup, find_packages


setup(
    name='example_praveen',
    version='0.1',
    license='MIT',
    author="Praveen Example",
    author_email='email@example.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    keywords='example project',
    install_requires=[
        'scikit-learn',
    ],

)
