#pragma once

#include <type_traits>

template<class C, class T>
concept Container = std::is_same_v<typename C::value_type, T>;
