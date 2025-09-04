#!/bin/bash
echo "================================================"
echo "resnet50 compile"
echo "================================================"
echo ""
echo "> python compile.py"
python compile.py


# Check compilation result
if [ $? -ne 0 ]; then
    echo "Compilation failed"
    exit 1
fi

echo ""

echo "================================================"
echo "resnet50 inference"
echo "================================================"

# JSON data (in actual use, parse the result of rbln-stat command)
JSON_DATA=$(rbln-stat --json)

# Get the length of devices array using jq
DEVICE_COUNT=$(echo "$JSON_DATA" | jq '.devices | length')

echo "Number of devices found: $DEVICE_COUNT"

# Run inference.py for each device
for i in $(seq 0 $((DEVICE_COUNT-1))); do
    echo "> RBLN_DEVICES=$i python inference.py"
    RBLN_DEVICES=$i python inference.py
    
    # Check execution result
    if [ $? -ne 0 ]; then
        echo "Inference failed on device $i"
    fi
    echo ""
done


echo "================================================"
echo "resnet50 inference completed"
echo "================================================"

