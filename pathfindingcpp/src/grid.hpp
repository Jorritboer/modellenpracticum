#include <cstddef>
#include <iterator>
#include <optional>
#include <stdexcept>
#include <vector>

#include "container.hpp"
#include "tile.hpp"
#include "tile_data.hpp"

class Grid {
public:
    struct Dimensions {
        std::size_t width;
        std::size_t height;
    };

    struct PathFindingOptions {
        std::optional<double> max_path_length {};
        double path_cost_per_unit { 1 };
        std::vector<std::vector<Point>> existing_paths {};
        std::vector<TileData::AttributeWeightMapping> attribute_weights {};
        double existing_path_multiplier { 1 };
        size_t existing_path_radius {};
    };

    class NeighborsView {
    private:
        const Grid& grid;
        const Point center;

    public:
        class const_iterator {
            friend class Grid;

        private:
            const Grid& grid;
            const Point center;
            Point current_neighbor; // If equal to center, this is the end iterator

            void find_nearest_neighbor();
            bool next_neighbor_candidate();

        public:
            using iterator_concept = std::forward_iterator_tag;
            using value_type = Point;

            const_iterator(
                const Grid& grid,
                const Point center,
                const Point current_neighbor
            ): grid(grid), center(center), current_neighbor(current_neighbor) {
                find_nearest_neighbor();
            }

            Point operator*();
            const_iterator& operator++();
            bool operator==(const const_iterator&);
        };

        NeighborsView(const Grid& grid, const Point center): grid(grid), center(center) {}

        const_iterator begin();
        const_iterator end();
    };

private:
    Dimensions dimensions;

    std::vector<TileData> tile_data {};
    std::vector<Tile> tiles {};

    bool path_finding_has_run {};

    NeighborsView neighbors_at(Point) const;
    size_t index_from_point(Point) const;
    void alter_weights_using_paths(const std::vector<std::vector<Point>>& paths, double multiplier, size_t radius);
    void unvisited_neighbors(Point) const;

public:
    explicit Grid(Dimensions dimensions) : dimensions(dimensions) {
        if(dimensions.width < 1 || dimensions.height < 1)
            throw std::invalid_argument("Grid must be at least 1x1");

        const size_t elements = dimensions.width * dimensions.height;
        tile_data.reserve(elements);
        tiles.reserve(elements);

        for(size_t i = 0; i < elements; ++i) {
            tile_data.emplace_back();
            tiles.emplace_back();
        }
    }

    Dimensions get_dimensions() const;

    void set_tile_data_at(Point, const TileData&);

    void reset();

    void enable_tile_at(Point);
    void disable_tile_at(Point);

    double heuristic(Point from, Point to, const PathFindingOptions& options) const;

    std::optional<std::vector<Point>> find_path(Point from, Point to, const PathFindingOptions& options);
    std::vector<Point> get_path_to(Point);
};
