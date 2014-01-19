#include <iostream>

class B
{
public:
  static void stat()
  { std::cerr << "=== calling static function B::stat" << std::endl; }

  void nonstat() const
  { std::cerr << "==== calling B::nonstat for some object of B" << std::endl; }
};

class D : public B {};
