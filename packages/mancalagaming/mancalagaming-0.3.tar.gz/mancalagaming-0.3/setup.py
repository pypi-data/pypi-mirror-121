from setuptools import setup, find_packages

setup(name='mancalagaming',
      version='0.3',
      url='https://github.com/alecsey-m-sorokin',
      license='AMS',
      author='Alecsey.M.Sorokin',
      author_email='alecsey.m.sorokin@gmail.com',
      description='base mancala functions',
      # packages=['mancala-slotx'],
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      # long_description_content_type=text,
      zip_safe=False)
