import asyncio
from aiohttp import web
import RPi.GPIO as GPIO

# Konfiguracja GPIO
GPIO.setmode(GPIO.BCM)
GPIO_PIN = 18
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

async def check_gpio():
    try:
        # Odczyt stanu pinu - jeśli zwróci False, oznacza to zwarty obwód (GND)
        return not GPIO.input(GPIO_PIN)
    except Exception as e:
        print(f"Błąd odczytu GPIO: {e}")
        return False

async def handle_request(request):
    is_connected = await check_gpio()
    status = "GPIO 18 i GND są zwarte" if is_connected else "GPIO 18 i GND nie są zwarte"
    response_data = {
        "gpio_18_connected_to_gnd": is_connected,
        "status": status
    }
    return web.json_response(response_data)

async def on_shutdown(app):
    GPIO.cleanup()

async def create_app():
    app = web.Application()
    app.router.add_get('/', handle_request)
    app.on_shutdown.append(on_shutdown)
    return app

if __name__ == '__main__':
    try:
        print("Starting server...")
        print("Aby sprawdzić stan, otwórz http://localhost:8080 w przeglądarce")
        print("Naciśnij Ctrl+C aby zatrzymać serwer")
        
        loop = asyncio.get_event_loop()
        app = loop.run_until_complete(create_app())
        web.run_app(app, port=8080)
    except KeyboardInterrupt:
        print("Zamykanie serwera...")
    finally:
        GPIO.cleanup()
