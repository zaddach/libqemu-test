#include <stdio.h>
#include <libqemu/qemu-lib-external.h>

uint64_t qemu_ld(void *env, uint64_t ptr, unsigned width, bool is_signed, bool is_code)
{
	printf("Load data: ptr=0x%08lx, width=%d, signed=%d, is_code=%d\n", ptr, width, is_signed, is_code);
    return 0x46c0;
}
#define TBFLAG_ARM_THUMB 1

int main(int argc, char *argv[])
{
	libqemu_init(qemu_ld, NULL);

    LLVMValueRef func = libqemu_gen_intermediate_code(0, TBFLAG_ARM_THUMB, 0, true);
}
