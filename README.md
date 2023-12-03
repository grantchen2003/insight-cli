# insight-cli

## Overview

The insight-cli provides a CLI for developers to use insight.

## Installation

Before installing the insight-cli, ensure that you have Python version 3.12.0+ and PIP version 23.2.1+.
To install the insight-cli globally, run the following command:

```bash
$ pip install insight-cli
```

To ensure the insight-cli was successfully installed, check your insight-cli version by running: 

```bash
$ insight --version
```

## CLI Commands

The following commands require an internet connection.

To initialize the current directory as an insight repository, run the following command: 

```bash
$ insight --initialize
```

The following commands must be ran in a directory that has been initialized as an insight repository.

To display the files and lines in an insight repository (excluding the files and folders specified in the .insightignore file) that satisfy the given natural language query, run the following command: 

```bash
$ insight --query "<query>"
```

To uninitialize an insight repository, run the following command: 

```bash
$ insight --uninitialize
```

## Example Usage

Install the insight-cli.

```bash
$ pip install insight-cli
```

Change the current working directory to the desired codebase. This example will use the following GitHub repository: https://github.com/ChenGrant/fitcountr.

```bash
$ git clone https://github.com/ChenGrant/fitcountr
$ cd fitcountr
```

Initialize the current directory as an insight repository. This will create a .insight directory inside the current directory.

```bash
$ insight --initialize
The current directory has been successfully initialized as an insight repository.
```

Create a .insightignore file in the current directory and specify that we don't want to search the .git directory.

```bash
$ echo ".git" > .insightignore
```

Search in the current insight repository (excluding the .git directory) for the "function that makes a connection to the mongodb database".

```bash
$ insight --query "function that makes a connection to the mongodb database"
2 matches found in the following files:
/server/insight_cli/config/database.js
    Line 3 - 15: const connectToDatabase = async () => {...};
    
/server/insight_cli/server.js
    Line 25: await connectToDatabase(app);
```

## Contributing

Feel free to contribute to the development of the insight-cli. Submit bug reports, feature requests, or pull requests through GitHub.

## License
This project is licensed under the [MIT License](./LICENSE).
