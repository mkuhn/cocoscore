import unittest

import cocoscore.tagger.co_occurrence_score as co_occurrence_score


class CooccurrenceTest(unittest.TestCase):
    matches_file_path = 'tests/tagger/matches_file.tsv'
    matches_document_level_comentions_file_path = 'tests/tagger/matches_file_document_level_comentions.tsv'
    matches_file_single_matches_path = 'tests/tagger/matches_file_single_matches.tsv'
    matches_file_cross_path = 'tests/tagger/matches_file_cross.tsv'
    score_file_path = 'tests/tagger/sentence_scores_file.tsv'
    entity_file_path = 'tests/tagger/entities2.tsv.gz'

    def test_load_sentence_scores(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        self.assertDictEqual({('--D', 'A'): {(1111, 1, 2): 0.9, (1111, 2, 3): 0.5,
                                             (3333, 2, 2): 0.4, (3333, 2, 3): 0.44},
                              ('C', 'B'): {(2222, 1, 1): 0}}, sentence_scores)

    def test_weighted_counts_sentences_only(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        weighted_counts = co_occurrence_score.get_weighted_counts(None, sentence_scores, None,
                                                                  document_weight=15.0, paragraph_weight=0,
                                                                  sentence_weight=1.0)
        self.assertDictEqual({('--D', 'A'): 15.9 + 15.44,
                              ('C', 'B'): 15,
                              'A': 15.9 + 15.44,
                              '--D': 15.9 + 15.44,
                              'B': 15,
                              'C': 15,
                              None: 15.9 + 15.44 + 15}, weighted_counts)

    def test_co_occurrence_score_sentences_only(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        document_weight = 15.0
        paragraph_weight = 0
        weighting_exponent = 0.6
        counts = co_occurrence_score.get_weighted_counts(None, sentence_scores, None,
                                                         document_weight=document_weight,
                                                         paragraph_weight=paragraph_weight,
                                                         sentence_weight=1.0)
        scores = co_occurrence_score.co_occurrence_score(None, self.score_file_path, None,
                                                         document_weight=document_weight,
                                                         paragraph_weight=paragraph_weight,
                                                         weighting_exponent=weighting_exponent)
        c_a_d = counts[('--D', 'A')]
        c_a = counts['A']
        c_d = counts['--D']
        c_all = counts[None]
        s_a_d = c_a_d ** weighting_exponent * ((c_a_d * c_all) / (c_a * c_d)) ** (1 - weighting_exponent)
        c_b_c = counts[('C', 'B')]
        c_b = counts['B']
        c_c = counts['C']
        s_b_c = c_b_c ** weighting_exponent * ((c_b_c * c_all) / (c_b * c_c)) ** (1 - weighting_exponent)
        self.assertAlmostEqual(s_a_d, scores[('--D', 'A')])
        self.assertAlmostEqual(s_b_c, scores[('C', 'B')])

    def test_weighted_counts_sentences_only_diseases(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        weighted_counts = co_occurrence_score.get_weighted_counts(None, sentence_scores, None,
                                                                  document_weight=15.0, paragraph_weight=0,
                                                                  sentence_weight=1.0,
                                                                  ignore_scores=True)
        self.assertDictEqual({('--D', 'A'): 32,
                              ('C', 'B'): 16,
                              'A': 32,
                              '--D': 32,
                              'B': 16,
                              'C': 16,
                              None: 48}, weighted_counts)

    def test_co_occurrence_score_sentences_only_diseases(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        document_weight = 15.0
        paragraph_weight = 0
        weighting_exponent = 0.6
        counts = co_occurrence_score.get_weighted_counts(None, sentence_scores, None,
                                                         document_weight=document_weight,
                                                         paragraph_weight=paragraph_weight,
                                                         sentence_weight=1.0,
                                                         ignore_scores=True)
        scores = co_occurrence_score.co_occurrence_score(None, self.score_file_path, None,
                                                         document_weight=document_weight,
                                                         paragraph_weight=paragraph_weight,
                                                         weighting_exponent=weighting_exponent,
                                                         ignore_scores=True)
        c_a_d = counts[('--D', 'A')]
        c_a = counts['A']
        c_d = counts['--D']
        c_all = counts[None]
        s_a_d = c_a_d ** weighting_exponent * ((c_a_d * c_all) / (c_a * c_d)) ** (1 - weighting_exponent)
        c_b_c = counts[('C', 'B')]
        c_b = counts['B']
        c_c = counts['C']
        s_b_c = c_b_c ** weighting_exponent * ((c_b_c * c_all) / (c_b * c_c)) ** (1 - weighting_exponent)
        self.assertAlmostEqual(s_a_d, scores[('--D', 'A')])
        self.assertAlmostEqual(s_b_c, scores[('C', 'B')])

    def test_weighted_counts_matches_file(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        weighted_counts = co_occurrence_score.get_weighted_counts(self.matches_file_path, sentence_scores,
                                                                  self.entity_file_path,
                                                                  document_weight=15.0, paragraph_weight=0,
                                                                  sentence_weight=1.0)
        self.assertAlmostEqual(15.9 + 15.44 + 15., weighted_counts[None])  # needed due to floating point strangeness
        del weighted_counts[None]
        self.assertDictEqual({('--D', 'A'): 15.9 + 15.44,
                              ('C', 'B'): 15.,
                              'A': 15.9 + 15.44,
                              '--D': 15.9 + 15.44,
                              'B': 15.,
                              'C': 15.}, weighted_counts)

    def test_co_occurrence_score_matches_file(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        document_weight = 15.0
        paragraph_weight = 0
        weighting_exponent = 0.6
        counts = co_occurrence_score.get_weighted_counts(self.matches_file_path, sentence_scores,
                                                         self.entity_file_path,
                                                         document_weight=document_weight,
                                                         paragraph_weight=paragraph_weight,
                                                         sentence_weight=1.0)
        scores = co_occurrence_score.co_occurrence_score(self.matches_file_path, self.score_file_path,
                                                         self.entity_file_path,
                                                         document_weight=document_weight,
                                                         paragraph_weight=paragraph_weight,
                                                         weighting_exponent=weighting_exponent)
        c_a_d = counts[('--D', 'A')]
        c_a = counts['A']
        c_d = counts['--D']
        c_all = counts[None]
        s_a_d = c_a_d ** weighting_exponent * ((c_a_d * c_all) / (c_a * c_d)) ** (1 - weighting_exponent)
        c_b_c = counts[('C', 'B')]
        c_b = counts['B']
        c_c = counts['C']
        s_b_c = c_b_c ** weighting_exponent * ((c_b_c * c_all) / (c_b * c_c)) ** (1 - weighting_exponent)
        self.assertAlmostEqual(s_a_d, scores[('--D', 'A')])
        self.assertAlmostEqual(s_b_c, scores[('C', 'B')])

    def test_co_occurrence_score_matches_file_diseases(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        document_weight = 15.0
        paragraph_weight = 0
        sentence_weight = 1.0
        weighting_exponent = 0.6
        counts = co_occurrence_score.get_weighted_counts(self.matches_file_path, sentence_scores, self.entity_file_path,
                                                         document_weight=document_weight,
                                                         paragraph_weight=paragraph_weight,
                                                         sentence_weight=1.0,
                                                         ignore_scores=True)

        scores = co_occurrence_score.co_occurrence_score_diseases(self.matches_file_path,
                                                                  self.entity_file_path,
                                                                  document_weight=document_weight,
                                                                  sentence_weight=sentence_weight)
        c_a_d = counts[('--D', 'A')]
        c_a = counts['A']
        c_d = counts['--D']
        c_all = counts[None]
        s_a_d = c_a_d ** weighting_exponent * ((c_a_d * c_all) / (c_a * c_d)) ** (1 - weighting_exponent)
        c_b_c = counts[('C', 'B')]
        c_b = counts['B']
        c_c = counts['C']
        s_b_c = c_b_c ** weighting_exponent * ((c_b_c * c_all) / (c_b * c_c)) ** (1 - weighting_exponent)
        self.assertAlmostEqual(s_a_d, scores[('--D', 'A')])
        self.assertAlmostEqual(s_b_c, scores[('C', 'B')])

    def test_weighted_counts_matches_document_level_comentions_file(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        weighted_counts = co_occurrence_score.get_weighted_counts(self.matches_document_level_comentions_file_path,
                                                                  sentence_scores,
                                                                  self.entity_file_path,
                                                                  document_weight=15.0, paragraph_weight=0,
                                                                  sentence_weight=1.0)

        self.assertDictEqual({('--D', 'A'): 15. + 15.4,
                              ('C', 'B'): 15.,
                              'A': 15. + 15.4,
                              '--D': 15. + 15.4,
                              'B': 15.,
                              'C': 15.,
                              None: 15. + 15.4 + 15.}, weighted_counts)

    def test_co_occurrence_score_matches_document_level_comentions_file(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        document_weight = 15.0
        paragraph_weight = 0
        weighting_exponent = 0.6
        counts = co_occurrence_score.get_weighted_counts(self.matches_document_level_comentions_file_path,
                                                         sentence_scores,
                                                         self.entity_file_path,
                                                         document_weight=document_weight,
                                                         paragraph_weight=paragraph_weight,
                                                         sentence_weight=1.0)
        scores = co_occurrence_score.co_occurrence_score(self.matches_document_level_comentions_file_path,
                                                         self.score_file_path,
                                                         self.entity_file_path,
                                                         document_weight=document_weight,
                                                         paragraph_weight=paragraph_weight,
                                                         weighting_exponent=weighting_exponent)
        c_a_d = counts[('--D', 'A')]
        c_a = counts['A']
        c_d = counts['--D']
        c_all = counts[None]
        s_a_d = c_a_d ** weighting_exponent * ((c_a_d * c_all) / (c_a * c_d)) ** (1 - weighting_exponent)
        c_b_c = counts[('C', 'B')]
        c_b = counts['B']
        c_c = counts['C']
        s_b_c = c_b_c ** weighting_exponent * ((c_b_c * c_all) / (c_b * c_c)) ** (1 - weighting_exponent)
        self.assertAlmostEqual(s_a_d, scores[('--D', 'A')])
        self.assertAlmostEqual(s_b_c, scores[('C', 'B')])

    def test_co_occurrence_score_matches_document_level_comentions_file_diseases(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        document_weight = 15.0
        paragraph_weight = 0
        weighting_exponent = 0.6
        sentence_weight = 1.0
        counts = co_occurrence_score.get_weighted_counts(self.matches_document_level_comentions_file_path,
                                                         sentence_scores, self.entity_file_path,
                                                         document_weight=document_weight,
                                                         paragraph_weight=paragraph_weight,
                                                         sentence_weight=sentence_weight,
                                                         ignore_scores=True)

        scores = co_occurrence_score.co_occurrence_score_diseases(self.matches_document_level_comentions_file_path,
                                                                  self.entity_file_path,
                                                                  document_weight=document_weight,
                                                                  sentence_weight=sentence_weight)
        c_a_d = counts[('--D', 'A')]
        c_a = counts['A']
        c_d = counts['--D']
        c_all = counts[None]
        s_a_d = c_a_d ** weighting_exponent * ((c_a_d * c_all) / (c_a * c_d)) ** (1 - weighting_exponent)
        c_b_c = counts[('C', 'B')]
        c_b = counts['B']
        c_c = counts['C']
        s_b_c = c_b_c ** weighting_exponent * ((c_b_c * c_all) / (c_b * c_c)) ** (1 - weighting_exponent)
        self.assertAlmostEqual(s_a_d, scores[('--D', 'A')])
        self.assertAlmostEqual(s_b_c, scores[('C', 'B')])

    def test_weighted_counts_matches_single_matches_file(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        weighted_counts = co_occurrence_score.get_weighted_counts(self.matches_file_single_matches_path,
                                                                  sentence_scores,
                                                                  self.entity_file_path,
                                                                  document_weight=15.0, paragraph_weight=0,
                                                                  sentence_weight=1.0)
        self.assertAlmostEqual(15.9 + 15.44 + 15., weighted_counts[None])  # needed due to floating point strangeness
        del weighted_counts[None]
        self.assertDictEqual({('--D', 'A'): 15.9 + 15.44,
                              ('C', 'B'): 15.,
                              'A': 15.9 + 15.44,
                              '--D': 15.9 + 15.44,
                              'B': 15.,
                              'C': 15.}, weighted_counts)

    def test_co_occurrence_score_matches_single_matches_file(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        document_weight = 15.0
        paragraph_weight = 0
        weighting_exponent = 0.6
        counts = co_occurrence_score.get_weighted_counts(self.matches_file_single_matches_path,
                                                         sentence_scores,
                                                         self.entity_file_path,
                                                         document_weight=document_weight,
                                                         paragraph_weight=paragraph_weight,
                                                         sentence_weight=1.0)
        scores = co_occurrence_score.co_occurrence_score(self.matches_file_single_matches_path,
                                                         self.score_file_path,
                                                         self.entity_file_path,
                                                         document_weight=document_weight,
                                                         paragraph_weight=paragraph_weight,
                                                         weighting_exponent=weighting_exponent)
        c_a_d = counts[('--D', 'A')]
        c_a = counts['A']
        c_d = counts['--D']
        c_all = counts[None]
        s_a_d = c_a_d ** weighting_exponent * ((c_a_d * c_all) / (c_a * c_d)) ** (1 - weighting_exponent)
        c_b_c = counts[('C', 'B')]
        c_b = counts['B']
        c_c = counts['C']
        s_b_c = c_b_c ** weighting_exponent * ((c_b_c * c_all) / (c_b * c_c)) ** (1 - weighting_exponent)
        self.assertAlmostEqual(s_a_d, scores[('--D', 'A')])
        self.assertAlmostEqual(s_b_c, scores[('C', 'B')])

    def test_co_occurrence_score_matches_single_matches_file_diseases(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        document_weight = 15.0
        paragraph_weight = 0
        weighting_exponent = 0.6
        sentence_weight = 1.0

        counts = co_occurrence_score.get_weighted_counts(self.matches_file_single_matches_path,
                                                         sentence_scores, self.entity_file_path,
                                                         document_weight=document_weight,
                                                         paragraph_weight=paragraph_weight,
                                                         sentence_weight=sentence_weight,
                                                         ignore_scores=True)

        scores = co_occurrence_score.co_occurrence_score_diseases(self.matches_file_path,
                                                                  self.entity_file_path,
                                                                  document_weight=document_weight,
                                                                  sentence_weight=sentence_weight)
        c_a_d = counts[('--D', 'A')]
        c_a = counts['A']
        c_d = counts['--D']
        c_all = counts[None]
        s_a_d = c_a_d ** weighting_exponent * ((c_a_d * c_all) / (c_a * c_d)) ** (1 - weighting_exponent)
        c_b_c = counts[('C', 'B')]
        c_b = counts['B']
        c_c = counts['C']
        s_b_c = c_b_c ** weighting_exponent * ((c_b_c * c_all) / (c_b * c_c)) ** (1 - weighting_exponent)
        self.assertAlmostEqual(s_a_d, scores[('--D', 'A')])
        self.assertAlmostEqual(s_b_c, scores[('C', 'B')])

    def test_weighted_counts_matches_file_cross(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        weighted_counts = co_occurrence_score.get_weighted_counts(self.matches_file_cross_path, sentence_scores,
                                                                  self.entity_file_path,
                                                                  document_weight=15.0, paragraph_weight=0,
                                                                  sentence_weight=1.0)
        self.assertAlmostEqual(15.9 + 15.44 + 15. + 15., weighted_counts[None])  # needed due to float inaccuracy
        del weighted_counts[None]
        self.assertAlmostEqual(15.9 + 15.44 + 15., weighted_counts['--D'])
        del weighted_counts['--D']
        self.assertDictEqual({('--D', 'A'): 15.9 + 15.44,
                              ('--D', 'B'): 15.,
                              ('C', 'B'): 15.,
                              'A': 15.9 + 15.44,
                              'B': 15. + 15.,
                              'C': 15.}, weighted_counts)

    def test_co_occurrence_score_matches_file_cross(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        document_weight = 15.0
        paragraph_weight = 0
        weighting_exponent = 0.6
        counts = co_occurrence_score.get_weighted_counts(self.matches_file_cross_path, sentence_scores,
                                                         self.entity_file_path,
                                                         document_weight=document_weight,
                                                         paragraph_weight=paragraph_weight,
                                                         sentence_weight=1.0)
        scores = co_occurrence_score.co_occurrence_score(self.matches_file_cross_path, self.score_file_path,
                                                         self.entity_file_path,
                                                         document_weight=document_weight,
                                                         paragraph_weight=paragraph_weight,
                                                         weighting_exponent=weighting_exponent)
        c_a_d = counts[('--D', 'A')]
        c_d_b = counts[('--D', 'B')]
        c_a = counts['A']
        c_d = counts['--D']
        c_all = counts[None]
        s_a_d = c_a_d ** weighting_exponent * ((c_a_d * c_all) / (c_a * c_d)) ** (1 - weighting_exponent)
        c_b_c = counts[('C', 'B')]
        c_b = counts['B']
        c_c = counts['C']
        s_b_c = c_b_c ** weighting_exponent * ((c_b_c * c_all) / (c_b * c_c)) ** (1 - weighting_exponent)
        s_d_b = c_d_b ** weighting_exponent * ((c_d_b * c_all) / (c_b * c_d)) ** (1 - weighting_exponent)
        self.assertAlmostEqual(s_a_d, scores[('--D', 'A')])
        self.assertAlmostEqual(s_b_c, scores[('C', 'B')])
        self.assertAlmostEqual(s_d_b, scores[('--D', 'B')])

    def test_co_occurrence_score_matches_file_cross_diseases(self):
        sentence_scores = co_occurrence_score.load_score_file(self.score_file_path)
        document_weight = 15.0
        paragraph_weight = 0
        weighting_exponent = 0.6
        sentence_weight = 1.0
        counts = co_occurrence_score.get_weighted_counts(self.matches_file_cross_path, sentence_scores,
                                                         self.entity_file_path,
                                                         document_weight=document_weight,
                                                         paragraph_weight=paragraph_weight,
                                                         sentence_weight=sentence_weight,
                                                         ignore_scores=True)

        scores = co_occurrence_score.co_occurrence_score_diseases(self.matches_file_cross_path,
                                                                  self.entity_file_path,
                                                                  document_weight=document_weight,
                                                                  sentence_weight=sentence_weight)
        c_a_d = counts[('--D', 'A')]
        c_d_b = counts[('--D', 'B')]
        c_a = counts['A']
        c_d = counts['--D']
        c_all = counts[None]
        s_a_d = c_a_d ** weighting_exponent * ((c_a_d * c_all) / (c_a * c_d)) ** (1 - weighting_exponent)
        c_b_c = counts[('C', 'B')]
        c_b = counts['B']
        c_c = counts['C']
        s_b_c = c_b_c ** weighting_exponent * ((c_b_c * c_all) / (c_b * c_c)) ** (1 - weighting_exponent)
        s_d_b = c_d_b ** weighting_exponent * ((c_d_b * c_all) / (c_b * c_d)) ** (1 - weighting_exponent)
        self.assertAlmostEqual(s_a_d, scores[('--D', 'A')])
        self.assertAlmostEqual(s_b_c, scores[('C', 'B')])
        self.assertAlmostEqual(s_d_b, scores[('--D', 'B')])