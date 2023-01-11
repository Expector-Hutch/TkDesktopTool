// 这里负责处理一些在 Python 中较难处理的事
#define _WIN32_WINNT 0x0501
#include <windows.h>
#include <winuser.h>
#include <stdio.h>

long memory_footprint()
{   // 获取内存占用率并返回
    MEMORYSTATUSEX statex;
    statex.dwLength = sizeof(statex);
    GlobalMemoryStatusEx(&statex);
    return statex.dwMemoryLoad;
}



double FileTimeToDouble(FILETIME* pFiletime)
{
    return (double)((*pFiletime).dwHighDateTime * 4.294967296E9) + (double)(*pFiletime).dwLowDateTime;
}

double m_fOldCPUIdleTime;
double m_fOldCPUKernelTime;
double m_fOldCPUUserTime;


void Initialize()
{
    FILETIME ftIdle, ftKernel, ftUser;
    GetSystemTimes(&ftIdle, &ftKernel, &ftUser);
    m_fOldCPUIdleTime = FileTimeToDouble(&ftIdle);
    m_fOldCPUKernelTime = FileTimeToDouble(&ftKernel);
    m_fOldCPUUserTime = FileTimeToDouble(&ftUser);
}

int GetCPUUseRate()
{
    int nCPUUseRate = -1;
    FILETIME ftIdle, ftKernel, ftUser;
    if (GetSystemTimes(&ftIdle, &ftKernel, &ftUser))
    {
        double fCPUIdleTime = FileTimeToDouble(&ftIdle);
        double fCPUKernelTime = FileTimeToDouble(&ftKernel);
        double fCPUUserTime = FileTimeToDouble(&ftUser);
        nCPUUseRate = (int)(100.0 - (fCPUIdleTime - m_fOldCPUIdleTime) / (fCPUKernelTime - m_fOldCPUKernelTime + fCPUUserTime - m_fOldCPUUserTime)*100.0);
    }
    return nCPUUseRate;
}