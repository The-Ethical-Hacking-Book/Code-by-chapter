static const char* keymap[] = { "\0", "ESC", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "_BACKSPACE_", "_TAB_",
                        "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "[", "]", "_ENTER_", "_CTRL_", "a", "s", "d", "f",
                        "g", "h", "j", "k", "l", ";", "'", "`", "_SHIFT_", "\\", "z", "x", "c", "v", "b", "n", "m", ",", "."};
                    



static int __init start(void)
{
	register_keyboard_notifier(&nb);
	printk(KERN_INFO "Keyboard Module Loaded!\n");
	return 0;
}
static void __exit end(void)
{
	unregister_keyboard_notifier(&nb);
	printk(KERN_INFO "Module Unloaded!\n");
}


int notify_keypress(struct notifier_block *nb, unsigned long code, void *_param)
{
	struct keyboard_notifier_param *param;
	param = _param;
	if(code == KBD_KEYCODE)
	{
		if(param->down)
		{
	    	/*-----------------------*/
	    	/* Place your code here */
	    	/*----------------------*/
		}
	}	
	return NOTIFY_OK;
}

struct keyboard_notifier_param {
    struct vc_data *vc;
    init down;
    init shift;
    init ledstate;
    unsigned int value;
};