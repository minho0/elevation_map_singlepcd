# syntax=docker/dockerfile:1.4
###############################################################################
#  Single‑file image that merges:
#    • docker/Dockerfile.x64  (build‑time logic)
#    • devcontainer.json      (runtime env / health‑check hints)
# -----------------------------------------------------------------------------
#  Build:   docker build -f Dockerfile.single -t emcupy-all .
#  Run:     see the runtime hint block at bottom (matches devcontainer.json)
###############################################################################

FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04 AS base

LABEL description="ROS2 Humble + CUDA 12 + Elevation Mapping CUPY (devcontainer merged)" \
      maintainer="mhlee00@inha.edu" \
      version="1.0"

###############################################################################
# -- Build arguments -----------------------------------------------------------
ARG ROS_DISTRO=humble
ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=$USER_UID
ARG RMW_NAME=fastrtps
ARG INSTALL_EMCUPY_ROSDEPS=true
###############################################################################

###############################################################################
# -- Global environment --------------------------------------------------------
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LC_ALL=en_US.UTF-8 \
    TZ=UTC \
    PYTHONUNBUFFERED=1 \
    ROS_DISTRO=${ROS_DISTRO} \
    ROS_ROOT=/opt/ros/${ROS_DISTRO} \
    AMENT_PREFIX_PATH=/opt/ros/${ROS_DISTRO} \
    COLCON_PREFIX_PATH=/opt/ros/${ROS_DISTRO} \
    LD_LIBRARY_PATH=/opt/ros/${ROS_DISTRO}/lib:/usr/local/cuda/lib64 \
    PATH=/opt/ros/${ROS_DISTRO}/bin:/usr/local/cuda/bin:$PATH \
    PYTHONPATH=/opt/ros/${ROS_DISTRO}/lib/python3.10/site-packages \
    RMW_IMPLEMENTATION=rmw_${RMW_NAME}_cpp \
    RMW_IMPLEMENTATION_DASH=rmw-${RMW_NAME}-cpp \
    # devcontainer‑specific defaults
    LIBGL_ALWAYS_SOFTWARE=1 \
    ROS_DOMAIN_ID=0 \
    TURTLEBOT3_MODEL=waffle_realsense_depth
###############################################################################

###############################################################################
# -- Base utilities ------------------------------------------------------------
RUN apt update && apt install -y --no-install-recommends \
        locales tzdata curl gnupg2 lsb-release sudo \
        software-properties-common wget git git-lfs nano \
    && locale-gen ${LANG} \
    && ln -fs /usr/share/zoneinfo/${TZ} /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && apt clean && rm -rf /var/lib/apt/lists/*

###############################################################################
# -- ROS 2 installation --------------------------------------------------------
RUN curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] \
       http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
       > /etc/apt/sources.list.d/ros2.list \
    && apt update && apt install -y --no-install-recommends \
       ros-${ROS_DISTRO}-ros-base \
       python3-argcomplete \
       ros-${ROS_DISTRO}-${RMW_IMPLEMENTATION_DASH} \
       python3-rosdep python3-vcstool \
    && rosdep init && rosdep update \
    && apt clean && rm -rf /var/lib/apt/lists/*

###############################################################################
# -- Dev tools & libs (from original Dockerfile.x64) ---------------------------
RUN apt update && apt install -y --no-install-recommends \
        bash-completion build-essential cmake gdb openssh-client vim \
        doxygen graphviz python3-sphinx python3-breathe ros-dev-tools \
        "ros-${ROS_DISTRO}-ament-*" libxine2-dev libtiff5-dev libpostproc-dev \
        libopencv-dev \
    && apt clean && rm -rf /var/lib/apt/lists/*

###############################################################################
# -- Python / PyTorch ----------------------------------------------------------
RUN apt update && apt install -y python3-pip   \   
    && python3 -m pip install -U pip \
    && python3 -m pip install -U --extra-index-url https://download.pytorch.org/whl/cu121 \
       torch torchvision torchaudio \
    && python3 -m pip install colcon-clean rosdoc2 sphinx_rtd_theme \
       sphinx-multiversion sphinx-copybutton sphinx-tabs autopep8 \
       flake8-builtins flake8-comprehensions flake8-docstrings flake8-import-order \
       flake8-class-newline flake8-blind-except flake8-quotes transforms3d scipy

# extra ecu‑py deps
RUN if [ "$INSTALL_EMCUPY_ROSDEPS" = "true" ]; then \
      python3 -m pip install scikit-learn opencv-python cupy-cuda12x simple-parsing "numpy<2.0.0"; \
    fi

###############################################################################
# -- Elevation Mapping CUPY APT libs ------------------------------------------
RUN if [ "$INSTALL_EMCUPY_ROSDEPS" = "true" ]; then \
      apt update && apt install -y --no-install-recommends \
        libboost-all-dev \
        ros-${ROS_DISTRO}-grid-map-msgs ros-${ROS_DISTRO}-grid-map-ros \
        ros-${ROS_DISTRO}-image-transport ros-${ROS_DISTRO}-pcl-ros \
        ros-${ROS_DISTRO}-cv-bridge ros-${ROS_DISTRO}-tf-transformations \
        ros-${ROS_DISTRO}-rviz2 ros-${ROS_DISTRO}-gazebo-ros \
        ros-${ROS_DISTRO}-grid-map-cv ros-${ROS_DISTRO}-grid-map-core ros-${ROS_DISTRO}-grid-map-demos \
        ros-${ROS_DISTRO}-point-cloud-transport \
        python3-shapely python3-scipy python3-ruamel.yaml \
        ros-${ROS_DISTRO}-camera-calibration-parsers ros-${ROS_DISTRO}-camera-info-manager \
        ros-${ROS_DISTRO}-gazebo-plugins ros-${ROS_DISTRO}-turtlebot3-msgs ros-${ROS_DISTRO}-turtlebot3-teleop \
        ros-${ROS_DISTRO}-gazebo-ros-pkgs \
      && apt clean && rm -rf /var/lib/apt/lists/*; \
    fi

###############################################################################
# -- NVIDIA container toolkit --------------------------------------------------
RUN distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
    && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | apt-key add - \
    && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list \
       > /etc/apt/sources.list.d/nvidia-docker.list \
    && apt update && apt install -y nvidia-container-toolkit \
    && apt clean && rm -rf /var/lib/apt/lists/*

###############################################################################
# -- Non‑root user -------------------------------------------------------------
RUN groupadd --gid ${USER_GID} ${USERNAME} \
    && useradd -m -s /bin/bash --uid ${USER_UID} --gid ${USER_GID} ${USERNAME} \
    && echo "${USERNAME} ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/${USERNAME} \
    && chmod 0440 /etc/sudoers.d/${USERNAME}

###############################################################################
# -- Workspace skeleton --------------------------------------------------------
ARG WORKSPACE=/home/${USERNAME}/workspace
RUN mkdir -p ${WORKSPACE}/src/elevation_mapping_cupy \
    && chown -R ${USERNAME}:${USERNAME} /home/${USERNAME}

# Extra rosdep file symlink (optional)
RUN ln -s ${WORKSPACE}/src/elevation_mapping_cupy/docker/extra_rosdeps.yaml \
    /etc/ros/rosdep/sources.list.d/emcupy-rosdeps.yaml 2>/dev/null || true

###############################################################################
# -- User shell setup ----------------------------------------------------------
RUN echo "source /opt/ros/${ROS_DISTRO}/setup.bash" >> /home/${USERNAME}/.bashrc \
    && echo "if [ -f ${WORKSPACE}/install/setup.bash ]; then source ${WORKSPACE}/install/setup.bash; fi" >> /home/${USERNAME}/.bashrc

WORKDIR ${WORKSPACE}
USER ${USERNAME}

###############################################################################
# -- Health‑check (from devcontainer.json) ------------------------------------
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD ros2 topic list > /dev/null 2>&1 || exit 1

CMD ["bash"]

###############################################################################
# Runtime hint: run with the same flags VS Code devcontainer uses, e.g.
# docker run -it --rm \
#  --network=host --cap-add=SYS_PTRACE --cap-add=SYS_NICE \
#  --security-opt seccomp:unconfined --security-opt apparmor:unconfined \
#  --runtime=nvidia --gpus=all --privileged \
#  --ipc=host --pid=host \
#  --ulimit rtprio=98 --ulimit rttime=-1 --ulimit memlock=8428281856 \
#  --mount type=bind,source=/mnt/wslg,target=/mnt/wslg \
#  --mount type=bind,source=/dev,target=/dev \
#  --env DISPLAY --env WAYLAND_DISPLAY --env XDG_RUNTIME_DIR --env PULSE_SERVER \
#  --name emcupy-ros2-devcontainer-2 \
#  -v $(pwd):/home/ros/workspace/src/elevation_mapping_cupy \
#  emcupy-all
###############################################################################
