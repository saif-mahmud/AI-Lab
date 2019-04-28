from __future__ import absolute_import

import os
import re

import numpy as np


def get_ethnicity_data(data_dir, params):
    is_ethnicity = params['ethnicity']

    for root, dir, files in os.walk(data_dir):
        unigram_set = []
        bigram_set = []
        trigram_set = []
        length_set = []
        labels = []

        unigram2idx = {}
        idx2unigram = {}
        bigram2idx = {}
        idx2bigram = {}
        trigram2idx = {}
        idx2trigram = {}
        country2idx = {}
        idx2country = {}
        country2ethnicity = {}
        name_max_len = 0

        train_set = []
        valid_set = []
        test_set = []

        for file_cnt, file_name in enumerate(sorted(files)):
            data = open(os.path.join(root, file_name))
            file_len = 0

            if file_name == '0_unigram_to_idx.txt':
                for k, line in enumerate(data):
                    file_len = k + 1
                    unigram, index = line[:-1].split('\t')
                    unigram2idx[unigram] = int(index)
                    idx2unigram[int(index)] = unigram
            elif file_name == '1_bigram_to_idx.txt':
                for k, line in enumerate(data):
                    file_len = k + 1
                    bigram, index = line[:-1].split('\t')
                    bigram2idx[bigram] = int(index)
                    idx2bigram[int(index)] = bigram
            elif file_name == '2_trigram_to_idx.txt':
                for k, line in enumerate(data):
                    file_len = k + 1
                    trigram, index = line[:-1].split('\t')
                    trigram2idx[trigram] = int(index)
                    idx2trigram[int(index)] = trigram
            elif file_name == 'country_to_idx.txt':
                for k, line in enumerate(data):
                    file_len = k + 1
                    country, index = line[:-1].split('\t')
                    if not is_ethnicity:
                        index = k  # Change to index when testing nationality
                    country2idx[country] = int(index)
                    idx2country[int(index)] = country
            elif file_name == 'country_to_ethnicity.txt':
                for k, line in enumerate(data):
                    file_len = k + 1
                    country, eth1, eth2 = line[:-1].split('\t')
                    country2ethnicity[int(country)] = [int(eth1), int(eth2)]
            elif 'data_' in file_name:
                for k, line in enumerate(data):
                    name, nationality = line[:-1].split('\t')
                    name = re.sub(r'\ufeff', '', name)  # delete BOM

                    unigram_vector = [unigram2idx[c] if c in unigram2idx else 0 for c in name]
                    bigram_vector = [bigram2idx[c1 + c2] if (c1 + c2) in bigram2idx else 0
                                     for c1, c2 in zip(*[name[i:] for i in range(2)])]
                    trigram_vector = [trigram2idx[c1 + c2 + c3] if (c1 + c2 + c3) in trigram2idx else 0
                                      for c1, c2, c3 in zip(*[name[i:] for i in range(3)])]

                    # label vector
                    nationality = country2idx[nationality]
                    if is_ethnicity:
                        ethnicity = country2ethnicity[nationality][1]
                        if ethnicity < 0:
                            continue
                    name_length = len(name)

                    if name_max_len < len(name):
                        name_max_len = len(name)

                    unigram_set.append(unigram_vector)
                    bigram_set.append(bigram_vector)
                    trigram_set.append(trigram_vector)
                    length_set.append(name_length)
                    if is_ethnicity:
                        labels.append(ethnicity)
                    else:
                        labels.append(nationality)
                    file_len = k + 1

                if 'train_ch' in file_name:
                    train_set = [unigram_set, bigram_set, trigram_set, length_set, labels]
                elif 'val' in file_name:
                    valid_set = [unigram_set, bigram_set, trigram_set, length_set, labels]
                elif 'ijcai' in file_name:  # test
                    test_set = [unigram_set, bigram_set, trigram_set, length_set, labels]
                else:
                    assert True, 'not allowed file name %s' % file_name

                unigram_set = []
                bigram_set = []
                trigram_set = []
                length_set = []
                labels = []
            else:
                print('ignoring file', file_name)

            print('reading', file_name, 'of length', file_len)

    print('total data length:', len(train_set[0]), len(valid_set[0]), len(test_set[0]))
    print('shape of data:', np.array(train_set).shape, np.array(valid_set).shape, np.array(test_set).shape)
    print('name max length:', name_max_len)

    return (train_set, valid_set, test_set,
            [idx2unigram, unigram2idx, idx2country, country2ethnicity, idx2bigram, idx2trigram])
