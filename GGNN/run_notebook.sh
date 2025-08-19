#!/bin/bash

read -p "Do you really want to start the script? (y/n):" answer
if [[ "$answer" == "y" ]]; then
echo "Starting the script..."
else echo "Exiting..."
exit 1
fi

NOTEBOOK_NAME="GGNN_model.ipynb"
OUTPUT_DIR="run_out_HIV"
OUTPUT_NOTEBOOK="$OUTPUT_DIR/GGNN_tune1_out1.ipynb"
LOG_FILE="$OUTPUT_DIR/run_GGNN.log"

mkdir -p "$OUTPUT_DIR"
echo "Saving all outputs into: $OUTPUT_DIR"

echo "Running the notebook in the background"
nohup papermill "$NOTEBOOK_NAME" "$OUTPUT_NOTEBOOK" > "$LOG_FILE" 2>&1 &

echo "The notebook is now running in the background"
echo "The progress will be saved in: $LOG_FILE"
echo "When it's done, open $OUTPUT_NOTEBOOK (in jupyter) to see the outputs"


