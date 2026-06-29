# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  engine.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/29 14:12:52 by roandrie        #+#    #+#               #
#  Updated: 2026/06/29 14:36:25 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

DEFAULT_DATASET_PATH : str = (
    'data/datasets/UnansweredQuestions/dataset_docs_public.json'
)
DEFAULT_SAVE_DIRECTORY: str = 'data/output/search_results'
DEFAULT_STUDENT_ANSWER_PATH: str = (
    'data/output/search_results/dataset_docs_public.json'
)
DEFAULT_STUDENT_SEARCH_RESULTS_PATH: str = (
    'data/output/search_results/dataset_docs_public.json'
)


class RAGEngine():

    def index(self, max_chunk_size: int = 2000) -> None:
        pass

    def answer(self, prompt: str, k: int = 10) -> None:
        pass

    def search_dataset(
        self,
        dataset_path: str = DEFAULT_DATASET_PATH,
        k: int = 10,
        save_directory: str = DEFAULT_SAVE_DIRECTORY
    ) -> None:
        pass

    def evaluate_student_search_results(
        self,
        student_answer_path: str = DEFAULT_STUDENT_ANSWER_PATH,
        dataset_path: str = DEFAULT_DATASET_PATH,
        k: int = 10,
        max_context_lenght: int = 2000
    ) -> None:
        pass

    def answer_dataset(
        self,
        student_search_results_path: str = DEFAULT_STUDENT_SEARCH_RESULTS_PATH,
        save_directory: str = DEFAULT_SAVE_DIRECTORY
    ) -> None:
        pass
