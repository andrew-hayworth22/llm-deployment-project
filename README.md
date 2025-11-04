# llm-deployment-project
Deploying and benchmarking LLMs within a Kubernetes cluster

## Environment Setup

### Baseline

To start the baseline setup, simply run the docker-baseline make conmmand:

```make docker-baseline```

Note: Make sure the cleanup has been run if another GPU partitioning method was tested.

### CUDA MPS

To run the CUDA MPS setup, first run the command to start up the MPS CUDA daemon:

```make mps-start```

After the daemon has started, you can then run the command to apply the Docker configuration file:

```make docker-mps```

When you are finished testing, be sure to stop the MPS daemon with the following command:

```make mps-stop```

## Running Benchmark

To run the benchmarking suite, run the following command:

```make bench-run```