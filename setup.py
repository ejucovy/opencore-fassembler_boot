from setuptools import setup, find_packages

version = '0.3.1'

setup(name='opencore-fassembler_boot',
      version=version,
      description="Creates a setup for new OpenCore site deployments that use Fassembler",
      long_description=open('README.txt').read(),
      classifiers=[],
      keywords='',
      author='opencore-dev',
      author_email='opencore-dev@lists.coactivate.org',
      url='http://www.coactivate.org/projects/opencore',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        "Tempita",
        "setuptools",
        ],
      entry_points="""
      [console_scripts]
      new-opencore-site = fassembler_boot.newsite:main
      rebuild-opencore = fassembler_boot.newbuild:main
      """,
      )
      
