from setuptools import setup

from Ska.quatutil import __version__

setup(name='Ska.quatutil',
      author = 'Tom Aldcroft',
      description='ACA quaternion utilities',
      author_email = 'aldcroft@head.cfa.harvard.edu',
      py_modules = ['Ska.quatutil'],
      url = 'http://cxc.harvard.edu/mta/ASPECT/tool_doc/pydocs/Ska.quatutil.html',
      version=__version__,
      zip_safe=False,
      packages=['Ska'],
      package_dir={'Ska' : 'Ska'},
      package_data={}
      )
