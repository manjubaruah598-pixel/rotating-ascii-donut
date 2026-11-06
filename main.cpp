// Preview: Rotating Donut Code in C++
// A C++ program that animates a rotating 3D donut in the terminal.
// Run the program to see the donut rotate, drawn with ASCII characters.

#include <iostream>
#include <vector>
#include <cmath>
#include <chrono>
#include <windows.h> // Replaced <thread> with Windows API for sleeping

int main() {
    float A = 0, B = 0;
    float i, j;
    int k;
    
    const int screen_width = 80;
    const int screen_height = 22;
    
    // Clear screen initially
    std::cout << "\x1b[2J";
    
    while (true) {
        // Buffers for the screen frame and depth tracking
        std::vector<char> output_buffer(screen_width * screen_height, ' ');
        std::vector<float> depth_buffer(screen_width * screen_height, 0.0f);
        
        // Theta loop (controls the cross-section circle of the torus)
        for (j = 0; j < 6.28f; j += 0.07f) {
            // Phi loop (revolves the circle around the center axis to create the donut)
            for (i = 0; i < 6.28f; i += 0.02f) {
                float sin_i = std::sin(i);
                float cos_j = std::cos(j);
                float sin_A = std::sin(A);
                float sin_j = std::sin(j);
                float cos_A = std::cos(A);
                
                float circle_x = cos_j + 2; // R2 + R1*cos(j)
                
                // Calculate 1/z (depth) value for perspective projection
                float ooz = 1.0f / (sin_i * circle_x * sin_A + sin_j * cos_A + 5);
                
                float cos_i = std::cos(i);
                float cos_B = std::cos(B);
                float sin_B = std::sin(B);
                
                float t = sin_i * circle_x * cos_A - sin_j * sin_A;
                
                // 3D to 2D projection mapping
                int x = static_cast<int>(40 + 30 * ooz * (cos_i * circle_x * cos_B - t * sin_B));
                int y = static_cast<int>(12 + 15 * ooz * (cos_i * circle_x * sin_B + t * cos_B));
                
                int buffer_index = x + screen_width * y;
                
                // Calculate surface luminance (dot product of normal vector and light source)
                int luminance = static_cast<int>(8 * ((sin_j * sin_A - sin_i * cos_j * cos_A) * cos_B 
                                - sin_i * cos_j * sin_A - sin_j * cos_A - cos_i * cos_j * sin_B));
                
                // Check if the coordinate falls within screen boundaries and is closer than previous depths
                if (screen_height > y && y >= 0 && x >= 0 && screen_width > x && ooz > depth_buffer[buffer_index]) {
                    depth_buffer[buffer_index] = ooz;
                    
                    // Map positive illumination values to ASCII shading characters
                    const char* gradient = ".,-~:;=!*#$@";
                    output_buffer[buffer_index] = gradient[luminance > 0 ? luminance : 0];
                }
            }
        }
        
        // Move cursor back to top left instead of resetting console
        std::cout << "\x1b[H";
        
        // Render the buffer to the terminal
        for (k = 0; k < screen_width * screen_height; k++) {
            std::cout << (k % screen_width ? output_buffer[k] : '\n');
        }
        
        // Increment angles to progress the animation rotation
        A += 0.04f;
        B += 0.02f;
        
        // Replaced std::this_thread::sleep_for with Windows Sleep (takes milliseconds)
        Sleep(30); 
    }
    
    return 0;
}
