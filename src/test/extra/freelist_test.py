from pymtl import *
from util.test_utils import run_test_vector_sim
from util.rtl.freelist import FreeList


def test_basic():
  run_test_vector_sim(
      FreeList( 4 ), [
          ( 'alloc_port.call alloc_port.ret.valid* alloc_port.ret.index* free_port.call free_port.arg'
          ),
          ( 1, 1, 0, 0, 0 ),
          ( 1, 1, 1, 0, 0 ),
          ( 0, 1, 2, 1, 0 ),
          ( 1, 1, 2, 0, 0 ),
          ( 1, 1, 3, 0, 0 ),
          ( 1, 1, 0, 0, 0 ),
          ( 1, 1, 1, 1, 1 ),
      ],
      dump_vcd=None,
      test_verilog=True )


def test_used_initial():
  run_test_vector_sim(
      FreeList( 4, 2 ), [
          ( 'alloc_port.call alloc_port.ret.valid* alloc_port.ret.index* free_port.call free_port.arg'
          ),
          ( 1, 1, 2, 0, 0 ),
          ( 1, 1, 3, 0, 0 ),
          ( 0, 0, 3, 1, 0 ),
          ( 1, 1, 0, 0, 0 ),
          ( 1, 0, 0, 0, 0 ),
      ],
      dump_vcd=None,
      test_verilog=True )
