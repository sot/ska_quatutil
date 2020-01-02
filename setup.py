# Licensed under a 3-clause BSD style license - see LICENSE.rst
from setuptools import setup

from Ska.quatutil import __version__

try:
    from testr.setup_helper import cmdclass
except ImportError:
    cmdclass = {}

setup(name='Ska.quatutil',
      author='Tom Aldcroft',
      description='ACA quaternion utilities',
      author_email='taldcroft@cfa.harvard.edu',
      url='http://cxc.harvard.edu/mta/ASPECT/tool_doc/pydocs/Ska.quatutil.html',
      version=__version__,
      zip_safe=False,
      packages=['Ska', 'Ska.quatutil', 'Ska.quatutil.tests'],
      tests_require=['pytest'],
      cmdclass=cmdclass,
      )
