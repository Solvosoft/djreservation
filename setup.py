from setuptools import setup, find_packages
import os

CLASSIFIERS = [
    'Environment :: Web Environment',
	'Framework :: Django',
	'Framework :: Django :: 1.10',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
	'Topic :: Software Development :: Libraries :: Python Modules',
	'Development Status :: 4 - Beta',
]

README = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))



setup(
    author='Luis Zarate',
    author_email='luis.zarate@solvosoft.com',
    name='django-reservation',
    version='0.2.9',
    description='Powerful and dinamic reservation system in django.',
    long_description=README,
    url='https://github.com/luisza/djreservation',
    license='GNU General Public License v3 (GPLv3)',
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    install_requires=[
        'setuptools',
        'django>=1.10',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False
)
