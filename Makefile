# Applies the Docker configuration for the baseline
docker-baseline:
	docker compose -f ./config/docker-compose.baseline.yml up -d

# Applies the Docker configuration for CUDA MPS
# Note: Make sure the cuda daemon is started (make mps-start) before applying this configuration and stopped (make mps-stop) after testing
docker-mps:
	docker compose -f ./config/docker-compose.mps.yml up -d	

# Starts CUDA MPS on the host maching
mps-start:
	sudo nvidia-cuda-mps-control -d

# Stops the CUDA MPS daemon on the host machine
mps-stop:
	echo quit | sudo nvidia-cuda-mps-control