# ************************************************************************* #
#                                                                           #
#                                                      :::      ::::::::    #
#  __main__.py                                       :+:      :+:    :+:    #
#                                                  +:+ +:+         +:+      #
#  By: roandrie <roandrie@student.42lehavre.fr   +#+  +:+       +#+         #
#                                              +#+#+#+#+#+   +#+            #
#  Created: 2026/06/19 19:27:46 by roandrie        #+#    #+#               #
#  Updated: 2026/06/29 13:54:22 by roandrie        ###   ########.fr        #
#                                                                           #
# ************************************************************************* #

import sys

from src.utils.utils import print_error, print_with_color


def main() -> int:
    try:

        while True:
            pass

        return 0

    except ValueError as e:
        print_error(e)
        return 1

    # except Exception as e:
    #     print_error(f"Critical error: {e}")
    #     return 1


if __name__ == '__main__':
    try:
        sys.exit(main())

    except KeyboardInterrupt:
        print_error('\nProgram interrupted by the user. 😥\nGoodbye!')
        print_with_color('RAG left the terminal.', 'yellow')
        sys.exit(130)
