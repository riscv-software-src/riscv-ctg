# See LICENSE.incore file for details
import sys
import os
import shutil
import yaml

from riscv_ctg.log import *
from riscv_ctg.utils import *
from riscv_ctg.constants import *
from riscv_ctg.__init__ import __version__

def ctg(verbose, dir, clean):

    logger.level(verbose)
    logger.info('****** RISC-V Compliance Test Generator {0} *******'.format(__version__ ))
    logger.info('Copyright (c) 2020, InCore Semiconductors Pvt. Ltd.')
    logger.info('All Rights Reserved.')
    
