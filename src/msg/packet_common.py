from pymtl import *
from config.general import *
from msg.codes import *


def CommonBundle( target ):
  target.valid = BitField( XLEN )
  target.pc = BitField( XLEN )
  target.tag = BitField( INST_TAG_LEN )
  target.inst = BitField( RV64Inst.bits )
  target.instr = BitField( ILEN )

  ExceptionBundle( target )


def ExceptionBundle( target ):
  target.exception_triggered = BitField( 1 )
  target.mcause = BitField( XLEN )
  target.mtval = BitField( XLEN )


def DecodeBundle( target ):
  target.is_control_flow = BitField( 1 )
  target.funct3 = BitField( 3 )
  target.opcode = BitField( Opcode.bits )

  FieldValidPair( target, 'imm', DECODED_IMM_LEN )
  FieldValidPair( target, 'csr', CSR_SPEC_LEN )


def valid_name( name ):
  return '%s_valid' % name


def FieldValidPair( target, name, width ):
  setattr( target, name, BitField( width ) )
  setattr( target, valid_name( name ), BitField( 1 ) )


def copy_field_valid_pair( src, dst, name ):
  setattr( dst, name, getattr( src, name ) )
  setattr( dst, valid_name( name ), getattr( src, valid_name( name ) ) )


def copy_common_bundle( src, dst ):
  dst.valid = src.valid
  dst.pc = src.pc
  dst.tag = src.tag
  dst.inst = src.inst
  dst.instr = src.instr

  copy_exception_bundle( src, dst )


def copy_exception_bundle( src, dst ):
  dst.exception_triggered = src.exception_triggered
  dst.mcause = src.mcause
  dst.mtval = src.mtval


def copy_decode_bundle( src, dst ):
  dst.is_control_flow = src.is_control_flow
  dst.funct3 = src.funct3
  dst.opcode = src.opcode
  copy_field_valid_pair( src, dst, 'imm' )
  copy_field_valid_pair( src, dst, 'csr' )
