from setuptools import setup

from setuptools import setup
import os

README = os.path.join(os.path.dirname(__file__), 'README.md')

setup(name='lahar-python',
      version='0.1.0',
      description='LAHAR API integration wrapper for python',
      long_description=open(README).read(),
      long_description_content_type="text/markdown",
      author="Vinícius Bôscoa",
      author_email="virb30@gmail.com",
      license="MIT",
      py_modules=['lahar'],
      zip_safe=False,
      platforms='any',
      include_package_data=True,
      install_requires=[
          'requests'
      ],
      python_requires=">=3.6",
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: Portuguese',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries',
      ],
      project_urls={
          'Bug Tracker': 'http://github.com/virb30/lahar-python/issues'
      },
      url='http://github.com/virb30/lahar-python/',)