/*
 * vpi_timer.c — VPI wall-clock timer & perf control for Icarus Verilog
 * =====================================================================
 */

#include <vpi_user.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifdef _WIN32
#include <windows.h>
static LARGE_INTEGER _t_start;
static LARGE_INTEGER _t_freq;
static int           _freq_cached = 0;
#else
#include <time.h>
#include <fcntl.h>
#include <unistd.h>
static struct timespec _t_start;
#endif

void send_perf_ctrl(const char* cmd) {
#ifndef _WIN32
    int fd = open("/tmp/rx_perf_ctrl", O_WRONLY | O_NONBLOCK);
    if (fd != -1) {
        write(fd, cmd, strlen(cmd));
        close(fd);
    }
#endif
}

static PLI_INT32 start_timer_calltf(PLI_BYTE8 *user_data)
{
    (void)user_data;
    send_perf_ctrl("enable\n");

#ifdef _WIN32
    if (!_freq_cached) {
        QueryPerformanceFrequency(&_t_freq);
        _freq_cached = 1;
    }
    QueryPerformanceCounter(&_t_start);
#else
    clock_gettime(CLOCK_MONOTONIC, &_t_start);
#endif
    return 0;
}

static PLI_INT32 start_timer_compiletf(PLI_BYTE8 *user_data)
{
    (void)user_data;
    return 0;
}

static PLI_INT32 stop_timer_calltf(PLI_BYTE8 *user_data)
{
    (void)user_data;
    long long elapsed_ns = 0;

#ifdef _WIN32
    LARGE_INTEGER t_end;
    QueryPerformanceCounter(&t_end);
    long long elapsed_counts = t_end.QuadPart - _t_start.QuadPart;
    double seconds = (double)elapsed_counts / (double)_t_freq.QuadPart;
    elapsed_ns = (long long)(seconds * 1000000000.0);
#else
    struct timespec t_end;
    clock_gettime(CLOCK_MONOTONIC, &t_end);
    elapsed_ns = (t_end.tv_sec - _t_start.tv_sec) * 1000000000LL + (t_end.tv_nsec - _t_start.tv_nsec);
#endif

    send_perf_ctrl("disable\n");
    vpi_printf("$ELAPSED_NS:%lld\n", elapsed_ns);
    return 0;
}

static PLI_INT32 stop_timer_compiletf(PLI_BYTE8 *user_data)
{
    (void)user_data;
    return 0;
}

static void register_tasks(void)
{
    s_vpi_systf_data start_tf = { vpiSysTask, 0, "$start_timer", start_timer_calltf, start_timer_compiletf, 0, 0 };
    s_vpi_systf_data stop_tf = { vpiSysTask, 0, "$stop_timer", stop_timer_calltf, stop_timer_compiletf, 0, 0 };
    vpi_register_systf(&start_tf);
    vpi_register_systf(&stop_tf);
}

void (*vlog_startup_routines[])(void) = { register_tasks, 0 };

