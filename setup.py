from distutils.core import setup
REQUIRES = ['numpy', 'shapely', 'pyproj', 'tables', 'netCDF4', 'pyhdf']
setup(name='process_sat',
      version='0.2.82',

      install_requires = REQUIRES,

      description='Scripts for customized regridding of Level-2 data to Level-3 data',
      long_description=open('README.txt').read(),
      author='Jacob Oberman, Keith Maki',
      author_email='oberman@wisc.edu',
      packages=['process_sat'],
      url = 'http://github.com/Joberman/process_sat',
      download_url='http://github.com/Joberman/process_sat/downloads',

      classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Science/Research',
            'Natural Language :: English',
            'Programming Language :: Python'
      ]
)
      
