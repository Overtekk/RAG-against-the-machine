# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __main__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/19 19:27:46 by roandrie        #+#    #+#               #
#  Updated: 2026/06/29 14:38:18 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys
import fire

from student.src.utils import print_error, print_with_color
from student.src import RAGEngine


def main() -> int:
    try:

        print_with_color(
            '\nRAG joined the terminal\n', 'bright_yellow'
        )

        # Init the CLI with Python Fire
        fire.Fire(RAGEngine)

        return 0

    except ValueError as e:
        print_error(e)
        print_with_color('\nRAG left the terminal.', 'bright_yellow')
        return 1

    # except Exception as e:
    #     print_error(f"Critical error: {e}")
    #     print_with_color('\nRAG left the terminal.', 'bright_yellow')
    #     return 1


if __name__ == '__main__':
    try:
        sys.exit(main())

    except KeyboardInterrupt:
        print_error('Program interrupted by the user. 😥\nGoodbye!')
        print_with_color('\nRAG left the terminal.', 'bright_yellow')
        sys.exit(130)
