import sys

if sys.version_info < (3, 0):
    sys.exit(
        ("This doesn't support python 2,"
         " it doesn't support {0}").format(sys.version))

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()

setup(name='neurotic',
      version='2018.10.27',
      description=("Code for studying neural networks."),
      author="russell",
      platforms=['linux'],
      url='https://github.com/necromuralist/In-Too-Deep',
      author_email="cloisteredmonkey.jmark@slmail.me",
      packages=find_packages(),
      )
