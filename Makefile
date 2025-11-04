# Applies the Docker configuration for the baseline
docker-baseline-up:
	docker compose -f ./config/docker-compose.baseline.yml up -d

docker-baseline-down:
	docker compose -f docker-compose.baseline.yml down --volumes --remove-orphans

# Applies the Docker configuration for CUDA MPS
# Note: Make sure the cuda daemon is started (make mps-start) before applying this configuration and stopped (make mps-stop) after testing
docker-mps-up:
	docker compose -f ./config/docker-compose.mps.yml up -d	

docker-mps-down:
	docker compose -f docker-compose.mps.yml down --volumes --remove-orphans

# Starts CUDA MPS on the host maching
mps-start:
	sudo nvidia-cuda-mps-control -d

# Stops the CUDA MPS daemon on the host machine
mps-stop:
	echo quit | sudo nvidia-cuda-mps-control