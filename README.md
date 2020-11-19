# tf-idf-luigi-pipeline

### Running the pipeline
You can run this solution either using a clean python3 environment or using the provided `docker-compose.yaml` file.

**To run it locally:**

I have included a sample eval.sh script in the repository directory. You can use that to do a sanity check by executing `./eval.sh`. For normal run with a custom documents.txt file, follow the process below:

Execute the following from the location of the repository:
```
./run.sh <absolute-path-to-documents.txt>
```

A sample documents.txt file is included in the sample-data directory. Note that the path of the input file has to be **absolute**.

All documents in the documents.txt file should end with the delimiter `%`.

A successful execution would produce a `similarity.csv` file in the CWD of the run.sh file.

**To run it using docker-compose:**

Place your documents.txt file in the same directory as run.sh. Then, from the docker directory, run the following:
```
docker-compose up
```
This will run the pipeline inside a clean python:3.9 container and generate the `similarity.csv` file in the directory of the `run.sh` file. Since it's a mounted volume, generated file should be available on your local file system as well :)


**Cleaning for subsequent runs:**

If you want to do subsequent runs of the pipeline, you can execute the clean.sh script and repeat the running process again. Cleaning is necessary because once luigi has generated a target, it considers that task as done so it would skip running them again.

Execute `clean.sh`:
```
./clean.sh
```

Note that I am running luigi in local-scheduler mode instead of spinning up a scheduler and submitting tasks to it in order to make the pipeline execution simple and convenient for our case.

### Algorithm implementation

I have implemented tf-idf algorithm described in [Speech and Language Processing by Dan Jurafsky and James H. Martin](https://web.stanford.edu/~jurafsky/slp3/).

This method is described in [chapter 6](https://web.stanford.edu/~jurafsky/slp3/6.pdf) of the book.

I also made slight modification to the normalization process so instead of taking the _log10_ of the count for _tf_, I have normalized it by dividing it by the length of the document _d_. This is described [here](http://www.tfidf.com/).

### Mapping tf-idf into a luigi pipeline

Each of the following steps for calculating tf-idf and a final similarity matrix are broken down into the following tasks:
- ParseAndClean - This task parses the documents.txt file and removes any punctuation
- ComputeTf - This task computes the term-frequency for each term in each document
- ComputeIdf - This task computes the inverse document frequency for each term
- ComputeTfIdf - This task computes the TF-IDF weight of each term in each document
- ComputeSimilarity - This task computes similarity and generates a similarity.csv file 

These tasks are defined in `code/pipeline/tasks.py`

Each task writes it's output to a pickled target file that is used as an input for the next task. These files are generated in `code/pipeline/data`.

The underlying implementation of the parser and tf-idf algorithm are located in the nlp package. I have ensured that every possible detail is broken into small functions so they can be unit tested individually. For example, we can unit-test tf component of tf-idf by virtue of having tf as a separate function.

I have also included a jupyter notebook (tf-idf.ipynb) to understand the individual breakdown of the algorithm.

### Improvements and further notes

- Add unit tests for the nlp package


---
Maintainer and author: Muhammad Rafay Aleem
