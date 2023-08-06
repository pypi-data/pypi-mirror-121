from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='MotionArtifactRemoval',
    version='1.0.7',    
    description='Motion Artifact Removal',
    author='Jim Peterson, Abed Ghanbari',
    url='https://www.jax.org',
    author_email='jim.peterson@jax.org',
    license='BSD 2-clause',
    packages=find_packages(),
    install_requires=required,

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    include_package_data=True,
    package_data={'': ['ssUNET/weights/*.pth']},
)
