# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Recall.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/09/01 09:21:52 by roandrie        #+#    #+#               #
#  Updated: 2026/09/03 16:05:38 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum
import json
from pathlib import Path
from typing import Any

class Score(Enum):
    FAILED = 0.0
    SUCCESS = 1.0


class Recall:
    def __init__(self, dataset: Path) -> None:
        self.dataset = dataset

    def recall_file(self, file_path: Path) -> dict[str, Any]:
        recall_dict: dict[str, Any] = {}

        # Get the data
        with open(self.dataset, 'r', encoding='utf8') as f:
            raw_data_dataset = json.load(f)
        with open(file_path, 'r', encoding='utf8') as f:
            raw_data_student = json.load(f)

        # Prepare dict of questions for better performance
        student_dict = {
            str(q["question_id"]): q["retrieved_sources"] for q in raw_data_student["search_results"]
        }
        dataset_dict = {
            str(item["question_id"]): item["sources"] for item in raw_data_dataset["rag_questions"]
        }

        score_list: list[float] = []
        for q_id in dataset_dict:
            expected_source = dataset_dict.get(q_id, [])
            if expected_source is None:
                pass

            retrieved_sources = student_dict.get(q_id, [])
            if retrieved_sources is None:
                score_list.append(Score.FAILED)

            # Check if student source is in the expected source
            for source in expected_source:
                for chunk in retrieved_sources:
                    if chunk["file_path"] == source["file_path"]:
                        if max(chunk["first_character_index"], source["first_character_index"]) < min(chunk["last_character_index"], source["last_character_index"]):
                            score_list.append(Score.SUCCESS)
                            break
                    else:
                        score_list.append(Score.FAILED)
