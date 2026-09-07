# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  Recall.py                                         :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/09/01 09:21:52 by roandrie        #+#    #+#               #
#  Updated: 2026/09/07 19:35:20 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from enum import Enum, auto
import json
from pathlib import Path
from typing import Any
from src import RAGError
from src.model import MinimalSource, RagDataset, StudentSearchResults

class Score(Enum):
    FAILED = 0.0
    SUCCESS = 1.0

    def __str__(self) -> str:
        return str(self.value)

class DatasetType(Enum):
    CODE = auto()
    DOCS = auto()


class Recall:
    def __init__(self, dataset: Path) -> None:
        self._validate_dataset_type(dataset)
        self.dataset = dataset

    def recall_file(self, file_path: Path) -> dict[str, Any]:
        valid_student_data: bool = False

        dataset_type: DatasetType = DatasetType.CODE if "dataset_code" in self.dataset.name else DatasetType.DOCS

        # Get the data from dataset and student
        with open(self.dataset, 'r', encoding='utf8') as f:
            raw_dataset = json.load(f)
        with open(file_path, 'r', encoding='utf8') as f:
            data_student_model = StudentSearchResults.model_validate_json(f.read())
        valid_student_data = True

        # Prepare dict of questions for better performance
        student_dict = {
            str(q.question_id): q.retrieved_sources for q in data_student_model.search_results
        }
        dataset_dict = {
            str(item["question_id"]): [MinimalSource(**s) for s in item.get("sources", [])] for item in raw_dataset.get("rag_questions", [])
        }

        score_list: list[float] = []
        nb_questions_with_sources: int = 0
        nb_questions_with_student_sources: int = 0
        nb_questions_evaluated: int = 0
        # Get all questions to compare with the student file
        for q_id in dataset_dict:
            expected_source = dataset_dict.get(q_id, [])
            nb_questions_evaluated += 1

            if expected_source is None:
                score_list.append(Score.SUCCESS.value)
                continue
            nb_questions_with_sources += 1

            retrieved_sources = student_dict.get(q_id, [])
            if retrieved_sources is None:
                score_list.append(Score.FAILED.value)
                continue
            nb_questions_with_student_sources += 1

            matched_count: int = 0

            for source in expected_source:
                for chunk in retrieved_sources:
                    # Check if file path is correct and "Intersection over Union" is greather than 0.05. If source is good, increase a counter to calculate the ratio further below
                    if chunk.file_path == source.file_path and self._compute_iou(source, chunk) >= 0.05:
                        matched_count += 1
                        break

            # Calculate the ratio
            question_score: float = (matched_count / len(expected_source)) if len(expected_source) > 0 else 0
            score_list.append(question_score)

        # Calculate the recall
        total_recall: float = ((sum(score_list) / len(score_list) * 100)) if len(score_list) > 0 else 0

        # Fill the dictionnary
        return {
            "file_path": file_path,
            "dataset_path": self.dataset,
            "dataset_type": dataset_type,
            "valid_student_data": valid_student_data,
            "nb_questions": len(dataset_dict),
            "nb_questions_with_sources": nb_questions_with_sources,
            "nb_questions_with_student_sources": nb_questions_with_student_sources,
            "nb_questions_evaluated": nb_questions_evaluated,
            "recall_score": total_recall
        }

    @staticmethod
    def print_recall_results(recall_dict: dict[str, Any]) -> None:
        print(f"File: {recall_dict['file_path']}")
        print(f"Dataset: {recall_dict['dataset_path']}")
        print("")
        print(f"Student data is valid: {recall_dict['valid_student_data']}")
        print(f"Total number of questions: {recall_dict['nb_questions']}")
        print(f"Total number of questions with sources: {recall_dict['nb_questions_with_sources']}")
        print(f"Total number of questions with student sources: {recall_dict['nb_questions_with_student_sources']}")
        print("")
        print("🎯 Evaluation Results")
        print("============================================")
        print(f"📊 Questions evaluated: {recall_dict['nb_questions_evaluated']}%")
        print(f"📈 Recall: {round(recall_dict['recall_score'], 2)}")
        if recall_dict['dataset_type'] == DatasetType.CODE and recall_dict['recall_score'] >= 50:
            print("✅ PASS")
        elif recall_dict['dataset_type'] == DatasetType.DOCS and recall_dict['recall_score'] >= 80:
            print("✅ PASS")
        else:
            print("❌ FAILED")
        print("\n")

    # :-----------------:
    #   PRIVATE METHODS
    # :-----------------:

    @staticmethod
    def _compute_iou(source_a: MinimalSource, source_b: MinimalSource) -> float:
        inter_start: int = max(source_a.first_character_index, source_b.first_character_index)
        inter_end: int = min(source_a.last_character_index, source_b.last_character_index)
        intersection: int = max(0, inter_end - inter_start)

        len_a: int = max(0, source_a.last_character_index - source_a.first_character_index)
        len_b: int = max(0, source_b.last_character_index - source_b.first_character_index)
        union: int = len_a + len_b - intersection

        if union <= 0:
            return 0.0

        return intersection / union

    @staticmethod
    def _validate_dataset_type(dataset: Path) -> None:
        required_parts = {"data", "datasets", "AnsweredQuestions"}
        if not required_parts.issubset(dataset.parts):
           raise RAGError("Please provide a json file from 'data/datasets/AnsweredQuestions'.")
