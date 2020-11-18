import luigi

from pipeline.tasks import TfIdfSimilarityPipeline


def main():
    print("Staring pipeline...")
    luigi.build([TfIdfSimilarityPipeline()])


if __name__ == '__main__':
    main()
