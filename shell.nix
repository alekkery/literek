# shell.nix
{ pkgs ? import <nixpkgs> { } }:

let
  python = pkgs.python3.withPackages (ps: [
#     ps.numpy
#     (ps.opencv4.override { enableGtk2 = true; })
#     ps.pygame
#     ps.rich
#     ps.keras
#     ps.tensorflow-bin
  ]);
in
pkgs.mkShell {
  packages = [ python ];

  LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath [
    pkgs.stdenv.cc.cc.lib
    pkgs.zlib
    pkgs.glib
    pkgs.libGL
    pkgs.libxcb
    pkgs.libX11
    pkgs.libXext
    pkgs.libXrender
    pkgs.libSM
    pkgs.libICE

    # SDL, pygame
    pkgs.libXcursor
    pkgs.libXi
    pkgs.libXrandr
    pkgs.libXfixes
    pkgs.wayland
    pkgs.libxkbcommon
    pkgs.alsa-lib
    pkgs.libpulseaudio
  ];
}