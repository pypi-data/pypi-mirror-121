from setuptools import setup
setup(
  name = 'pycad',         # How you named your package folder (MyLib)
  packages = ['pycad'],   # Chose the same as "name"
  version = '0.0.0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'python lib raspberry',   # Give a short description about your library
  author = 'Airat Abdrakov',                   # Type in your name
  author_email = 'crackanddie@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/CADindustries/',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/CADindustries/',    # I explain this later on
  keywords = ['pycad', 'studicad', 'raspberrypi'],   # Keywords that define your package best
  install_requires=['numpy', 'pyserial'],
  include_package_data=True,
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)