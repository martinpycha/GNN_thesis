#!/bin/bash

read -p "Do you really want to start the script? (y/n):" answer
if [[ "$answer" != "y" ]]; then
    echo "Exiting..."
    exit 1
fi

NOTEBOOK_NAME="GraphSAGE_model.ipynb"
OUTPUT_DIR="run_out_hERG"
mkdir -p "$OUTPUT_DIR"

echo "Running 10 notebook executions sequentially..."

for i in {9..10}
do
    OUTPUT_NOTEBOOK="$OUTPUT_DIR/GraphSAGE_out${i}.ipynb"
    LOG_FILE="$OUTPUT_DIR/run_GraphSAGE_${i}.log"

    echo "Starting run $i..."
    papermill "$NOTEBOOK_NAME" "$OUTPUT_NOTEBOOK" -p run_number "$i" > "$LOG_FILE" 2>&1

    echo "Finished run $i"
done

echo "All runs completed."
