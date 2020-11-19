import luigi

from pipeline.tasks import TfIdfSimilarityPipeline


def main():
    input_file = '/Users/aleemr/powerhouse/tf-idf-luigi-pipeline/documents.txt'

    print("Staring pipeline...")
    luigi.build([TfIdfSimilarityPipeline(input_path=input_file)])


if __name__ == '__main__':
    main()
