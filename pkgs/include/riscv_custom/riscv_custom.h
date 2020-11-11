#pragma once

#ifdef __riscv
#include <stdint.h>
#include <time.h>

#if 0
// Original stuff for their own hardware
#define riscv_roi_begin() asm volatile("csrwi 0x801, 1")
#define riscv_roi_end() asm volatile("csrwi 0x801, 0")
#define riscv_terminate() asm volatile("csrwi 0x800, 0")
#endif
#if 0
/* On qemu, access to instret or cycle csr are more or less directly
 * translated into an x86 rdstc instruction.
 * The problem is that I don't exactly know what to do with that stuff */
#define riscv_roi_begin() \
   do { \
       uint64_t __riscv_start_time, __riscv_end_time; \
       asm volatile("csrr %0, 0xc02" : "=r"(__riscv_start_time));

#define riscv_roi_end() \
       asm volatile("csrr %0, 0xc02" : "=r"(__riscv_end_time)); \
       printf("ROI time:  %lu\n", __riscv_end_time - __riscv_start_time); \
   } while (0)

#define riscv_terminate()
#else 
/* Since we are running Linux, let us use clock_gettime() then */
#define riscv_roi_begin() \
   do { \
       struct timespec __riscv_start_time, __riscv_end_time; \
       clock_gettime(CLOCK_REALTIME, &__riscv_start_time);

#define riscv_roi_end() \
       clock_gettime(CLOCK_REALTIME, &__riscv_end_time); \
       printf("ROI time measured: %.3f seconds.\n", \
               (__riscv_end_time.tv_sec - __riscv_start_time.tv_sec) + \
               (__riscv_end_time.tv_nsec - __riscv_start_time.tv_nsec) * 1e-9); \
   } while (0)

#define riscv_terminate()

/* We need that because some measures are taken between functions in 2 programs */
#define riscv_static_roi_decl \
   struct timespec __riscv_start_time, __riscv_end_time

#define riscv_static_roi_begin() \
   do { \
      clock_gettime(CLOCK_REALTIME, &__riscv_start_time); \
   } while (0)

#define riscv_static_roi_end() \
   do { \
       clock_gettime(CLOCK_REALTIME, &__riscv_end_time); \
       printf("ROI time measured: %.3f seconds.\n", \
               (__riscv_end_time.tv_sec - __riscv_start_time.tv_sec) + \
               (__riscv_end_time.tv_nsec - __riscv_start_time.tv_nsec) * 1e-9); \
   } while (0)

#endif

#else

#define riscv_roi_begin()
#define riscv_roi_end()
#define riscv_terminate()

#endif
