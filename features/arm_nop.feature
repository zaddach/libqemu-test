Feature: Translate an ARM nop instruction to LLVM IR
    Background:
        Given current test directory at "tests/arm_nop"
        Given test binary at "arm_nop"
        When libqemu test is run

    Scenario: Check arm_nop output
        Then the stdout should contain:
        """
        SUCCESS: Translated instruction

        define private void @tcg-llvm-tb-0-0(%struct.ARMCPU*) {
          %"ARMCPU.env.regs[0]_ptr3" = getelementptr %struct.ARMCPU* %0, i32 0, i32 1, i32 0, i32 0
          %"ARMCPU.env.regs[0]" = load i32* %"ARMCPU.env.regs[0]_ptr3", !tcg-llvm.env_access.indices !11150, !tcg-llvm.env_access.member_name !11151
          %"ARMCPU.env.regs[0]_ptr" = getelementptr %struct.ARMCPU* %0, i32 0, i32 1, i32 0, i32 0
          store i32 %"ARMCPU.env.regs[0]", i32* %"ARMCPU.env.regs[0]_ptr", !tcg-llvm.env_access.indices !11150, !tcg-llvm.env_access.member_name !11151
          %"ARMCPU.env.regs[15]_ptr" = getelementptr %struct.ARMCPU* %0, i32 0, i32 1, i32 0, i32 15
          store i32 4, i32* %"ARMCPU.env.regs[15]_ptr", !tcg-llvm.env_access.indices !11152, !tcg-llvm.env_access.member_name !11153
          ret void
        }
        """
