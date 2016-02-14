import libqemu

def memhandler(self, env, addr, size, signed, code):
    #self.raise_error(env, 1)
    return 0xe1a00000

if __name__ == "__main__":
    codeflags = libqemu.ArmCodeFlags(thumb = False)
    lq = libqemu.Libqemu(memhandler, "/home/ida/projects/build/libqemu-test/libqemu/arm-lib/libqemu-arm.so")
    print(lq.target_name)
    code = lq.gen_intermediate_code(0, codeflags, True)
    print(code)



