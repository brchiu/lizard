#=========================================================================
# test_harness
#=========================================================================
# Includes a test harness that composes a processor, src/sink, and test
# memory, and a run_test function.

import struct
import inspect

from pymtl import *
from tests.context import lizard

from pclib.test import TestSource, TestSink

from lizard.util.arch import rv64g
from lizard.util import elf

from lizard.config.general import *
from lizard.util import line_block
from lizard.util.line_block import Divider
import time
import sys


def asm_test(func):
  name = func.__name__
  if name.startswith("gen_"):
    name = name[4:]
  if name.endswith("_test"):
    name = name[:-5]
  return (name, func)


def is_mod_function(mod, func):
  return inspect.isfunction(func) and inspect.getmodule(func) == mod


def list_functions(mod):
  return [
      func for func in mod.__dict__.itervalues() if is_mod_function(mod, func)
  ]


def clean_module_name(m, n=2):
  return '-'.join(m.__name__.split('.')[-n:])


def extract_module_tests(m):
  funcs = [f for f in list_functions(m) if f.__name__.endswith('_test')]
  result = [('{}_{}'.format(clean_module_name(m), name), func)
            for name, func in [asm_test(f) for f in funcs]]
  return result


def extract_tests(ms):
  return [test_pair for m in ms for test_pair in extract_module_tests(m)]


#=========================================================================
# run_test
#=========================================================================


def run_test(TestHarness, gen_test, max_cycles=50000000, extra_cycles=3):
  # Assemble the test program
  asm = gen_test()
  if isinstance(asm, list):
    asm = '\n'.join(asm)
  print(asm)
  mem_image = rv64g.assembler.assemble(asm)

  # Run the test
  run_test_image(TestHarness, mem_image, max_cycles, extra_cycles)


#=========================================================================
# run_test_bin: Run a test from an elf binary
#=========================================================================
def run_test_elf(TestHarness, elf_file, max_cycles=50000000, extra_cycles=3):
  with open(elf_file, "rb") as fd:
    mem = elf.elf_reader(fd, True)
    run_test_image(TestHarness, mem, max_cycles, extra_cycles)


def run_test_image(TestHarness, mem_image, max_cycles=50000000, extra_cycles=3):
  # Instantiate and elaborate the model
  model = TestHarness()

  model.elaborate()

  # Load the program into the model
  model.load(mem_image)

  # Create a simulator using the simulation tool
  sim = SimulationTool(model)

  # Run the simulation
  print('')

  def print_line_trace():
    print(line_block.join([
        '{:>3} '.format(sim.ncycles),
        sim.model.line_trace(),
    ]))
    print('\n')

  sim.reset()
  last = time.time()
  while not model.done() and sim.ncycles < max_cycles:
    print_line_trace()
    sim.cycle()

  # print the very last line trace after the last tick
  print_line_trace()

  # Force a test failure if we timed out

  assert sim.ncycles < max_cycles

  # Add a couple extra ticks so that the VCD dump is nicer
  for _ in range(extra_cycles):
    sim.cycle()

  model.cleanup()
