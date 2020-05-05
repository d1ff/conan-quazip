from conans import ConanFile, CMake, tools


class QuazipConan(ConanFile):
    name = "quazip"
    version = "0.8.1"
    license = "LGPL"
    author = "Vladislav Bortnikov facepalmlite@gmail.com"
    url = "https://github.com/d1ff/quazip-conan"
    description = "QuaZIP is the C++ wrapper for Gilles Vollant's ZIP/UNZIP package (AKA Minizip) using Trolltech's Qt library."
    topics = ("compress",)
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": True}
    generators = "cmake"
    requires = ("qt/5.14.2@d1ff/stable", "zlib/1.2.11")

    def source(self):
        self.run("git clone --branch v0.8.1 https://github.com/stachenov/quazip.git")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("quazip/CMakeLists.txt", "project(QuaZip)",
                              '''PROJECT(QuaZip)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')
        tools.replace_in_file("quazip/CMakeLists.txt", "add_subdirectory(quazip)",
                              '''find_package(ZLIB REQUIRED)
                              add_subdirectory(quazip)''')

    def build(self):
        cmake = CMake(self)
        cmake.verbose = True
        
        cmake.configure(source_folder="quazip")
        cmake.build(target='quazip5')
        
    def package(self):
        cmake = CMake(self)
        cmake.verbose = True
        cmake.configure(source_folder="quazip")
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["qt5quazip"]

