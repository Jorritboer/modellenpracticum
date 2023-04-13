#pragma once

#include <utility>

#include "point.hpp"
#include "tile_data.hpp"

class Tile {
private:
    double weight {};

    bool enabled : 1 {};

    bool discovered : 1 {};
    bool visited : 1 {};

    bool parent_left_of_this : 1 {};
    bool parent_right_of_this : 1 {};
    bool parent_below_this : 1 {};
    bool parent_above_this : 1 {};

public:
    Tile() = default;
    explicit Tile(double weight) : weight(weight), enabled(true) {};

    void enable();
    void enable(double weight);
    void disable();
    bool is_enabled() const;

    double get_weight() const;
    void set_weight(double);

    void reset();

    void discover();
    void visit();
    void undiscover();
    bool is_discovered() const;
    bool is_visited() const;

    void set_distance_to_parent(Distance);
    Distance get_distance_to_parent() const;
};
