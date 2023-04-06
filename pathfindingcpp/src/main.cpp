#include <bitset>
#include <chrono>
#include <iostream>
#include <thread>

#include "attributes.hpp"
#include "grid.hpp"

int main(int argc, char* argv[]) {
    Grid g { { 3000, 3000 } };
    const auto dimensions = g.get_dimensions();

    for(size_t y = 0; y < dimensions.height; ++y)
        for(size_t x = 0; x < dimensions.width; ++x) {
            Attributes attributes {};
            if(x % 2)
                attributes.set(Attribute::Road);
            if(y % 2)
                attributes.set(Attribute::Water);
            g.set_tile_data_at({ x, y }, { attributes });
        }

    std::vector<TileData::AttributeWeightMapping> mapping {
        { Attribute::Road, 2 },
        { Attribute::Water, 5 },
    };

    for(size_t y = 0; y < dimensions.height; ++y)
        for(size_t x = 0; x < dimensions.width; ++x)
            //if(x == 0 || y == dimensions.height - 1)
            g.enable_tile_at({ x, y });

    std::cout << "Running for a " << dimensions.width << "x" << dimensions.height << " grid.." << std::endl;

    std::optional<std::vector<Point>> path = g.find_path(
        { 0, 0 },
        { dimensions.width - 1, dimensions.height - 1 },
        {
            .max_path_length = 5000,
            .path_cost_per_unit = 1,
            .existing_paths = {},
            .attribute_weights = mapping,
            .existing_path_multiplier = 1,
            .existing_path_radius = 0
        }
    );

    if(path.has_value()) {
        std::cout << "Found path:";
        for(const Point pos : path.value())
            std::cout << " (" << pos.x << ", " << pos.y << ")";
        std::cout << std::endl;
    } else
        std::cout << "No path found" << std::endl;

    return 0;
}
