#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/utsname.h>

static int __init hello_init(void)
{
    pr_info("Hello PYNQ module loaded!\n");
    pr_info("Kernel version: %s\n", utsname()->release);
    return 0;
}

static void __exit hello_exit(void)
{
    pr_info("Hello PYNQ module unloaded!\n");
}

module_init(hello_init);
module_exit(hello_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("xilinx");
MODULE_DESCRIPTION("Hello PYNQ kernel module");

