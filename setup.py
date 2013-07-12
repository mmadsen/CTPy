from distutils.core import setup

setup(name="CTPy",
      version="1.0.1",
      packages=['ctpy'],
      scripts=['simulations/neutral-kn-interactive.py'],
      author='Mark E. Madsen',
      author_email='mark@madsenlab.org',
      url='https://github.com/mmadsen/',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: POSIX',
          'Programming Language :: Python :: 2.7',
          'Topic :: Scientific/Engineering',
      ]
      )