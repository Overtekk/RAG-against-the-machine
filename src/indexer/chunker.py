# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  chunker.py                                        :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/03 14:37:38 by roandrie        #+#    #+#               #
#  Updated: 2026/07/13 14:14:02 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

from langchain_text_splitters import (
    MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter)
from src.model import MinimalSource
from src.utils import check_file_extension, print_log


headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
        ("####", "Header 4"),
    ]


class ChunkerEngine():
    def __init__(self, chunk_size: int) -> None:
        self._chunk_size: int = chunk_size

    def process(
        self, file_path: str, content: str) -> list[tuple[MinimalSource, str]]:
        if check_file_extension(file_path, '.md'):
            return self._chunk_md_file(file_path, content)

        elif check_file_extension(file_path, '.py'):
            return self._chunk_py_file(file_path, content)

        else:
            print_log(f"Unkown file extension for {file_path}.", 'red')

    # :-----------------:
    #   PRIVATE METHODS
    # :-----------------:

    def _chunk_py_file(
        self, file_path: str, content: str) -> list[tuple[MinimalSource, str]]:
        return []

    def _chunk_md_file(
        self, file_path: str, content: str) -> list[tuple[MinimalSource, str]]:
        chunked_txt: list[tuple[MinimalSource, str]] = []

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self._chunk_size,
            chunk_overlap=0,
            keep_separator=True
        )

        sub_search_start = 0
        for sub_txt in text_splitter.split_text(content):
            sub_first_index = content.find(sub_txt, sub_search_start)
            sub_last_index = sub_first_index + len(sub_txt)
            sub_search_start = sub_last_index

            chunked_txt.append((MinimalSource(
                file_path=file_path,
                first_character_index=sub_first_index,
                last_character_index=sub_last_index), sub_txt)
            )

        return chunked_txt

# chunked_txt: list[tuple[MinimalSource, str]] = []
# curr_index: int = 0

# # Split the content with the header
# markdown_splitter = MarkdownHeaderTextSplitter(
#     headers_to_split_on=headers_to_split_on, strip_headers=False
# )
# md_header_splits = markdown_splitter.split_text(content)

# # Get the index
# for split in md_header_splits:
#     raw_text = split.page_content

#     first_char_index = content.find(raw_text, curr_index)

#     # Get the last index
#     last_char_index = first_char_index + len(raw_text)
#     curr_index = last_char_index

#     # Check the chunk_size
#     if len(raw_text) <= self._chunk_size:
#         chunked_txt.append((MinimalSource(
#             file_path=file_path,
#             first_character_index=first_char_index,
#             last_character_index=last_char_index), raw_text)
#         )

#     else:
#         text_splitter = RecursiveCharacterTextSplitter(
#             chunk_size=self._chunk_size,
#             chunk_overlap=0,
#             keep_separator=True
#         )
#         sub_search_start = first_char_index

#         for sub_txt in text_splitter.split_text(raw_text):
#             sub_first_index = content.find(sub_txt, sub_search_start)
#             sub_last_index = sub_first_index + len(sub_txt)

#             sub_search_start = sub_last_index

#             chunked_txt.append((MinimalSource(
#                 file_path=file_path,
#                 first_character_index=sub_first_index,
#                 last_character_index=sub_last_index), sub_txt)
#             )

# return chunked_txt
