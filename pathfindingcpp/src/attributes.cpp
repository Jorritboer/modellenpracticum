#include "attributes.hpp"

void Attributes::set(const Attribute attribute) {
    attributes |= static_cast<uint64_t>(attribute);
}

void Attributes::unset(const Attribute attribute) {
    attributes &= ~static_cast<uint64_t>(attribute);
}

bool Attributes::test(const Attribute attribute) const {
    return attributes & static_cast<uint64_t>(attribute);
}
