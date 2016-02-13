#include <llvm/Support/raw_ostream.h>
#include <stdio.h>
#include <libqemu/qemu-lib-external.h>

uint64_t qemu_ld(void *env, uint64_t ptr, unsigned width, bool is_signed, bool is_code)
{
    libqemu_raise_error(env, 1);
    return 0;
}

int main(int argc, char *argv[])
{
    CodeFlags code_flags = {.arm = {.thumb = 0}};

    libqemu_init(qemu_ld, NULL);
   
    LLVMValueRef func = libqemu_gen_intermediate_code(0, code_flags, true);
    if (!func) {
        llvm::outs() << "SUCCESS: libqemu_gen_intermediate_code returned NULL as expected" << '\n';
        return 0;
    }
    else {
        llvm::outs() << "ERROR: libqemu_gen_intermediate_code returned something unexpected" << '\n';
        return 1;
    }
}
