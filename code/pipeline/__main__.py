import luigi

from pipeline.tasks import TfIdfTask


def main():
    print("Staring pipeline...")
    luigi.build([TfIdfTask()])


if __name__ == '__main__':
    main()
