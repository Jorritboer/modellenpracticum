#pragma once

#include <cinttypes>

enum class Attribute : uint64_t {
    Road  = 0x0000000000000000000000000000000000000000000000000000000000000001,
    Water = 0x0000000000000000000000000000000000000000000000000000000000000010,
};

class Attributes {
private:
    uint64_t attributes {};

public:
    Attributes() = default;
    Attributes(const Attribute attribute) : attributes(static_cast<uint64_t>(attribute)) {}

    Attributes(const Attributes&) = default;
    Attributes& operator=(const Attributes&) = default;

    void set(Attribute);
    void unset(Attribute);

    bool test(Attribute) const;

};
