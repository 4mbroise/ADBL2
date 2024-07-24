#!/bin/sh

huggingface-cli login --token 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

# apt update -y
# apt upgrade -y
# apt install wget -y

# apt remove --purge *nvidia*
# apt remove --purge* cuda*
# apt autoremove -y


# wget https://developer.download.nvidia.com/compute/cuda/12.5.0/local_installers/cuda_12.5.0_555.42.02_linux.run
# sh cuda_12.5.0_555.42.02_linux.run


exec "$@"
