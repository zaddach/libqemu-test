#include <stdio.h>
#include <libqemu/qemu-lib-external.h>
#include <llvm/Support/raw_ostream.h>

uint64_t qemu_ld(void *env, uint64_t ptr, uint32_t memop, uint32_t mmu_idx)
{
    return 0xf7f0a000;
}

int main(int argc, char *argv[])
{
    CodeFlags code_flags = {.arm = {.thumb = 0}};
    int error;
    LLVMValueRef func;

    libqemu_init(qemu_ld, NULL);

    if ((error = libqemu_gen_intermediate_code(0, code_flags, true, &func)) == 0) {
        char *func_str = LLVMPrintValueToString(func);
        llvm::outs() << "SUCCESS: Translated instruction" << '\n';
        llvm::outs() << func_str << '\n';
        LLVMDisposeMessage(func_str);
    }
    else {
        llvm::outs() << "ERROR: Got error code " << error << " while translating instruction" << '\n';
        return 1;
    }
}
