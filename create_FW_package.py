# Script from: https://github.com/platformio/platform-espressif32/issues/1078
# creates one .bin file for ESP32 which can be flashed at once
# e.g. C:/Users/ralfk/.platformio/penv/Scripts/python.exe C:/Users/ralfk/.platformio/packages/tool-esptoolpy/esptool.py write_flash 0x0000 C:/_PlatformIO/MobiFlight-FirmwareSource/.pio/build/mobiflight_esp32_s2_mini/mobiflight_esp32_s2_mini_merged_0_0_1.bin

Import("env")

APP_BIN = "$BUILD_DIR/${PROGNAME}.bin"
MERGED_BIN = "$BUILD_DIR/${PROGNAME}_merged.bin"
BOARD_CONFIG = env.BoardConfig()


def merge_bin(source, target, env):
    # The list contains all extra images (bootloader, partitions, eboot) and
    # the final application binary
    flash_images = env.Flatten(env.get("FLASH_EXTRA_IMAGES", [])) + ["$ESP32_APP_OFFSET", APP_BIN]

    # Run esptool to merge images into a single binary
    env.Execute(
        " ".join(
            [
                "$PYTHONEXE",
                "$OBJCOPY",
                "--chip",
                BOARD_CONFIG.get("build.mcu", "esp32"),
                "merge_bin",
                "--fill-flash-size",
                BOARD_CONFIG.get("upload.flash_size", "4MB"),
                "-o",
                MERGED_BIN,
            ]
            + flash_images
        )
    )

# Add a post action that runs esptoolpy to merge available flash images
env.AddPostAction(APP_BIN , merge_bin)

# Patch the upload command to flash the merged binary at address 0x0
#env.Replace(
#    UPLOADERFLAGS=[
#        ]
#        + ["write_flash", "0x0", MERGED_BIN],
#    UPLOADCMD='"$PYTHONEXE" "$UPLOADER" $UPLOADERFLAGS',
#)
