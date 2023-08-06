import setuptools

setuptools.setup(
    entry_points = {
        'console_scripts': [
            'pdbuild=pdbuild.commandline.tool:builder',
            '_pdbuildcompletion_=pdbuild.commandline.tool:completion'
        ]
    }
)
