from pwnypack.shellcode.base import BaseEnvironment
from pwnypack.shellcode.types import Register
from pwnypack.target import Target


__all__ = ['ARM']


class ARM(BaseEnvironment):
    """
    Environment that targets a generic, unrestricted ARM architecture.
    """

    target = None  #: Target architecture, initialized in __init__.

    R0 = Register('r0')  #: r0 register
    R1 = Register('r1')  #: r1 register
    R2 = Register('r2')  #: r2 register
    R3 = Register('r3')  #: r3 register
    R4 = Register('r4')  #: r4 register
    R5 = Register('r5')  #: r5 register
    R6 = Register('r6')  #: r6 register
    R7 = Register('r7')  #: r7 register
    R8 = Register('r8')  #: r8 register
    R9 = Register('r9')  #: r9 register
    R10 = Register('r10')  #: r10 register
    R11 = Register('r11')  #: r11 register
    R12 = Register('r12')  #: r12 register
    SP = Register('sp')  #: sp register
    LR = Register('lr')  #: lr register
    PC = Register('pc')  #: pc register

    REGISTER_WIDTH_MAP = {
        32: [R0, R1, R2, R3, R4, R5, R6, R7, R8, R9, R10, R11, R12, SP, LR, PC]
    }

    STACK_REG = SP
    OFFSET_REG = R6
    TEMP_REG = {32: R7}

    PREAMBLE = [
        '.global _start',
        '_start:',
    ]

    def __init__(self, endian=None):
        self.target = Target(Target.Arch.arm, 32, endian)
        super(ARM, self).__init__()

    def reg_push(self, reg):
        return ['push {%s}' % reg]

    def reg_pop(self, reg):
        return ['pop {%s}' % reg]

    def reg_add_imm(self, reg, value):
        return ['add %s, %s, #%d' % (reg, reg, value)]

    def reg_sub_imm(self, reg, value):
        return ['sub %s, %s, #%d' % (reg, reg, value)]

    def reg_load_imm(self, reg, value):
        if not value:
            return ['eor %s, %s' % (reg, reg)]
        elif value < 0xff:
            return ['mov %s, #%d' % (reg, value)]
        else:
            return ['ldr %s, =%d' % (reg, value)]

    def reg_load_reg(self, dest_reg, src_reg):
        return ['mov %s, %s' % (dest_reg, src_reg)]

    def reg_load_offset(self, reg, value):
        return ['add %s, %s, #%d' % (reg, self.OFFSET_REG, value)]

    def finalize(self, code):
        return super(ARM, self).finalize(code) + ['.pool']
