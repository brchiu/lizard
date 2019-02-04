from model.test_model import run_test_state_machine
from util.rtl.snapshotting_registerfile import SnapshottingRegisterFile
from util.fl.snapshotting_registerfile import SnapshottingRegisterFileFL


def test_state_machine():
  run_test_state_machine(SnapshottingRegisterFile, SnapshottingRegisterFileFL,
                         (8, 4, 1, 1, False, False, 4))
