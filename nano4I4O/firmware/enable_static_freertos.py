"""Enable static tasks in the installed feilipu FreeRTOS config.

The published header turns static allocation off. Checkout images use
xTaskCreateStatic and xQueueCreateStatic, and they turn the timer task
off so the ATmega328P keeps enough SRAM for two tasks.
"""

import re
from pathlib import Path

Import("env")  # noqa: F821  PlatformIO injects this name.

LIBDEPS = Path(env["PROJECT_LIBDEPS_DIR"])  # noqa: F821
STATIC = re.compile(
    r"#define\s+configSUPPORT_STATIC_ALLOCATION\s+0",
)
TIMERS = re.compile(
    r"#define\s+configUSE_TIMERS\s+1",
)


def enable_static(header: Path) -> None:
    """Rewrite one installed FreeRTOSConfig.h."""
    text = header.read_text(encoding="utf-8")
    updated = TIMERS.sub(
        "#define configUSE_TIMERS 0",
        STATIC.sub(
            "#define configSUPPORT_STATIC_ALLOCATION 1",
            text,
        ),
    )
    if updated != text:
        header.write_text(updated, encoding="utf-8")


if LIBDEPS.is_dir():
    for config in LIBDEPS.rglob("FreeRTOSConfig.h"):
        enable_static(config)
