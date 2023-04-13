#include "tile.hpp"

void Tile::enable() {
    enabled = true;
}

void Tile::enable(const double weight) {
    enabled = true;
    this->weight = weight;
}

void Tile::disable() {
    enabled = false;
}

bool Tile::is_enabled() const {
    return enabled;
}

double Tile::get_weight() const {
    return weight;
}

void Tile::set_weight(const double weight) {
    this->weight = weight;
}

void Tile::reset() {
    discovered = false;
    visited = false;
    parent_left_of_this = false;
    parent_right_of_this = false;
    parent_below_this = false;
    parent_above_this = false;
}

void Tile::visit() {
    visited = true;
}

void Tile::discover() {
    discovered = true;
}

void Tile::undiscover() {
    discovered = false;
    visited = false;
}

bool Tile::is_discovered() const {
    return discovered || visited;
}

bool Tile::is_visited() const {
    return visited;
}

void Tile::set_distance_to_parent(const Distance to_parent) {
    parent_left_of_this  = to_parent.dx < 0;
    parent_right_of_this = to_parent.dx > 0;
    parent_below_this    = to_parent.dy < 0;
    parent_above_this    = to_parent.dy > 0;
}

Distance Tile::get_distance_to_parent() const {
    return {
        parent_right_of_this - parent_left_of_this,
        parent_above_this - parent_below_this
    };
}
