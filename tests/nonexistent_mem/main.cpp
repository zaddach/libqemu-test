#include <llvm/Support/raw_ostream.h>
#include <stdio.h>
#include <libqemu/qemu-lib-external.h>

uint64_t qemu_ld(void *env, uint64_t ptr, uint32_t memop, uint32_t mmu_idx)
{
    libqemu_raise_error(env, -ENOMEM);
    return 0;
}

int main(int argc, char *argv[])
{
    CodeFlags code_flags = {.arm = {.thumb = 0}};
    int error;
    LLVMValueRef func = NULL;

    libqemu_init(qemu_ld, NULL);
   
    if ((error = libqemu_gen_intermediate_code(0, code_flags, true, &func)) != 0) {
        if (!func) {
            llvm::outs() << "SUCCESS: libqemu_gen_intermediate_code returned error code as expected" << '\n';
            return 0;
        }
        else {
            llvm::outs() << "ERROR: libqemu_gen_intermediate_code returned correct error code, but set output parameter" << '\n';
            return 1;
        }
    }
    else {
        llvm::outs() << "ERROR: libqemu_gen_intermediate_code returned with success, but should't have" << '\n';
        return 1;
    }
}
