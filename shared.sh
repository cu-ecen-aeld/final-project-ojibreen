#!/bin/sh
# Shared definitions for buildroot scripts

# The defconfig from the buildroot directory we use for qemu builds
RP4_DEFCONFIG=configs/raspberrypi4_64_defconfig
# The place we store customizations to the qemu configuration
MODIFIED_RP4_DEFCONFIG=base_external/configs/aesd_raspberrypi4_64_defconfig
# The defconfig from the buildroot directory we use for the project
AESD_DEFAULT_DEFCONFIG=${RP4_DEFCONFIG}
AESD_MODIFIED_DEFCONFIG=${MODIFIED_RP4_DEFCONFIG}
AESD_MODIFIED_DEFCONFIG_REL_BUILDROOT=../${AESD_MODIFIED_DEFCONFIG}
