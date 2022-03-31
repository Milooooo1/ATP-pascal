#include "hwlib.hpp"

extern "C" void print_int( int c ){
   hwlib::cout << c << "\n";
}

extern "C" void example();

int main(void){

   hwlib::wait_ms(2000);
   hwlib::cout << "Program started\n";
   example();
   
}