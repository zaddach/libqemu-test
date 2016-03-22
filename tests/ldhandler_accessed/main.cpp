#include <stdio.h>
#include <libqemu/qemu-lib-external.h>

uint64_t qemu_ld(void *env, uint64_t ptr, uint32_t memop, uint32_t mmu_idx)
{
    printf("SUCCESS: Load data: ptr=0x%08lx, width=%d, signed=%d, is_code=%d\n", ptr, 1 << (memop & LQ_MO_SIZE), memop & LQ_MO_SIGN, memop & LQ_MO_CODE);
    return 0x46c0;
}

int main(int argc, char *argv[])
{
    CodeFlags code_flags = {.arm = {.thumb = 1}};
    int error;
    LLVMValueRef func;

    libqemu_init(qemu_ld, NULL);

    libqemu_gen_intermediate_code(0, code_flags, true, &func);
    return 0;
}
