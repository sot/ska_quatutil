from setuptools import setup
setup(name='Ska.quatutil',
      author = 'Tom Aldcroft',
      description='ACA quaternion utilities',
      author_email = 'taldcroft@cfa.harvard.edu',
      py_modules = ['Ska.quatutil'],
      url = 'http://cxc.harvard.edu/mta/ASPECT/tool_doc/pydocs/Ska.quatutil.html',
      test_suite = 'nose.collector',
      version='0.01',
      zip_safe=False,
      packages=['Ska'],
      package_dir={'Ska' : 'Ska'},
      package_data={}
      )
