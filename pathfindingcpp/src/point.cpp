#include <cmath>

#include "point.hpp"

Point Point::operator+(const Distance other) const {
    return { x + other.dx, y + other.dy };
}

Point Point::operator-(const Distance other) const {
    return { x - other.dx, y - other.dy };
}

Point operator+(const Distance other, const Point point) {
    return { point.x + other.dx, point.y + other.dy };
}

Point operator-(const Distance other, const Point point) {
    return { point.x - other.dx, point.y - other.dy };
}

Distance Point::operator-(const Point other) const {
    return {
        static_cast<std::ptrdiff_t>(x) - static_cast<std::ptrdiff_t>(other.x),
        static_cast<std::ptrdiff_t>(y) - static_cast<std::ptrdiff_t>(other.y)
    };
}

Point& Point::operator+=(const Distance other) {
    x += other.dx;
    y += other.dy;
    return *this;
}

Point& Point::operator-=(const Distance other) {
    x -= other.dx;
    y -= other.dy;
    return *this;
}

bool Point::operator==(const Point other) const {
    return x == other.x && y == other.y;
}

std::ostream& operator<<(std::ostream& out, const Point pos) {
    out << "(" << pos.x << ", " << pos.y << ")";
    return out;
}

Distance Distance::operator+(const Distance other) const {
    return { dx + other.dx, dy + other.dy };
}

Distance Distance::operator-(const Distance other) const {
    return { dx - other.dx, dy - other.dy };
}

Distance& Distance::operator+=(const Distance other) {
    dx += other.dx;
    dy += other.dy;
    return *this;
}

Distance& Distance::operator-=(const Distance other) {
    dx -= other.dx;
    dy -= other.dy;
    return *this;
}

bool Distance::operator==(const Distance other) const {
    return dx == other.dx && dy == other.dy;
}

std::ostream& operator<<(std::ostream& out, const Distance distance) {
    out << "(" << distance.dx << ", " << distance.dy << ")";
    return out;
}

double Distance::norm() const {
    return std::hypot(dx, dy);
}
