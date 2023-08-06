#  Created byMartin.cz
#  Copyright (c) Martin Strohalm. All rights reserved.

from pero import Enum, NONE

# define constants
CIRCLE_Z = 100
REGION_Z = 0

# define values
FULL = 'full'
SEMI = 'semi'

# define venn diagram modes
VENN_MODE_NONE = NONE
VENN_MODE_SEMI = SEMI
VENN_MODE_FULL = FULL

VENN_MODE = Enum(
    NONE = VENN_MODE_NONE,
    SEMI = VENN_MODE_SEMI,
    FULL = VENN_MODE_FULL)
