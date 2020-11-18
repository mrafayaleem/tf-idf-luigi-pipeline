import os
import pickle
from datetime import date
from functools import reduce

import luigi

from pipeline.nlp.parser import get_docs
from pipeline.nlp.parser import remove_extra_whitespaces
from pipeline.nlp.parser import remove_next_tab_chars
from pipeline.nlp.parser import remove_punctuations
from pipeline.nlp.tfidf import get_normalized_term_frequencies, get_vocab, get_idfs, get_word_term_doc_matrix

TARGET_PATH = os.path.join(os.path.dirname(__file__), 'data/{date}'.format(date=date.today()))
SOURCE_PATH = os.path.join(os.path.dirname(__file__))


class ParseAndClean(luigi.Task):

    def output(self):
        return get_local_target('cleaned.pkl')

    def run(self):
        with get_local_input('documents.txt').open('r') as in_file, self.output().open('w') as out_file:
            raw_doc = in_file.read()

            parsers = [remove_punctuations, remove_next_tab_chars, remove_extra_whitespaces]
            docs = get_docs(raw_doc)
            docs = reduce(lambda res, f: f(res), parsers, docs)

            pickle.dump(docs, out_file)


class ComputeTf(luigi.Task):

    def output(self):
        return get_local_target('tf.pkl')

    def requires(self):
        return ParseAndClean()

    def run(self):
        with get_local_target('cleaned.pkl').open('r') as in_file, \
                self.output().open('w') as out_file:

            docs = pickle.load(in_file)

            tfreq_d, tfreq_norm = get_normalized_term_frequencies(docs)

            pickle.dump({
                'tfreq_d': tfreq_d,
                'tfreq_norm': tfreq_norm
            }, out_file)


class ComputeIdf(luigi.Task):

    def output(self):
        return get_local_target('idf.pkl')

    def requires(self):
        return ComputeTf()

    def run(self):
        with get_local_target('tf.pkl').open('r') as tf_file, self.output().open('w') as out_file, \
                get_local_target('cleaned.pkl').open('r') as doc_file:

            docs = pickle.load(doc_file)
            mapping = pickle.load(tf_file)

            tfreq_d, tfreq_norm = mapping['tfreq_d'], mapping['tfreq_norm']

            terms, vocab_size = get_vocab(docs)
            N = len(docs)

            idfs = get_idfs(docs, terms, tfreq_d, N)

            pickle.dump(idfs, out_file)


class ComputeTfIdf(luigi.Task):

    def requires(self):
        return ComputeIdf()

    def output(self):
        return get_local_target('tf-idf.pkl')

    def run(self):
        with get_local_target('tf.pkl').open('r') as tf_file, \
                get_local_target('idf.pk').open('r') as idf_file, \
                get_local_target('cleaned.pkl').open('r') as doc_file, \
                self.output().open('w') as out_file:

            docs = pickle.load(doc_file)
            terms, vocab_size = get_vocab(docs)
            N = len(docs)
            mapping = pickle.load(tf_file)
            tfreq_d, tfreq_norm = mapping['tfreq_d'], mapping['tfreq_norm']
            idfs = pickle.load(idf_file)

            word_term_doc = get_word_term_doc_matrix(terms, docs, tfreq_norm, idfs)

            pickle.dump(word_term_doc, out_file)


class ComputeSimilarity(luigi.Task):

    def requires(self):
        return ComputeTfIdf()

    def output(self):
        return get_local_target('')



class TfIdfSimilarityPipeline(luigi.WrapperTask):

    def requires(self):
        return [
            ParseAndClean(),
            ComputeTf(),
            ComputeIdf(),
        ]

    def run(self):
        with self.output().open('w') as out_file:
            out_file.write(b"Successfully completed similarity generation!")

    def output(self):
        return get_local_target('pipeline_complete')


def get_local_target(path):
    return luigi.LocalTarget(os.path.join(TARGET_PATH, path), format=luigi.format.Nop)


def get_local_input(path):
    return luigi.LocalTarget(os.path.join(SOURCE_PATH, path))
