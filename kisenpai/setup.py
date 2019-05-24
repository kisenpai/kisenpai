from distutils.core import setup

setup(
    name='kisenpai',
    packages=['kisenpai', 'kisenpai.feature', 'kisenpai.feature.extraction'],
    version='0.6',
    license='gpl-3.0',
    description='A simple framework for feature engineering',
    author='Pascal Zoleko',
    author_email='kisenpaideveloper@gmail.com',
    url='https://github.com/kisenpai/kisenpai',
    download_url='https://github.com/kisenpai/kisenpai/archive/0.5.tar.gz',
    keywords=['feature engineering', 'feature selection', 'feature extraction', 'feature transformation'],
    install_requires=[  # I get to this in a second
        'pandas',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
