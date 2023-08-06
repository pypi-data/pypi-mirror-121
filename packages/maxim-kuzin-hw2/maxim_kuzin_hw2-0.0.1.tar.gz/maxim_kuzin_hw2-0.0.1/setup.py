from setuptools import setup

setup(
    name='maxim_kuzin_hw2',
    version='0.0.1',    
    description='A example Python package',
    url='https://github.com/shuds13/pyexample',
    author='Maxim Kuzin',
    author_email='12345min@mail.ru',
    license='BSD 2-clause',
    packages=['maxim_kuzin_hw2'],
    install_requires=['numpy','matplotlib'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)