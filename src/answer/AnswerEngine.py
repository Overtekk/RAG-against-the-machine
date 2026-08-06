# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  AnswerEngine.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/28 17:09:38 by roandrie        #+#    #+#               #
#  Updated: 2026/08/06 14:48:31 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from transformers import pipeline
from accelerate import Accelerator
from src.model import MinimalSearchResults
from src.config import RAGError
from src.utils import print_log

MAX_GENERATION_LENGHT: int = 300


class AnswerEngine:
    def __init__(self, k: int, llm_model: str = "Qwen/Qwen3-0.6B") -> None:
        self._k = k
        self._llm_model = llm_model

        # Load the LLM
        self._load_llm()

    def answer(self, source: list[MinimalSearchResults], prompt: str) -> str:
        if not source:
            return "Invalid source or empty source. Discarding..."

        message = self._generate_prompt(source, prompt)
        answer = self._generate_answer(message)
        print(answer)

    # :-----------------:
    #   PRIVATE METHODS
    # :-----------------:

    def _generate_answer(self, message: str) -> str:
        output = self._pipe(message, max_length=MAX_GENERATION_LENGHT)
        return output[0]

    def _generate_prompt(self, source: list[MinimalSearchResults], prompt: str) -> str:
        # Prepare the prompt (/no_think prevent the model to using the <think>)
        message = [
            {
                "role": "system",
                "content": ("Answer the user\'s prompt using ONLY the provided"
                            "sources. Your answer will be concise. The sources"
                            "are: \n\n"
                            f"{source.retrieved_sources}")
            },
            {
                "role": "user",
                "content": f"User\' prompt: {prompt} /no_think"
            }
        ]

        return message

    # :------------:----:
    #   Private methods
    # :-----------------:

    def _load_llm(self) -> None:
        try:
            print_log(f"Initializing LLM using '{self._llm_model}'", "gold1")

            # Auto detect an available accelerator
            device = Accelerator().device

            # Load the model throught pipeline
            self._pipe = pipeline(
                task="text-generation",
                model=self._llm_model,
                device=device
            )

        except Exception as e:
            raise RAGError(e)
