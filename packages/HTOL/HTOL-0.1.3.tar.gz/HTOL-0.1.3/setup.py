from setuptools import setup

setup(name='HTOL',
      version='0.1.3',
      description='HTOL package',
      url='https://github.imec.be/vsever71/HTOL',
      author='Koen Van Sever',
      author_email='koen.vansever@imec.be',
      packages=['HTOL', 'HTOL.analysis', 'HTOL.tool'],
      zip_safe=False,
      include_package_data=True)