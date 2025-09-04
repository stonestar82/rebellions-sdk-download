
#!/bin/bash

# Parameter validation
if [ $# -ne 1 ]; then
	echo "Usage: $0 <device count (1-16)>"
	exit 1
fi

DEVICE_COUNT=$1

# Parameter range validation (1-16)
if [ $DEVICE_COUNT -lt 1 ] || [ $DEVICE_COUNT -gt 16 ]; then
	echo "Error: Device count must be between 1-16."
	exit 1
fi

# Generate device options
DEVICE_OPTIONS=""
for i in $(seq 0 $((DEVICE_COUNT-1))); do
	DEVICE_OPTIONS="$DEVICE_OPTIONS --device /dev/rbln$i"
done

docker run \
			--device /dev/rsd0 \
			$DEVICE_OPTIONS \
			--volume /usr/local/bin/rbln-stat:/usr/local/bin/rbln-stat \
			-ti ubuntu-rebellions:2025.08.29