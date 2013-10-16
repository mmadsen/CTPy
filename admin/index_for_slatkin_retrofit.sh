#!/bin/sh

experiment = $1
hostname = ${2:-localhost}
port = ${3:-27017}

connect_prefix = "$hostname:$port/$experiment"
connection = "$connect_prefix_samples_postclassification"

mongo $connection < db/retrofit_slatkin_index.js
