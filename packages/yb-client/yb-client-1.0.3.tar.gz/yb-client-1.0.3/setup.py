from setuptools import setup

with open('README.md') as f:
    long_description = f.read()
  
setup(
  name = 'yb-client',
  version = '1.0.3',
  license = 'GNU General Public License v3.0',
  description = 'Yottab-Client is a command-line interface to interact with the Yottab server to create and manage workspaces and applications.',
  long_description = long_description,
  long_description_content_type = 'text/markdown',
  author = 'Yottab',
  author_email = 'admin@yottab.io',
  py_modules=['yb_client','yb_client.commands', 'yb_client.file', 'yb_client.api', 'yb_client.output'],
  keywords = ['yottab', 'yottab client', 'command-line'],
  url = 'https://github.com/yottab-io/yb-client',
  download_url = "https://github.com/yottab-io/yb-client/archive/refs/tags/v1.0.3.tar.gz",
  install_requires=[
    'Click',
    'tabulate',
    'requests'
  ],
  entry_points = {
    'console_scripts': ['yb=yb_client.commands:cli'],
  },
  classifiers = [
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',   
    'Topic :: Scientific/Engineering :: Human Machine Interfaces',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',   
    'Programming Language :: Python :: 3', 
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.8'
  ],
  
)