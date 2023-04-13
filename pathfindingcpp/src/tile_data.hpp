#pragma once

#include <type_traits>
#include <utility>

#include "attributes.hpp"
#include "container.hpp"

class TileData {
public:
    struct AttributeWeightMapping {
        Attribute attribute;
        double weight;
    };

    Attributes attributes {};

    double get_weight_from_attributes(const Container<AttributeWeightMapping> auto& attribute_weights) const {
        double total_weight { 1 };
        for(const auto [attribute, weight] : attribute_weights)
            if(attributes.test(attribute))
                total_weight *= weight;
        return total_weight;
    }
};
