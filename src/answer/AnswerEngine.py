# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  AnswerEngine.py                                   :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/28 17:09:38 by roandrie        #+#    #+#               #
#  Updated: 2026/07/28 17:58:28 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from transformers import AutoModelForCausalLM, AutoTokenizer
from src.config import RAGError


class AnswerEngine:
    def __init__(self, k: int, llm_model: str = "Qwen/Qwen3-0.6B") -> None:
        self.k = k
        self.llm_model = llm_model

        # Load the LLM
        self._load_llm()

    def answer(self, query: str) -> str:
        # Create the prompt
        prompt: str = query

        text = self.tokenizer.apply_chat_template(
            prompt, tokenize=False, add_generation_prompt=True, enable_thinking=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=200
        )
        output_ids = generated_ids[0][len(model_inputs.input_ids[0]):].tolist()

        # parsing thinking content
        try:
            # rindex finding 151668 (</think>)
            index = len(output_ids) - output_ids[::-1].index(151668)
        except ValueError:
            index = 0

        thinking_content = self.tokenizer.decode(output_ids[:index], skip_special_tokens=True).strip("\n")
        content = self.tokenizer.decode(output_ids[index:], skip_special_tokens=True).strip("\n")

        print("thinking content:", thinking_content)
        print("content:", content)

    # :------------:----:
    #   Private methods
    # :-----------------:

    def _load_llm(self) -> None:
        # Load the tokenizer and the model
        try:

            self.tokenizer = AutoTokenizer.from_pretrained(self.llm_model)
            self.model = AutoModelForCausalLM.from_pretrained(
                self.llm_model, torch_dtype="auto", device_map="auto"
            )

        except Exception as e:
            raise RAGError(e)
