from pymtl import *
from bitutil import bit_enum
from config.general import *
from msg.packet_common import *


class DecodePacket( BitStructDefinition ):

  def __init__( s ):
    CommonBundle( s )
    DecodeBundle( s )

    FieldValidPair( s, 'rs1', REG_SPEC_LEN )
    FieldValidPair( s, 'rs2', REG_SPEC_LEN )
    FieldValidPair( s, 'rd', REG_SPEC_LEN )

  def __str__( s ):
    return 'imm:{} inst:{: <5} rs1:{} v:{} rs2:{} v:{} rd:{} v:{}'.format(
        s.imm, RV64Inst.name( s.inst ), s.rs1, s.rs1_valid, s.rs2, s.rs2_valid,
        s.rd, s.rd_valid )
