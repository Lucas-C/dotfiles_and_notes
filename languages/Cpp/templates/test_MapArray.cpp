#include "MapArray.tpp"
#include "Macros.hpp"

class Point {
public:
    double x;
    double y;
    double z;
    Point() : x(0), y(0), z(0){}
    Point(double x_, double y_, double z_, Color* c_ = 0) : x(x_), y(y_), z(z_){}
    std::ostream& operator>>(std::ostream &strm) const {
        return strm << x << "  " << y << "  " << z;
    }
};

inline std::ostream& operator<<(std::ostream &strm, const Point& p) {
        return p >> strm;
}

void main() {
    MapArray<Point> m(8);

    m.insert(Point(1, 1, 1));
    m.insert(Point(1, 1, 0));
    m.insert(Point(1, 0, 1));
    m.insert(Point(1, 0, 0));

    m.insert(Point(0, 1, 1));
    m.insert(Point(0, 1, 0));
    m.insert(Point(0, 0, 1));
    m.insert(Point(0, 0, 0));

    for (unsigned int i = 0; i < m.size(); ++i)
        std::cout << m[i] << "\n";
}

