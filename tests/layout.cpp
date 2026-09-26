#include <iostream>
#include <iomanip>
#include <cstddef>
#include <vector>
#include <cstdint> // Modern C++ header for fixed-width integers

// Include your header file here
#if defined(_WIN32)
#include "D:\Github\darion-logic-sim\reactor\Profile.h"
#else
#include "../reactor/Profile.h"
#endif

// ─── Helper Macros ──────────────────────────────────────────────────────────

// Macro to print standard layout fields
#define PRINT_FIELD(Struct, Field) \
    std::cout << "  " << std::left << std::setw(15) << #Field \
              << " | Offset: " << std::setw(3) << offsetof(Struct, Field) \
              << " | Size: " << std::setw(3) << sizeof(Struct::Field) << " bytes\n"

// Macro to print bit-fields (since offsetof/sizeof cannot address them directly)
#define PRINT_BITFIELD(Field, Bits) \
    std::cout << "  " << std::left << std::setw(15) << #Field \
              << " | Offset: N/A | Size: " << std::setw(3) << Bits << " bit(s) (Packed)\n"

// ─── Analysis Functions ─────────────────────────────────────────────────────

void analyze_profile() {
    std::cout << "=== Profile ===\n";
    std::cout << "Total Size: " << sizeof(Profile) << " bytes\n";
    std::cout << "------------------------------------------\n";
    PRINT_FIELD(Profile, target);
    PRINT_FIELD(Profile, next);
    PRINT_FIELD(Profile, index);
    PRINT_FIELD(Profile, output);
    std::cout << "\n";
}

void analyze_task() {
    std::cout << "=== Task ===\n";
    std::cout << "Total Size: " << sizeof(Task) << " bytes\n";
    std::cout << "------------------------------------------\n";
    PRINT_FIELD(Task, gate_loc);
    PRINT_FIELD(Task, time);
    PRINT_FIELD(Task, location);
    std::cout << "\n";
}

void analyze_cpp_gate() {
    std::cout << "=== CPP_Gate ===\n";
    std::cout << "Total Size: " << sizeof(CPP_Gate) << " bytes\n";
    std::cout << "------------------------------------------\n";
    
    // Standard variables
    PRINT_FIELD(CPP_Gate, type);
    PRINT_FIELD(CPP_Gate, output);
    PRINT_FIELD(CPP_Gate, inputlimit);
    PRINT_FIELD(CPP_Gate, flags);
    PRINT_FIELD(CPP_Gate, logic);
    PRINT_FIELD(CPP_Gate, seed);
    PRINT_FIELD(CPP_Gate, hitlist_count);
    PRINT_FIELD(CPP_Gate, target_time);
    PRINT_FIELD(CPP_Gate, hitlist);

    
    std::cout << "\n";
}

// ─── Main Execution ─────────────────────────────────────────────────────────

int main() {
    std::cout << "==========================================\n";
    std::cout << "          MEMORY LAYOUT ANALYSIS          \n";
    std::cout << "==========================================\n\n";
    
    analyze_profile();
    analyze_task();
    analyze_cpp_gate();
    
    return 0;
}