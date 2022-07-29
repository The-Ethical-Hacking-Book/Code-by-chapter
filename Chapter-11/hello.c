#include <linux/module.h>
#include <linux/kernel.h>
static int startup(void){
    printk(KERN_NOTICE  "Hello, Kernel Reporting for Duty!\n");
	return 0;
}
static void shutdown(void){
	printk(KERN_NOTICE "Bye bye!\n");
}
module_init(startup);
module_exit(shutdown);
MODULE_LICENSE("GPL");

