# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  AnswerEngine.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/28 17:09:38 by roandrie        #+#    #+#               #
#  Updated: 2026/08/26 10:51:58 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import json
import uuid
from rich.console import Console
from pathlib import Path
from tqdm import tqdm
from transformers import pipeline
from src.model import ChunkSearchResult, StudentSearchResults, MinimalAnswer, StudentSearchResultsAndAnswer
from src.config import RAGError
from src.utils import print_log

MAX_NEW_TOKENS: int = 256
BATCH_SIZE: int = 4

console = Console()


class AnswerEngine:
    def __init__(self, context_limit: int, llm_model: str = "Qwen/Qwen3-0.6B") -> None:
        self._context_limit = context_limit
        self._llm_model = llm_model

        # Load the LLM
        self._load_llm()

    def answer(self, source: list[ChunkSearchResult], question: str, question_id: uuid.UUID | None = None) -> MinimalAnswer:
        if not source:
            return "Invalid source or empty source. Discarding..."

        # with console.status("[bold green]Generating answer..."):
        message = self._generate_prompt(source, question)
        raw_answer = self._generate_answer(message)
        if not raw_answer:
            "ERROR: Answer generation failed."

        # Clean the answer
        clean_answer = raw_answer.replace("<think>", "").replace("</think>", "").strip()

        answer_result: MinimalAnswer = MinimalAnswer(
            question_id=str(uuid.uuid4()) if question_id is None else question_id,
            question=question,
            retrieved_sources=source,
            answer=clean_answer
        )

        return answer_result

    def answer_dataset(self, filepath: Path, save_dir: Path) -> StudentSearchResultsAndAnswer:
        search_result = self._create_dataset(filepath)
        items = search_result.search_results

        print_log(f"Loaded {len(search_result.search_results)} questions.")

        prompts = [self._generate_prompt(item.retrieved_sources, item.question) for item in items]
        raw_answers = self._generate_batch_answers(prompts)

        list_answer: list[MinimalAnswer] = []
        # for item in tqdm(search_result.search_results, desc="Generating answers from dataset"):
        #     answer = self.answer(item.retrieved_sources, item.question, item.question_id if item.question_id is not None else None)
        #     list_answer.append(answer)
        for item, raw_answer in zip(items, raw_answers):
            clean_answer = raw_answer.replace("<think>", "").replace("</think>", "").strip()
            answer_result = MinimalAnswer(
            question_id=item.question_id,
            question=item.question,
            retrieved_sources=item.retrieved_sources,
            answer=clean_answer
        )
            list_answer.append(answer_result)

        answered_dataset = StudentSearchResultsAndAnswer (
            search_results=list_answer,
            k=search_result.k
        )

        save_file_path = Path(save_dir) / filepath.name
        with open(save_file_path, 'w', encoding='utf-8') as f:
            f.write(answered_dataset.model_dump_json(indent=4))

        print_log(f"Processed {len(list_answer)} questions.")
        print_log(f"Save student_search_results_and_answer to '{save_file_path}'.")

    # :-----------------:
    #   PRIVATE METHODS
    # :-----------------:

    def _load_llm(self) -> None:
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
        self._pipe.tokenizer.pad_token_id = self._pipe.tokenizer.eos_token_id
        self._pipe.tokenizer.padding_side = "left"

    def _generate_answer(self, message: str) -> str:
        output = self._pipe(message, return_full_text=False)
        return output[0]["generated_text"]

    def _generate_batch_answers(self, messages: list[list[dict[str, str]]]) -> list[str]:
        outputs: list[str] = []
        for i in tqdm(range(0, len(messages), BATCH_SIZE), desc="Generate answers..."):
            batch = messages[i : i + BATCH_SIZE]
            batch_results = self._pipe(batch, batch_size=BATCH_SIZE, return_full_text=False)
            for res in batch_results:
                outputs.append(res[0]["generated_text"])
        return outputs

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
                "content": f"User\' prompt: '{prompt}'/no_think"
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
