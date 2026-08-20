# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  AnswerEngine.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/28 17:09:38 by roandrie        #+#    #+#               #
#  Updated: 2026/08/20 09:48:12 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import json
import uuid
from rich.console import Console
from pathlib import Path
from transformers import pipeline
from src.model import ChunkSearchResult, StudentSearchResults, MinimalAnswer, StudentSearchResultsAndAnswer
from src.config import RAGError
from src.utils import print_log

MAX_NEW_TOKENS: int = 256

console = Console()


class AnswerEngine:
    def __init__(self, context_limit: int, llm_model: str = "Qwen/Qwen3-0.6B") -> None:
        self._context_limit = context_limit
        self._llm_model = llm_model

        # Load the LLM
        self._load_llm()

    def answer(self, source: list[ChunkSearchResult], question: str) -> MinimalAnswer:
        if not source:
            return "Invalid source or empty source. Discarding..."

        with console.status("[bold green]Generating answer..."):
            message = self._generate_prompt(source, question)
            raw_answer = self._generate_answer(message)
        if not raw_answer:
            "ERROR: Answer generation failed."

        # Clean the answer
        clean_answer = raw_answer.replace("<think>", "").replace("</think>", "").strip()

        answer_result: MinimalAnswer = MinimalAnswer(
            question_id=str(uuid.uuid4()),
            question=question,
            retrieved_sources=source,
            answer=clean_answer
        )

        return MinimalAnswer.model_validate(answer_result)

    def answer_dataset(self, filepath: Path) -> MinimalAnswer:
        search_result = self._create_dataset(filepath)
        print(search_result)


    # :-----------------:
    #   PRIVATE METHODS
    # :-----------------:

    def _load_llm(self) -> None:
        try:
            print_log(f"Initializing LLM using '{self._llm_model}'", "gold1")

            # Load the model throught pipeline
            self._pipe = pipeline(
                task="text-generation",
                model=self._llm_model,
                device=0,
                clean_up_tokenization_spaces=False
            )
            self._pipe.model.generation_config.max_new_tokens = MAX_NEW_TOKENS
            self._pipe.generation_config.max_length = None

        except Exception as e:
            raise RAGError(e)

    def _generate_answer(self, message: str) -> str:
        output = self._pipe(message, return_full_text=False)
        return output[0]["generated_text"]

    def _generate_prompt(self, sources: list[ChunkSearchResult], prompt: str) -> str:
        # Preparing source formatting
        formatted_source = "\n".join([str(source.content) for source in sources])
        # Cut if text too long
        if len(formatted_source) > self._context_limit:
            formatted_source = formatted_source[:1000]


        # Prepare the prompt (/no_think prevent the model to using the <think>)
        message = [
            {
                "role": "system",
                "content": ("Answer the user\'s prompt using ONLY the provided"
                            "sources. Your answer will be concise but helpfull"
                            "for the user."
                            "The sources are: \n\n"
                            f"{formatted_source}")
            },
            {
                "role": "user",
                "content": f"User\' prompt: {prompt}/no_think"
            }
        ]

        return message


    def _create_dataset(self, filepath: Path) -> StudentSearchResults:
        if filepath is None:
            raise RAGError("empty filepath.")

        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            dataset = StudentSearchResults.model_validate(data)
            return dataset
