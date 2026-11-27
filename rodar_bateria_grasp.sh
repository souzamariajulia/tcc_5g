#!/usr/bin/env bash

cd -- "$(dirname -- "${BASH_SOURCE[0]}")" || exit 1

sementes=(
    141592 653589 793238 462643 383279
    502884 197169 399375 105820 974944
    592307 816406 286208 998628 34825
    342117 67982 148086 513282 306647
    93844 609550 582231 725359 408128
    481117 450284 102701 938521 105559
)

for instancia in instancias/*.txt; do
    for semente in "${sementes[@]}"; do
        python main_grasp.py "$instancia" "$semente" || exit 1
    done
done
