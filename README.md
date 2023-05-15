# `hackathon`

Wordle game

```{warning}
Where this documentation refers to the root folder we mean where this README.md is
located.
```

## Getting started

To start using this project, [first make sure your system meets its
requirements](#requirements).

It's suggested that you install this pack and it's requirements within a virtual environment.

## Installing the package (Python Only)

Whilst in the root folder, in the command prompt, you can install the package and it's dependencies
using:

```shell
pip install -e .
```

This installs an editable version of the package. Meaning, when you update the
package code, you do not have to reinstall it for the changes to take effect.
(This saves a lot of time when you test your code)

Remember to update the setup and requirement files inline with any changes to your
package. The inital files contain the bare minimum to get you started.

## Running the pipeline (Python only)

The entry point for the pipeline is stored within the package and called `run_pipeline.py`.
To run the pipeline, run the following code in the terminal (whilst in the root directory of the
project).

```shell
python src/hackathon/run_pipeline.py
```

Alternatively, most Python IDE's allow you to run the code directly from the IDE using a `run` button.

## Licence

Unless stated otherwise, the codebase is released under the MIT License. This covers
both the codebase and any sample code in the documentation. The documentation is ©
Crown copyright and available under the terms of the Open Government 3.0 licence.

### Requirements

- Python 3.6.1+ installed

The required packages can be install directly from the requirements.txt file. For the example directory below:
```
D:/
└── git_repos/
    └── Hackathon/
        └── requirements.txt
```
The command is:
```shell
pip install -r "D:/git_repos/Hackathon/requirements.txt"
```

## Acknowledgements

[This project structure is based on the `govcookiecutter` template
project][govcookiecutter].

[govcookiecutter]: https://github.com/best-practice-and-impact/govcookiecutter