/* Copyright 2024- European Centre for Medium-Range Weather Forecasts (ECMWF)
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     https://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/*
 * This software was developed as part of the EC H2020 funded project IO-SEA
 * (Project ID: 955811) iosea-project.eu
 */

/// @file   Metadata.h
/// @author Metin Cakircali
/// @date   Feb 2024

#pragma once

#include <string>

namespace weather {

struct Metadata {
    std::string user;
    std::string type;
    std::string parameter;
    std::string institute;
    int         level;

    std::string print() const {
        return "institute=" + institute + ",user=" + user + ",type=" + type + ",parameter=" + parameter +
               ",level=" + std::to_string(level);
    }
};

}  // namespace weather
