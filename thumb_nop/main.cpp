#include <stdio.h>
#include <libqemu/qemu-lib-external.h>

uint64_t qemu_ld(void *env, uint64_t ptr, unsigned width, bool is_signed, bool is_code)
{
	printf("Load data: ptr=0x%08lx, width=%d, signed=%d, is_code=%d\n", ptr, width, is_signed, is_code);
    return 0x46c0;
}

int main(int argc, char *argv[])
{
    CodeFlags code_flags = {.arm = {.thumb = 1}};
    libqemu_init(qemu_ld, NULL);

    LLVMValueRef func = libqemu_gen_intermediate_code(0, code_flags, true);
    char *func_str = LLVMPrintValueToString(func);
    printf("%s\n", func_str);
    LLVMDisposeMessage(func_str);
}
