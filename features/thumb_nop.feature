Feature: Translate an ARM Thumb nop instruction to LLVM IR
    Background:
        Given current test directory at "tests/thumb_nop"
        Given test binary at "thumb_nop"
        When libqemu test is run

    Scenario: Check thumb_nop output
        Then the stdout should contain:
        """
        SUCCESS: Translated instruction
        
        define private void @tcg-llvm-tb-0-0(%struct.ARMCPU*) {
          %"ARMCPU.env.regs[8]_ptr3" = getelementptr %struct.ARMCPU* %0, i32 0, i32 1, i32 0, i32 8
          %"ARMCPU.env.regs[8]" = load i32* %"ARMCPU.env.regs[8]_ptr3", !tcg-llvm.env_access.indices !11150, !tcg-llvm.env_access.member_name !11151
          %"ARMCPU.env.regs[8]_ptr" = getelementptr %struct.ARMCPU* %0, i32 0, i32 1, i32 0, i32 8
          store i32 %"ARMCPU.env.regs[8]", i32* %"ARMCPU.env.regs[8]_ptr", !tcg-llvm.env_access.indices !11150, !tcg-llvm.env_access.member_name !11151
          %"ARMCPU.env.regs[15]_ptr" = getelementptr %struct.ARMCPU* %0, i32 0, i32 1, i32 0, i32 15
          store i32 2, i32* %"ARMCPU.env.regs[15]_ptr", !tcg-llvm.env_access.indices !11152, !tcg-llvm.env_access.member_name !11153
          ret void
        }
        """
