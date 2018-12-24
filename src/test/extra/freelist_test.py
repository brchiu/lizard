from pymtl import *
from util.test_utils import run_test_vector_sim
from util.rtl.freelist import FreeList
from test.config import test_verilog


def test_basic():
  run_test_vector_sim(
      FreeList( 4, 1, 1, False ), [
          ( 'alloc_ports[0].call alloc_ports[0].rdy* alloc_ports[0].index* free_ports[0].call free_ports[0].index'
          ),
          ( 1, 1, 0, 0, 0 ),
          ( 1, 1, 1, 0, 0 ),
          ( 0, 1, '?', 1, 0 ),
          ( 1, 1, 2, 0, 0 ),
          ( 1, 1, 3, 0, 0 ),
          ( 1, 1, 0, 0, 0 ),
          ( 0, 0, '?', 1, 1 ),
          ( 1, 1, 1, 0, 0 ),
      ],
      dump_vcd=None,
      test_verilog=test_verilog )


def test_used_initial():
  run_test_vector_sim(
      FreeList( 4, 1, 1, False, 2 ), [
          ( 'alloc_ports[0].call alloc_ports[0].rdy* alloc_ports[0].index* free_ports[0].call free_ports[0].index'
          ),
          ( 1, 1, 2, 0, 0 ),
          ( 1, 1, 3, 0, 0 ),
          ( 0, 0, '?', 1, 0 ),
          ( 1, 1, 0, 0, 0 ),
          ( 0, 0, '?', 0, 0 ),
      ],
      dump_vcd=None,
      test_verilog=test_verilog )


def test_reverse_free_order():
  run_test_vector_sim(
      FreeList( 2, 1, 1, False ), [
          ( 'alloc_ports[0].call alloc_ports[0].rdy* alloc_ports[0].index* free_ports[0].call free_ports[0].index'
          ),
          ( 1, 1, 0, 0, 0 ),
          ( 1, 1, 1, 0, 0 ),
          ( 0, 0, '?', 1, 1 ),
          ( 1, 1, 1, 0, 0 ),
      ],
      dump_vcd=None,
      test_verilog=test_verilog )


def test_bypass():
  run_test_vector_sim(
      FreeList( 2, 1, 1, True ), [
          ( 'alloc_ports[0].call alloc_ports[0].rdy* alloc_ports[0].index* free_ports[0].call free_ports[0].index'
          ),
          ( 1, 1, 0, 0, 0 ),
          ( 1, 1, 1, 0, 0 ),
          ( 1, 1, 1, 1, 1 ),
          ( 1, 1, 0, 1, 0 ),
      ],
      dump_vcd=None,
      test_verilog=test_verilog )