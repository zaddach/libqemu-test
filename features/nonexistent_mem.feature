Feature: Access an invalid memory location
    Background:
        Given current test directory at "tests/nonexistent_mem"
        Given test binary at "nonexistent_mem"
        When libqemu test is run

    Scenario: Check that translation aborts cleanly when an invalid memory location is accessed
        Then the stdout should contain "SUCCESS: libqemu_gen_intermediate_code returned error code as expected"
