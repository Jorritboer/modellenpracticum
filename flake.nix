{
  description = "Modellenpracticum";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = inputs@{ self, nixpkgs, flake-utils, ... }:
  flake-utils.lib.eachDefaultSystem (system:
  let
    pkgs = nixpkgs.legacyPackages.${system};
    pythonPackages = pkgs.python3Packages;
    python = pythonPackages.python;
  in {
    packages.default = pkgs.gdal;
    devShell = pkgs.mkShell {
      buildInputs = [
        pkgs.gdal
        pkgs.qgis
        (python.withPackages (ps:
        with ps; [
          python-lsp-server
          autopep8
          flake8
          pylint
          black
          geopandas
          numpy
          gdal
        ]))
      ];
    };
  });
}
