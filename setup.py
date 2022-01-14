from setuptools import setup


def descriptions():
    with open('README.md') as fh:
        ret = fh.read()
        first = ret.split('\n', 1)[0].replace('#', '')
        return first, ret


def version():
    with open('octodns_cloudns/__init__.py') as fh:
        for line in fh:
            if line.startswith('__VERSION__'):
                return line.split("'")[1]


description, long_description = descriptions()

setup(
    author='Ingo Struck',
    author_email='git@ingostruck.de',
    description=description,
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    name='octodns-cloudns',
    packages=('octodns_cloudns',),
    python_requires='>=3.6',
    install_requires=(
        'octodns>=0.9.14',
        ('git+https://github.com/istr/cloudns_api.git@'
         '5c6fa35f9c4048aba741df2aa84ae91c458573ad#egg=cloudns_api')
    ),
    url='https://github.com/octodns/octodns-cloudns',
    version=version(),
    tests_require=(
        'pytest',
        'pytest-network'
    ),
)
