# SSL Metrics Badges

> Convert PNG graphs into GitHub compatable badges

[![Publish to PyPi](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-badges/actions/workflows/pypi.yml/badge.svg)](https://github.com/SoftwareSystemsLaboratory/ssl-metrics-badges/actions/workflows/pypi.yml)

![Example](tests/badge.svg)

## Table of Contents

- [SSL Metrics Badges](#ssl-metrics-badges)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [How to Install](#how-to-install)
  - [How to Run](#how-to-run)
    - [Note on Colors](#note-on-colors)

## About

A script to convert graphs (or other `.png` files 😉) into GitHub compatible `.svg` badges.

## How to Install

0. Install `Python 3.9.6 +`
1. `pip install ssl-metrics-badges`

## How to Run

0. `ssl-metrics-badges -h` to view the command line arguements
1. `ssl-metrics-badges --graph GRAPH.png --left-color COLOR --left-text "LEFT TEXT" --link URL --output FILE.svg --right-text "RIGHT TEXT" --right-color COLOR --title TITLE`

### Note on Colors

Colors can either be phonetically called (such as **red**, **blue**, or **green**) or through hex codes (#123456).
