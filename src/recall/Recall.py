# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Recall.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/09/01 09:21:52 by roandrie        #+#    #+#               #
#  Updated: 2026/09/02 13:27:04 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import json
from pathlib import Path
from typing import Any
from src.model import RagDataset


class Recall:
    def __init__(self, dataset: Path) -> None:
        self.dataset = dataset

    def recall_file(self, file_path: Path) -> dict[str, Any]:
        recall_dict: dict[str, Any] = {}

        # Get the data
        with open(self.dataset, 'r', encoding='utf8') as f:
            raw_data_dataset = json.load(f)
            data_dataset = RagDataset.model_validate(raw_data_dataset)
        with open(file_path, 'r', encoding='utf8') as f:
            raw_data_student = json.load(f)

        # Prepare dict of questions for better performance
        student_dict = {
            str(q["question_id"]): q["retrieved_sources"] for q in raw_data_student["search_results"]
        }

        for item in data_dataset.rag_questions:
            print(item.question)
