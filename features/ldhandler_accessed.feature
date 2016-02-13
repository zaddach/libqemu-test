Feature: Read an instruction from the load memory handler
    Background:
        Given current test directory at "tests/ldhandler_accessed"
        Given test binary at "ldhandler_accessed"
        When libqemu test is run

    Scenario: Check that load memory handler is called
        Then the stdout should contain "SUCCESS: Load data: ptr=0x00000000, width=2, signed=0, is_code=1"
