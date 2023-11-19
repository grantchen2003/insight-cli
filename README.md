## insight-cli

## Overview

<p>The insight-cli provides a CLI for developers to use insight.</p>

## Installation

<p>Before installing the insight-cli, ensure that you have Python version 3.6+ and PIP version 3+.</p>
<p>To install the insight-cli globally, run the following command:</p>

```bash
$ pip install insight-cli
```

<p>To ensure the insight-cli was successfully installed, check your insight-cli version by running: </p>

```bash
$ insight --version
```

## CLI Commands

<p>Note that the following commands require an internet connection.</p>

<p>To initialize the current directory as an insight repository, run the following command: </p>

```bash
$ insight --initialize
```

<p>Note that the following commands must be ran in a directory that has been initialized as an insight repository.</p>

<p>To display the files and lines in an insight repository that satisfy the given natural language query, run the following command: </p>

```bash
$ insight --query "<query>"
```

<p>To uninitialize an insight repository, run the following command: </p>

```bash
$ insight --uninitialize
```

# Example Usage

Install the insight-cli

```bash
$ pip install insight-cli
```

Change the current working directory to the desired codebase. This example will use the following GitHub repository: https://github.com/ChenGrant/fitcountr

```bash
$ git clone https://github.com/ChenGrant/fitcountr
$ cd fitcountr
```

Initialize the current directory as an insight repository:

```bash
$ insight --initialize
The current directory has been successfully initialized as an insight repository.
```

Search in the current insight repository for the "function that makes a connection to the mongodb database".

```bash
$ insight --query "function that makes a connection to the mongodb database"
Found matches in the following files:
/server/src/config/database.js
    Line 3 - 15: const connectToDatabase = async () => {...};
/sever/src/server.js
    Line 25: await connectToDatabase(app);
```

## Contributing

<p>Feel free to contribute to the development of the insight-cli. Submit bug reports, feature requests, or pull requests through GitHub.</p>

## License

<p>This project is licensed under the <a href="https://opensource.org/license/mit/">MIT License</a>.</p>
