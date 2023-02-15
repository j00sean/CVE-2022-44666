// payload.cpp : This file contains the 'main' function. Program execution begins and ends there.
//
#pragma warning(disable: 28159)
#include <iostream>
#include <Windows.h>

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd)
{
	WinExec("notepad", 1);
}
