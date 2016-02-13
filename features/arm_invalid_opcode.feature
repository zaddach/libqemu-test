Feature: Translate an ARM invalid instruction to LLVM IR
    Background:
        Given current test directory at "tests/arm_invalid_opcode"
        Given test binary at "arm_invalid_opcode"
        When libqemu test is run

    Scenario: Check arm_invalid_opcode output
        Then the stdout should contain:
        """
        SUCCESS: Translated instruction

        define private void @tcg-llvm-tb-0-0(%struct.ARMCPU*) {
          %"ARMCPU.env.regs[15]_ptr" = getelementptr %struct.ARMCPU* %0, i32 0, i32 1, i32 0, i32 15
          store i32 0, i32* %"ARMCPU.env.regs[15]_ptr", !tcg-llvm.env_access.indices !11150, !tcg-llvm.env_access.member_name !11151
          %env_ptr4 = getelementptr %struct.ARMCPU* %0, i32 0, i32 1
          call void @helper_exception_with_syndrome(%struct.CPUARMState* %env_ptr4, i32 1, i32 33554432, i32 1)
          ret void
        }
        """
