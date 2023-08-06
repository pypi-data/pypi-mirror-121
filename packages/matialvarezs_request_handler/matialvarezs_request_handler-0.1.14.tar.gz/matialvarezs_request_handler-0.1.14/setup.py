from distutils.core import setup
setup(
  name = 'matialvarezs_request_handler',
  packages = ['matialvarezs_request_handler'], # this must be the same as the name above
  version = '0.1.14',
  install_requires = [
    'requests',
    'simplejson',
    'tenacity',
  ],
  include_package_data = True,
  description = 'Request handler',
  author = 'Matias Alvarez Sabate',
  author_email = 'matialvarezs@gmail.com',  
  classifiers = [
    'Programming Language :: Python :: 3.5',
  ],
)