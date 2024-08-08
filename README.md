## insight-cli

[![Stable Version](https://img.shields.io/pypi/v/insight-cli?color=blue)](https://pypi.org/project/insight-cli/)
[![Downloads](https://img.shields.io/pypi/dm/insight-cli)](https://pypistats.org/packages/insight-cli)

## Overview

insight is a search engine that enables developers to semantically search Python codebases using natural language queries. The insight-cli provides a CLI for developers to use insight.

## Installation

Before installing the insight-cli, ensure that Python version 3.10.0+ is installed. To install the insight-cli globally, run the following command:

```bash
$ pip install insight-cli
```

To ensure the insight-cli was successfully installed, check the insight-cli version by running the following command:

```bash
$ insight --version
```

## CLI Commands

The following cli commands require an internet connection.

To initialize the current directory as an insight repository, run the following command:

```bash
$ insight --initialize
```

To display the insight repository status of the current directory, run the following command:

```bash
$ insight --status
```

The following commands must be ran in a directory that has been initialized as an insight repository.

To display the top code snippets in an insight repository (excluding the files and directories specified in the .insightignore file) that semantically match a given natural language query and limit the number of results, run the following command:

```bash
$ insight --query "<query>" <limit>
```

To uninitialize an insight repository, run the following command:

```bash
$ insight --uninitialize
```

## .insightignore

The .insightignore file contains regex patterns that specify directory and file paths to ignore in an insight repository.

<ul>
    <li>Each line will be considered as a single regex pattern.</li>
    <li>Empty lines are not matchable, they serve only as separators for readability.</li>
    <li>Lines starting with a hashtag '#' serve as comments. A single backslash '\' is placed in front of the first hashtag for patterns that begin with a literal hashtag.</li>
    <li>Scope comments designate patterns to apply exclusively within a specified scope until encountering another scope comment. '## _directory_' and '## _file_' are scope comments which designate patterns to apply within directory and file path scopes respectively.</li>
</ul>

```.insightignore
# Ignore all directory and file paths ending in "test.py"
.*test\.py$

# Ignore all directory and file paths starting with "test_"
^test_

# Ignore all directory and file paths that are exactly "#.py"
\#\.py$

## _directory_
# Patterns now only apply to directory paths

# Ignore all directory paths starting with "main"
^main

## _file_
# Patterns now only apply to file paths

# Ignore all file paths starting with "cache"
^cache
```

## Example Usage

Install the insight-cli.

```bash
$ pip install insight-cli
```

Verify the installation was successful by checking the version.

```bash
$ insight --version
```

Change the current working directory to the desired codebase. This example will use the following GitHub repository: https://github.com/grantchen2003/instapix-word2vec.

```bash
$ git clone https://github.com/grantchen2003/instapix-word2vec
$ cd instapix-word2vec
```

Create a .insightignore file in the current directory and specify that insight should ignore the proto directory.

```bash
$ echo -e "## _directory_\n^proto$" > .insightignore
```

Initialize the current directory as an insight repository. This will create a .insight directory inside the current directory.

```bash
$ insight --initialize
Initialized insight repository in \path\to\current\directory\instapix-word2vec
```

Search in the current insight repository (excluding the proto directory) for the top 3 code snippets that match the query of "function that loads the word2vec model".

```bash
$ insight --query "function that loads the word2vec model" 2
src\word2vec_service.py
Line 13 - 21:
def load_model():
    print("loading model")
    start_time = time.process_time()
    model = KeyedVectors.load_word2vec_format(
        os.environ["MODEL_PATH"], binary=True, limit=None
    )
    end_time = time.process_time()
    print(f"loaded model in {round(end_time - start_time, 1)} seconds")
    return model

src\word2vec_service.py
Line 24 - 49:
class Word2Vec(word2vec_pb2_grpc.Word2VecServiceServicer):
    def __init__(self):
        self.model = load_model()
        self.vocabulary = set(self.model.key_to_index.keys())

    def EmbedWords(self, request, context):
        print("EmbedWords request received")
        words = request.words
        embeddings = [
            word2vec_pb2.Embedding(embedding=self.model.get_vector(word).tolist())
            for word in words
            if word in self.vocabulary
        ]
        return word2vec_pb2.EmbedWordsResponse(embeddings=embeddings)  

    def Similarity(self, request, context):
        print("Similarity request received")
        embeddings1 = np.array([element.embedding for element in request.embeddings1])
        embeddings2 = np.array([element.embedding for element in request.embeddings2])
        if len(embeddings1) == 0 or len(embeddings2) == 0:
            return word2vec_pb2.SimilarityResponse(similarity=0)       
        avg_embedding1 = np.mean(embeddings1, axis=0)
        avg_embedding2 = np.mean(embeddings2, axis=0)
        return word2vec_pb2.SimilarityResponse(
            similarity=cosine_similarity([avg_embedding1], [avg_embedding2])[0][0]
        )
```

## Contributing

Interested in contributing? Please read the [Contribution Guidelines](https://github.com/grantchen2003/insight-cli/blob/main/CONTRIBUTING.md) to get started.

## License

This project is licensed under the [MIT License](https://github.com/grantchen2003/insight-cli/blob/main/LICENSE).
