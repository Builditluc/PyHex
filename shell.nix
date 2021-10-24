{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    packages = with pkgs; [ python39 python39Packages.npyscreen ];
}
