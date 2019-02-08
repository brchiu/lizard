from pymtl import *

from pclib.ifcs import InValRdyBundle, OutValRdyBundle
from util.rtl.interface import Interface, IncludeSome
from util.rtl.method import MethodSpec
from pclib.rtl import RegEn, RegEnRst, RegRst

class ControlFlowManagerInterface(Interface):

  def __init__(s, xlen, seq_idx_nbits):
    super(ControlFlowManagerInterface, s).__init__(
        [
            MethodSpec(
                'check_redirect',
                args={},
                rets={
                    'redirect': Bits(1),
                    'target': Bits(xlen),
                },
                call=False,
                rdy=False,
            ),
            MethodSpec(
                'redirect',
                args={'target': Bits(xlen)},
                rets={},
                call=True,
                rdy=False,
            ),
            MethodSpec(
                'register',
                args={},
                rets={'seq': Bits(seq_idx_nbits)},
                call=True,
                rdy=True,
            ),
        ],
        ordering_chains=[
            [],
        ],
    )


class ControlFlowManager(Model):

  def __init__(s, xlen, reset_vector, seqidx_nbits):
    s.inter = ControlFlowManagerInterface(xlen, seqidx_nbits)
    s.inter.apply(s)

    # The redirect register
    s.redirect_ = Wire(xlen)
    s.redirect_valid_ = Wire(1)

    # Dealloc from tail, alloc at head
    s.tail = RegRst(seqidx_nbits, reset_value=0)
    s.head = RegRst(seqidx_nbits, reset_value=0)
    s.num = RegRst(seqidx_nbits + 1, reset_value=0)

    s.connect(s.check_redirect_redirect, s.redirect_valid_)
    s.connect(s.check_redirect_target, s.redirect_)

    s.connect(s.register_seq, s.head.out)

    # flags
    s.empty = Wire(1)

    @s.combinational
    def set_flags():
      s.empty.v = s.num.out == 0
      # Ready signals:
      s.register_rdy.v = s.num.out < (1 << seqidx_nbits) # Alloc rdy

    # @s.combinational
    # def update_tail():
    #   s.tail.in_.v = (s.tail.out + 1) if s.remove_port.call else s.tail.out

    @s.combinational
    def update_head():
      s.head.in_.v = (s.head.out + 1) if s.register_call else s.head.out

    @s.combinational
    def update_num():
      s.num.in_.v = s.num.out
      if s.register_call:
        s.num.in_.v = s.num.out + 1
      # if s.alloc_port.call and not s.remove_port.call:
      #   s.num.in_.v = s.num.out + 1
      # elif not s.alloc_port.call and s.remove_port.call:
      #   s.num.in_.v = s.num.out - 1

    @s.tick_rtl
    def handle_reset():
      s.redirect_valid_.n = s.reset or s.redirect_call
      s.redirect_.n = reset_vector if s.redirect_call else s.redirect_target
