from distutils.core import setup

setup(
    name='greybot',
    version='0.0.1',
    packages=[''],
    url='github.com/plathrop/greybot',
    license='',
    author='Paul Lathrop',
    author_email='paul@tertiusfamily.net',
    description='Personal IRC bot.',
    entry_points = {
        'console_scripts': ['greybot=greybot.cli:main'],
    }
)
