# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  config.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/15 10:29:07 by roandrie        #+#    #+#               #
#  Updated: 2026/07/15 10:30:45 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum


class Config(str, Enum):
    DEFAULT_DATASET_PATH = (
        'data/datasets/UnansweredQuestions/dataset_docs_public.json'
    )
    DEFAULT_STUDENT_ANSWER_PATH = (
        'data/output/search_results/dataset_docs_public.json'
    )
    DEFAULT_STUDENT_SEARCH_RESULTS_PATH = (
        'data/output/search_results/dataset_docs_public.json'
    )
    DEFAULT_SAVE_DIRECTORY = 'data/output/search_results'
    DEFAULT_VLLM_DIRECTORY = 'vllm-0.10.1'
    VLLM_ZIP = 'vllm-0.10.1.zip'
    INDEX_DIRECTORY = 'data/processed/'
    INDEX_BM25_DIRECTORY = 'data/processed/bm25_index'
    INDEX_CHUNKS_DIRECTORY = 'data/processed/chunks'
