from setuptools import setup
import os


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


extra_files = package_files('simple_NER')

setup(
    name='simple_NER',
    version='0.8.0',
    packages=['simple_NER', 'simple_NER.rules', 'simple_NER.annotators',
              'simple_NER.annotators.remote', 'simple_NER.utils',
              'simple_NER.keywords'],
    url='https://github.com/OpenJarbas/simple_NER',
    package_data={'': extra_files},
    include_package_data=True,
    license='MIT',
    author='jarbasAI',
    install_requires=["simplematch", "nltk", "quantulum3", "requests",
                      "lingua_nostra>=0.4.2", "RAKEkeywords>=0.2.0"],
    author_email='jarbasai@mailfence.com',
    description='rule based NER'
)
