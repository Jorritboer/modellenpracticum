#pragma once

#include <cstddef>
#include <iostream>

struct Distance;

struct Point {
    std::size_t x {};
    std::size_t y {};

    Point operator+(Distance) const;
    Point operator-(Distance) const;

    friend Point operator+(Distance, Point);
    friend Point operator-(Distance, Point);

    Distance operator-(Point) const;

    Point& operator+=(Distance);
    Point& operator-=(Distance);

    bool operator==(Point) const;

    friend std::ostream& operator<<(std::ostream&, Point);
};

struct Distance {
    std::ptrdiff_t dx {};
    std::ptrdiff_t dy {};

    Distance operator+(Distance) const;
    Distance operator-(Distance) const;

    Distance& operator+=(Distance);
    Distance& operator-=(Distance);

    bool operator==(Distance) const;

    friend std::ostream& operator<<(std::ostream&, Distance);

    double norm() const;
};
