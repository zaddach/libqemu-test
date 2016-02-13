Given /^current test directory at "(.+)"$/ do |dir|
    cd(dir)
    @test_dir = dir
end

Given /^test binary at "(.+)"$/ do |cmd|
    check_file_presence([cmd], true)
    @libqemu_cmd = "./" + cmd
end

When /^libqemu test is run$/ do
    run_simple(@libqemu_cmd, @aruba_timeout_seconds)
end
