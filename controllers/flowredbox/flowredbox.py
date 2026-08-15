from controller import Robot

robot = Robot()
TIME_STEP = int(robot.getBasicTimeStep())

# --------------------------------------------------
# Motors
# --------------------------------------------------
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")

left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))

# --------------------------------------------------
# Camera
# --------------------------------------------------
camera = robot.getDevice("camera")
camera.enable(TIME_STEP)

width = camera.getWidth()
height = camera.getHeight()

# --------------------------------------------------
# Parameters
# --------------------------------------------------

MAX_SPEED = 6.28

# سرعت جستجو
SEARCH_SPEED = 1.0

# سرعت چرخش برای پیدا کردن مرکز هدف
TURN_SPEED = 1.5

# سرعت حرکت مستقیم
FORWARD_SPEED = 2.0

# حداقل تعداد پیکسل قرمز
MIN_RED_PIXELS = 15

# محدوده‌ای که هدف را "وسط" حساب می‌کنیم
DEAD_ZONE = 0.20


# --------------------------------------------------
# Main loop
# --------------------------------------------------

while robot.step(TIME_STEP) != -1:

    image = camera.getImage()

    red_count = 0
    red_x = 0

    # ----------------------------------------------
    # Detect red
    # ----------------------------------------------

    for y in range(height):
        for x in range(width):

            r = camera.imageGetRed(
                image, width, x, y
            )

            g = camera.imageGetGreen(
                image, width, x, y
            )

            b = camera.imageGetBlue(
                image, width, x, y
            )

            # رنگ قرمز مخصوص محیط فعلی شما
            if (
                r > 50
                and r > g * 1.8
                and r > b * 1.8
            ):
                red_count += 1
                red_x += x

    # ==================================================
    # CASE 1: Target NOT found
    # ==================================================

    if red_count < MIN_RED_PIXELS:

        print("SEARCHING... red =", red_count)

        # چرخش آرام درجا
        left_motor.setVelocity(-SEARCH_SPEED)
        right_motor.setVelocity(SEARCH_SPEED)

    # ==================================================
    # CASE 2: Target FOUND
    # ==================================================

    else:

        center_x = red_x / red_count

        error = (
            center_x - width / 2
        ) / (width / 2)

        print(
            f"TARGET | pixels={red_count} "
            f"x={center_x:.1f} "
            f"error={error:.2f}"
        )

        # ----------------------------------------------
        # Target LEFT
        # ----------------------------------------------

        if error < -DEAD_ZONE:

            print("TURN LEFT")

            left_motor.setVelocity(-TURN_SPEED)
            right_motor.setVelocity(TURN_SPEED)

        # ----------------------------------------------
        # Target RIGHT
        # ----------------------------------------------

        elif error > DEAD_ZONE:

            print("TURN RIGHT")

            left_motor.setVelocity(TURN_SPEED)
            right_motor.setVelocity(-TURN_SPEED)

        # ----------------------------------------------
        # Target CENTER
        # ----------------------------------------------

        else:

            print("TARGET CENTER -> FORWARD")

            left_motor.setVelocity(FORWARD_SPEED)
            right_motor.setVelocity(FORWARD_SPEED)