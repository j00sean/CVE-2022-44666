// dllmain.cpp : Defines the entry point for the DLL application.
#pragma warning(disable: 28159)
#include "pch.h"

extern "C" __declspec(dllexport) void Foo() {};

void inject() {
	WinExec("notepad", 1);
}

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
    switch (ul_reason_for_call)
    {
    case DLL_PROCESS_ATTACH:
		inject();
    case DLL_THREAD_ATTACH:
    case DLL_THREAD_DETACH:
    case DLL_PROCESS_DETACH:
        break;
    }
    return TRUE;
}

