from setuptools import setup
setup(
  name = 'stopfortr',         # How you named your package folder (MyLib)
  packages = ['stopfortr'],   # Chose the same as "name"
  version = '0.6',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Stopwords for Turkish Language',   # Give a short description about your library
  author = 'Taylan Gezici',                   # Type in your name
  author_email = 'taylangezici@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/taylangezici/stpfortr',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/taylangezici/stopfortr/archive/refs/tags/v0.6.tar.gz', 
  keywords = ['none'],   # Keywords that define your package best
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
