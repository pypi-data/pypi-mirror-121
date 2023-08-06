#!/usr/bin/env bash

echo "$BUILDKITE_PARALLEL_JOB"
echo "$BUILDKITE_PARALLEL_JOB_COUNT"

set -euox pipefail

cp -a /upstream /workdir

export HOME=/workdir && cd $HOME && bash .buildkite/scripts/install_bagua.sh || exit 1

echo "begin to test [communication_primitives]"
COMMUNICATION_SCRIPT="/workdir/examples/communication_primitives/main.py"
python -m bagua.distributed.launch \
    --nnodes=2 \
    --nproc_per_node 4 \
    --node_rank=1 \
    --master_addr="10.158.66.134" \
    --master_port=1234 \
    ${COMMUNICATION_SCRIPT}

SYNTHETIC_SCRIPT="/workdir/examples/benchmark/synthetic_benchmark.py"
algorithms=(gradient_allreduce bytegrad decentralized low_precision_decentralized async)
length=${#algorithms[@]}
for ((i=0;i<$length;i++))
do
    echo "begin to test ["${algorithms[$i]}]
    logfile=$(mktemp /tmp/bagua_benchmark_${algorithms[$i]}.XXXXXX.log)
    GLOO_SOCKET_IFNAME=enp96s0f0 python -m bagua.distributed.launch \
        --nnodes=2 \
        --nproc_per_node 4 \
        --node_rank=1 \
        --master_addr="10.158.66.134" \
        --master_port=1234 \
        ${SYNTHETIC_SCRIPT} \
        --num-iters 100 \
        --algorithm ${algorithms[$i]} \
        --deterministic \
        --async-sync-interval 100 \
        --async-warmup-steps 100 \
        2>&1 | tee ${logfile}
done
