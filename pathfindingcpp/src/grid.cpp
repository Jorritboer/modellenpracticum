#include <cmath>
#include <deque>
#include <queue>
#include <stdexcept>

#include "grid.hpp"

bool Grid::NeighborsView::const_iterator::next_neighbor_candidate() {
    if(current_neighbor == center)
        return false;
    while(true) {
        if(current_neighbor.x <= center.x && current_neighbor.x < grid.dimensions.width - 1) {
            ++current_neighbor.x;
            if(current_neighbor == center)
                continue;
        } else if(current_neighbor.y <= center.y && current_neighbor.y < grid.dimensions.height - 1) {
            ++current_neighbor.y;
            current_neighbor.x = center.x == 0 ? 0 : center.x - 1;
            if(current_neighbor == center)
                continue;
        } else {
            current_neighbor = center;
            return false;
        }
        return true;
    }
}

Point Grid::NeighborsView::const_iterator::operator*() {
    return current_neighbor;
}

void Grid::NeighborsView::const_iterator::find_nearest_neighbor() {
    while(true) {
        const Tile& tile = grid.tiles[grid.index_from_point(current_neighbor)];
        if(tile.is_enabled() && !tile.is_visited())
            return;
        if(!next_neighbor_candidate())
            return;
    }
}

Grid::NeighborsView::const_iterator& Grid::NeighborsView::const_iterator::operator++() {
    next_neighbor_candidate();
    find_nearest_neighbor();
    return *this;
}

bool Grid::NeighborsView::const_iterator::operator==(const Grid::NeighborsView::const_iterator& other) {
    return current_neighbor == other.current_neighbor;
}

Grid::NeighborsView::const_iterator Grid::NeighborsView::begin() {
    Point pos { center.x == 0 ? 0 : center.x - 1, center.y == 0 ? 0 : center.y - 1 };
    if(pos.x == 0 && pos.y == 0) {
        if(grid.dimensions.width > 1)
            pos.x = 1;
        else if(grid.dimensions.height > 1)
            pos.y = 1;
    }
    return { grid, center, pos };
}

Grid::NeighborsView::const_iterator Grid::NeighborsView::end() {
    return { grid, center, center };
}

Grid::NeighborsView Grid::neighbors_at(const Point pos) const {
    return { *this, pos };
}

size_t Grid::index_from_point(const Point pos) const {
    return pos.y * dimensions.height + pos.x;
}

void Grid::alter_weights_using_paths(
    const std::vector<std::vector<Point>>& paths,
    const double multiplier,
    const size_t radius
) {
    std::deque<std::pair<Point, size_t>> visit_queue {};
    for(const std::vector<Point>& path : paths)
        for(const Point pos : path) {
            tiles[index_from_point(pos)].visit();
            visit_queue.push_back({ pos, 0 });
        }

    while(visit_queue.size() > 0) {
        auto [ pos, distance ] = visit_queue.front();
        visit_queue.pop_front();

        Tile& tile = tiles[index_from_point(pos)];
        tile.set_weight(
            tile.get_weight() * std::lerp(multiplier, 1.0, static_cast<double>(distance) / static_cast<double>(radius))
        );
        
        if(distance >= radius)
            continue;

        for(const Point neighbor_pos : neighbors_at(pos)) {
            tiles[index_from_point(neighbor_pos)].visit();
            visit_queue.push_back({ neighbor_pos, distance + 1 });
        }
    }
}

Grid::Dimensions Grid::get_dimensions() const {
    return dimensions;
}

void Grid::set_tile_data_at(const Point pos, const TileData& data) {
    tile_data[index_from_point(pos)] = data;
}

void Grid::reset() {
    for(Tile& tile : tiles)
        tile.reset();
    path_finding_has_run = false;
}

void Grid::enable_tile_at(const Point pos) {
    tiles[index_from_point(pos)].enable();
}

double Grid::heuristic(const Point from, const Point to, const Grid::PathFindingOptions& options) const {
    return (to - from).norm() * options.path_cost_per_unit;
}

std::optional<std::vector<Point>> Grid::find_path(const Point from, const Point to, const Grid::PathFindingOptions& options) {
    if(options.path_cost_per_unit < 0.0)
        throw std::invalid_argument("Path cost per unit must be nonnegative");

    if(path_finding_has_run)
        reset();
    path_finding_has_run = true;

    const size_t from_index = index_from_point(from);
    const size_t to_index = index_from_point(to);

    for(size_t i = 0; i < tiles.size(); ++i)
        if(tiles[i].is_enabled())
            tiles[i].set_weight(tile_data[i].get_weight_from_attributes(options.attribute_weights));

    if(options.existing_paths.size() > 0) {
        if(options.existing_path_multiplier < 1.0)
            throw std::invalid_argument("Existing path mutiplier must be at least 1");
        alter_weights_using_paths(options.existing_paths, options.existing_path_multiplier, options.existing_path_radius);
        for(Tile& tile : tiles)
            tile.undiscover();
    }

    struct QueueElem {
        Point pos;
        size_t index;
        double length;
        double cost;
        std::optional<Point> parent;
    };
    const auto cost_compare = [](const QueueElem& a, const QueueElem& b) -> bool { return a.cost > b.cost; };
    std::priority_queue<QueueElem, std::vector<QueueElem>, decltype(cost_compare)> visit_queue { cost_compare };
    visit_queue.push({
        from,
        from_index,
        0.0,
        tiles[from_index].get_weight() + heuristic(from, to, options),
        {}
    });

    while(!visit_queue.empty()) {
        QueueElem elem = visit_queue.top();
        visit_queue.pop();

        if(tiles[elem.index].is_visited())
            continue;
        if(options.max_path_length.has_value() && elem.length > options.max_path_length.value())
            continue;

        if(elem.parent.has_value())
            tiles[elem.index].set_distance_to_parent(elem.pos - elem.parent.value());
        tiles[elem.index].visit();

        if(elem.index == to_index)
            return get_path_to(to);

        for(const Point neighbor_pos : neighbors_at(elem.pos)) {
            const size_t neighbor_index = index_from_point(neighbor_pos);
            const double distance = (neighbor_pos - elem.pos).norm();
            const double cost = elem.cost
                + tiles[neighbor_index].get_weight()
                - heuristic(elem.pos, to, options)
                + heuristic(neighbor_pos, to, options)
                + distance * options.path_cost_per_unit;
            tiles[neighbor_index].discover();
            visit_queue.push({
                neighbor_pos,
                neighbor_index,
                elem.length + distance,
                cost,
                elem.pos
            });
        }
    }

    return {};
}

std::vector<Point> Grid::get_path_to(const Point to) {
    std::vector<Point> rev_path { to };
    Point current = to;
    Distance parent_distance;
    while((parent_distance = tiles[index_from_point(current)].get_distance_to_parent()) != Distance { 0, 0 }) {
        current -= parent_distance;
        rev_path.push_back(current);
    }
    return { rev_path.rbegin(), rev_path.rend() };
}
