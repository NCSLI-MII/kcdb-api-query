#! /bin/sh
#
# combine.sh
# Copyright (C) 2022 Ryan Mackenzie White <ryan.white@nrc-cnrc.gc.ca>
#
# Distributed under terms of the Copyright © 2022 National Research Council Canada. license.
#



head -n 1 kcdb_cmc_AUV.csv > physics_kcdb_cmc.csv && tail -n +2 -q kcdb_cmc_*.csv >> physics_kcdb_cmc.csv
