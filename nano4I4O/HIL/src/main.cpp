/**
 * @relation(SDD-001, scope=file)
 * @relation(SDD-004, scope=file)
 * @relation(IRS-002, scope=file)
 * @relation(IRS-003, scope=file)
 * @relation(IRS-004, scope=file)
 * @relation(SRS-006, scope=file)
 *
 * Checkout image for one Arduino Nano. NANO4I4O_ROLE_READ samples D2-D5
 * and prints frames. NANO4I4O_ROLE_DRIVE walks those pins and stays silent.
 * The feilipu AVR port ticks about every 16 ms, so a requested 10 ms
 * settle waits one tick and a 50 ms hold waits the remaining ticks.
 */
#include <Arduino.h>
#include <Arduino_FreeRTOS.h>
#include <queue.h>
#include <stdint.h>

#if !defined(NANO4I4O_ROLE_READ) && !defined(NANO4I4O_ROLE_DRIVE)
#error Define NANO4I4O_ROLE_READ or NANO4I4O_ROLE_DRIVE
#endif

static const uint8_t CHECKOUT_PINS[] = {2, 3, 4, 5};
static const uint8_t CHECKOUT_PIN_COUNT = 4;
static const uint8_t WALK[][4] = {
    {0, 0, 0, 1},
    {0, 0, 1, 0},
    {0, 1, 0, 0},
    {1, 0, 0, 0},
    {1, 1, 1, 0},
    {1, 1, 0, 1},
    {1, 0, 1, 1},
    {0, 1, 1, 1},
};
static const uint8_t WALK_LENGTH = 8;
static const uint16_t SETTLE_MS = 10;
static const uint16_t HOLD_MS = 50;
static const uint16_t SAMPLE_MS = 20;
static const unsigned long SERIAL_BAUD = 115200;
static const uint16_t IO_STACK_WORDS = 96;
static const uint16_t SERIAL_STACK_WORDS = 128;
static const UBaseType_t SAMPLE_QUEUE_LENGTH = 4;

#if defined(NANO4I4O_ROLE_READ)
static QueueHandle_t sample_queue = NULL;
static StaticQueue_t sample_queue_buffer;
static uint8_t sample_queue_storage[SAMPLE_QUEUE_LENGTH * sizeof(uint8_t)];
#endif

static StaticTask_t io_task_buffer;
static StackType_t io_stack[IO_STACK_WORDS];
static StaticTask_t serial_task_buffer;
static StackType_t serial_stack[SERIAL_STACK_WORDS];
static StaticTask_t idle_task_buffer;
static StackType_t idle_stack[configMINIMAL_STACK_SIZE];

static void delay_at_least(uint16_t milliseconds) {
    TickType_t ticks = pdMS_TO_TICKS(milliseconds);
    if (ticks == 0) {
        ticks = 1;
    }
    vTaskDelay(ticks);
}

static void configure_pins(uint8_t mode) {
    uint8_t index;
    for (index = 0; index < CHECKOUT_PIN_COUNT; index++) {
        pinMode(CHECKOUT_PINS[index], mode);
    }
}

#if defined(NANO4I4O_ROLE_DRIVE)
static void drive_levels(const uint8_t levels[4]) {
    uint8_t index;
    for (index = 0; index < CHECKOUT_PIN_COUNT; index++) {
        digitalWrite(CHECKOUT_PINS[index], levels[index] ? HIGH : LOW);
    }
}
#endif

#if defined(NANO4I4O_ROLE_READ)
static uint8_t sample_levels(void) {
    uint8_t packed = 0;
    uint8_t index;
    for (index = 0; index < CHECKOUT_PIN_COUNT; index++) {
        if (digitalRead(CHECKOUT_PINS[index]) == HIGH) {
            packed = (uint8_t)(packed | (uint8_t)(1U << index));
        }
    }
    return packed;
}

static void print_frame(uint8_t packed) {
    static const char *pin_names[4] = {"D2", "D3", "D4", "D5"};
    uint8_t index;
    Serial.print("READY\n");
    for (index = 0; index < CHECKOUT_PIN_COUNT; index++) {
        Serial.print("SAMPLE ");
        Serial.print(pin_names[index]);
        Serial.print(" ");
        Serial.print((packed >> index) & 1U);
        Serial.print("\n");
    }
    Serial.print("DONE\n");
}
#endif

static void io_task(void *argument) {
    (void)argument;
#if defined(NANO4I4O_ROLE_DRIVE)
    uint8_t step;
    configure_pins(OUTPUT);
    for (;;) {
        for (step = 0; step < WALK_LENGTH; step++) {
            drive_levels(WALK[step]);
            delay_at_least(SETTLE_MS);
            delay_at_least((uint16_t)(HOLD_MS - SETTLE_MS));
        }
    }
#else
    configure_pins(INPUT);
    for (;;) {
        uint8_t packed = sample_levels();
        (void)xQueueSend(sample_queue, &packed, 0);
        delay_at_least(SAMPLE_MS);
    }
#endif
}

static void serial_task(void *argument) {
    (void)argument;
#if defined(NANO4I4O_ROLE_READ)
    for (;;) {
        uint8_t packed = 0;
        if (xQueueReceive(sample_queue, &packed, portMAX_DELAY) == pdPASS) {
            print_frame(packed);
        }
    }
#else
    for (;;) {
        delay_at_least(1000);
    }
#endif
}

extern "C" void vApplicationGetIdleTaskMemory(
    StaticTask_t **idle_tcb,
    StackType_t **idle_stack_memory,
    configSTACK_DEPTH_TYPE *idle_stack_depth) {
    *idle_tcb = &idle_task_buffer;
    *idle_stack_memory = idle_stack;
    *idle_stack_depth = configMINIMAL_STACK_SIZE;
}

void setup() {
#if defined(NANO4I4O_ROLE_READ)
    Serial.begin(SERIAL_BAUD);
    sample_queue = xQueueCreateStatic(
        SAMPLE_QUEUE_LENGTH,
        sizeof(uint8_t),
        sample_queue_storage,
        &sample_queue_buffer);
#endif
    (void)xTaskCreateStatic(
        io_task,
        "io",
        IO_STACK_WORDS,
        NULL,
        2,
        io_stack,
        &io_task_buffer);
    (void)xTaskCreateStatic(
        serial_task,
        "ser",
        SERIAL_STACK_WORDS,
        NULL,
        1,
        serial_stack,
        &serial_task_buffer);
    vTaskStartScheduler();
}

void loop() {}
