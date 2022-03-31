#include "hwlib.hpp"

extern "C" void print_int( int c ){
   hwlib::cout << c << "\n";
}

extern "C" void example();
extern "C" int aMinB(int a, int b);
extern "C" int aPlusB(int a, int b);
extern "C" int odd(int a);
extern "C" int even(int a);

int main(void){

   hwlib::wait_ms(2000);
   hwlib::cout << "Program started\n";
   example();
   hwlib::cout << "Unit tests started\n";

   int passed = 0;
   int failed = 0;

   if(aMinB(1, 1) == 0){
      passed++;
   } else {
      failed++;
   }

   if(aMinB(5, 2) == 3){
      passed++;
   } else {
      failed++;
   }

   if(aPlusB(1, 1) == 2){
      passed++;
   } else {
      failed++;
   }

   if(aPlusB(9, 1) == 10){
      passed++;
   } else {
      failed++;
   }

   if(odd(9) == 1){
      passed++;
   } else {
      failed++;
   }

   if(odd(8) == 0){
      passed++;
   } else {
      failed++;
   }

   if(even(9) == 0){
      passed++;
   } else {
      failed++;
   }

   if(even(8) == 0){
      passed++;
   } else {
      failed++;
   }

   hwlib::cout << "Passed: " << passed << " failed: " << failed << "\n";
}