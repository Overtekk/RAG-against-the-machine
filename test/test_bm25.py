# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  test_bm25.py                                      :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/07/03 10:37:19 by roandrie        #+#    #+#               #
#  Updated: 2026/07/03 11:08:41 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import bm25s


corpus = [
    "Outer Wilds is a game about exploring planets in space.",
    "Cow are farms animals.",
    "Wolf are aggresive if you attack them.",
    "Minecraft is the best game in the world.",
    "Python is an animal and also a programmation language.",
    "No ones can survives in the space.",
    "Pac-Man is a game made in Python."
]

retriever = bm25s.BM25(corpus=corpus)
retriever.index(bm25s.tokenize(corpus, show_progress=True))

question = "What is Python"
results, scores = retriever.retrieve(bm25s.tokenize(question), k=2)

print(f"Raw results =\n {results}\n")
print(f"Raw scores = {scores}\n")

doc, score = results[0, 0], scores[0, 0]
print(f"Rank {1} (score: {score:.2f}): {doc}\n")
