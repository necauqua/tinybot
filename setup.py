from setuptools import setup

version = '1.0.0'

setup(name='tinybot',
      packages=['tinybot'],
      version=version,
      description='Very simple yet flexible Telegram Bot API',
      long_description=open('readme.markdown').read(),
      long_description_content_type='text/markdown',
      author='Anton Bulakh',
      author_email='necauqua@gmail.com',
      url='http://github.com/necauqua/tinybot',
      download_url='https://github.com/necauqua/tinybot/archive/v' + version + '.tar.gz',
      keywords=['telegram', 'bot', 'api'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Topic :: Communications :: Chat',
          'Topic :: Utilities'
      ],
      license='MIT',
      install_requires=['requests'],
      zip_safe=False,
      include_package_data=True)
