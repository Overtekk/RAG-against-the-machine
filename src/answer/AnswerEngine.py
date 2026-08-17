# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  AnswerEngine.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/28 17:09:38 by roandrie        #+#    #+#               #
#  Updated: 2026/08/17 16:28:14 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from tqdm import tqdm
from transformers import pipeline
from src.model import MinimalSearchResults
from src.config import RAGError
from src.utils import print_log

MAX_GENERATION_LENGHT: int = 256


class AnswerEngine:
    def __init__(self, k: int, llm_model: str = "Qwen/Qwen3-0.6B") -> None:
        self._k = k
        self._llm_model = llm_model

        # Load the LLM
        self._load_llm()

    def answer(self, source: list[MinimalSearchResults], question_list: list[str]) -> str:
        if not source:
            return "Invalid source or empty source. Discarding..."

        for question in tqdm(question_list, desc="Generating"):
            message = self._generate_prompt(source, question)
            answer = self._generate_answer(message)
            print(answer)

    # :-----------------:
    #   PRIVATE METHODS
    # :-----------------:

    def _generate_answer(self, message: str) -> str:
        output = self._pipe(message, max_new_tokens=MAX_GENERATION_LENGHT)
        return output[0]["generated_text"]

    def _generate_prompt(self, source: list[MinimalSearchResults], prompt: str) -> str:
        # Preparing source formatting
        formatted_source: dict[int, str] = {}
        for i, result in enumerate(source):
            formatted_source[i] = result.content

        # Prepare the prompt (/no_think prevent the model to using the <think>)
        message = [
            {
                "role": "system",
                "content": ("Answer the user\'s prompt using ONLY the provided"
                            "sources. Your answer will be concise. The sources"
                            "are: \n\n"
                            f"{formatted_source}")
            },
            {
                "role": "user",
                "content": f"User\' prompt: {prompt}"
            }
        ]

        return message

    # :------------:----:
    #   Private methods
    # :-----------------:

    def _load_llm(self) -> None:
        try:
            print_log(f"Initializing LLM using '{self._llm_model}'", "gold1")

            device = "cpu"

            # Load the model throught pipeline
            self._pipe = pipeline(
                task="text-generation",
                model=self._llm_model,
                device=device,
                torch_dtype="auto"
            )

        except Exception as e:
            raise RAGError(e)
