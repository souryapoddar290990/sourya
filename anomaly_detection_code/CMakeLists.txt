cmake_minimum_required(VERSION 3.6)
project(anomaly_detection_code)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
    code/AnomalyDetection.cpp
    code/AnomalyDetection.h
    code/CascadedBgsParams.h
    code/DisplayImage.cpp
    code/DisplayImage.h
    code/inc.h
    code/inputs.h
    code/k_nearest_neighbours_meat.hpp
    code/k_nearest_neighbours_proto.hpp
    code/main.cpp
    code/main.h
    code/ParameterInfo.cpp
    code/ParameterInfo.h
    code/SequentialBgeParams.h)

add_executable(anomaly_detection_code ${SOURCE_FILES})