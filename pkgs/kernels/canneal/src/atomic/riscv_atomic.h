#pragma once

typedef long unsigned int riscv_atomic_int;

static inline bool atomic_cmpset_ptr(riscv_atomic_int *ptr, riscv_atomic_int old_v, riscv_atomic_int new_v) {
    return __sync_bool_compare_and_swap(ptr, old_v, new_v);
}

static inline riscv_atomic_int atomic_load_acq_ptr(riscv_atomic_int *ptr) {
    riscv_atomic_int v = *ptr;
    __sync_synchronize();
    return v;
};

static inline void atomic_store_rel_ptr(riscv_atomic_int *ptr, riscv_atomic_int v) {
    __sync_synchronize();
    *ptr = v;
}
