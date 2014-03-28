/*
 * simple demo for pycflow2dot, use with:
 *    cflow2dot -i hello_simple.c -f png
 * for help:
 *    cflow2dot -h
 */

#include <stdio.h>

void say_hello(char *s)
{
	printf(s);
}

void hello_athens()
{
	say_hello("Hello Athens !\n");
}

void take_off()
{
	printf("Bye bye\n");
}

void cruise()
{
	printf("Nice blue sky\n");
}

void land()
{
	printf("I can see you from up here\n");
}

void fly()
{
	take_off();
	cruise();
	land();
}

void hello_paris()
{
	say_hello("Hello Paris !\n");
}

void hello_los_angeles()
{
	say_hello("Hello Los Angeles !\n");
}

void back()
{
	fly();
}

int main(void)
{
	hello_athens();
	fly();
	hello_paris();
	fly();
	hello_los_angeles();
	back();
}
