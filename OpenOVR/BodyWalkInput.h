#pragma once
#include <windows.h>
#include <stdint.h>

struct SharedOpenXRInputState {
    int32_t writeCounter;

    // Output axes from BodyWalk
    bool overrideStickL;
    float thumbstickLX, thumbstickLY;

    bool overrideStickR;
    float thumbstickRX, thumbstickRY;

    // Buttons
    uint64_t buttonsL; 
    uint64_t buttonsR; 
    
    uint64_t overrideMaskL;
    uint64_t overrideMaskR;
};

inline SharedOpenXRInputState* GetBodyWalkInputState() {
    static SharedOpenXRInputState* s_pInputState = nullptr;
    static bool s_attempted = false;

    if (!s_pInputState) {
        HANDLE hMap = OpenFileMappingA(FILE_MAP_READ, FALSE, "Local\\BodyWalk_OpenXR_Input");
        if (hMap) {
            s_pInputState = (SharedOpenXRInputState*)MapViewOfFile(hMap, FILE_MAP_READ, 0, 0, sizeof(SharedOpenXRInputState));
        }
    }
    return s_pInputState;
}
