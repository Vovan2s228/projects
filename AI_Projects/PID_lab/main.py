import math
import time
from collections import deque

import pygame
import pid
from utils import scale_image, blit_rotate_center, blit_text_center  # keep if you use text overlays

# ================== CONFIG ==================
pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
debug = False

wind = True
steer_bias = True

FrameHeight = 400
FrameWidth = 1200

pygame.display.set_caption("PID controller simulation")
screen = pygame.display.set_mode((FrameWidth, FrameHeight))

bg = pygame.image.load("background_small.png").convert()
RED_CAR = scale_image(pygame.image.load("imgs/red-car_small.png"), 1.0)

MAIN_FONT = pygame.font.SysFont("courier", 35)

# ===== Metrics configuration (for CV) =====
EPS_CTE = 5.0          # settling band in pixels
SETTLE_FRAMES = 45     # ~0.75 s at 60 FPS

# ===== Metrics state =====
metrics = {
	"frames": 0,
	"t_start": time.perf_counter(),
	"cte_abs_sum": 0.0,      # for mean|CTE|
	"cte_sq_sum": 0.0,       # for RMSE
	"cte_max_abs": 0.0,
	"cte_last": None,
	"zero_crossings": 0,     # optional, not printed in final summary
	"settled": False,
	"settle_frame": None,
	"settle_window": deque(maxlen=SETTLE_FRAMES),
	"u_abs_sum": 0.0,        # mean|u|
	"u_sq_sum": 0.0,         # mean(u^2)
	"fps_sum": 0.0,
	"frame_time_sum": 0.0,   # seconds
	"oob": 0
}

def update_metrics(current_cte: float, control_u: float, fps_now: float):
	"""Update aggregate metrics once per frame."""
	# counts & timing
	metrics["frames"] += 1
	metrics["fps_sum"] += fps_now
	metrics["frame_time_sum"] += 1.0 / max(fps_now, 1e-6)

	# error stats
	abs_cte = abs(current_cte)
	metrics["cte_abs_sum"] += abs_cte
	metrics["cte_sq_sum"] += current_cte * current_cte
	if abs_cte > metrics["cte_max_abs"]:
		metrics["cte_max_abs"] = abs_cte

	# zero crossings (optional)
	if metrics["cte_last"] is not None and (metrics["cte_last"] * current_cte) < 0:
		metrics["zero_crossings"] += 1
	metrics["cte_last"] = current_cte

	# settling detection (|CTE| within band for consecutive frames)
	metrics["settle_window"].append(abs_cte <= EPS_CTE)
	if (not metrics["settled"]
		and len(metrics["settle_window"]) == SETTLE_FRAMES
		and all(metrics["settle_window"])):
		metrics["settled"] = True
		metrics["settle_frame"] = metrics["frames"]

	# control effort
	metrics["u_abs_sum"] += abs(control_u)
	metrics["u_sq_sum"] += control_u * control_u

def final_report():
	"""Print a compact summary suitable for the CV/README."""
	dur = time.perf_counter() - metrics["t_start"]
	n = max(metrics["frames"], 1)
	rmse = (metrics["cte_sq_sum"] / n) ** 0.5
	mean_abs = metrics["cte_abs_sum"] / n
	avg_u_abs = metrics["u_abs_sum"] / n
	avg_u_sq  = metrics["u_sq_sum"] / n
	avg_fps = metrics["fps_sum"] / n
	avg_ms = 1000.0 * (metrics["frame_time_sum"] / n)

	if metrics["settled"] and metrics["settle_frame"] is not None and avg_fps > 0:
		settle_time = metrics["settle_frame"] / avg_fps
	else:
		settle_time = None

	print("\n=== PID Tracking Report ===")
	print(f"Duration: {dur:.2f}s  Frames: {n}")
	print(f"RMSE(CTE): {rmse:.2f} px   Mean|CTE|: {mean_abs:.2f} px   Max|CTE|: {metrics['cte_max_abs']:.1f} px")
	if settle_time is not None:
		print(f"Settling time (|CTE|≤{EPS_CTE} px for {SETTLE_FRAMES} frames): {settle_time:.2f} s")
	else:
		print("Settling time: not settled")
	print(f"Control effort: mean|u|={avg_u_abs:.3f}   mean(u^2)={avg_u_sq:.3f}")
	print(f"Performance: avg FPS={avg_fps:.1f}   avg frame={avg_ms:.2f} ms")
	print(f"Out-of-bounds exits: {metrics['oob']}")

def draw(win, player_car, scroll):
	i = 0
	while i < tiles:
		screen.blit(bg, (bg.get_width() * i + scroll, 0))
		i += 1

	# RESET THE SCROLL FRAME
	if abs(scroll) > bg.get_width():
		scroll = 0

	if debug:
		level_text = MAIN_FONT.render(f"CTE {player_car.y - 266:.1f}", 1, (255, 255, 255))
		win.blit(level_text, (10, FrameHeight - level_text.get_height() - 70))
		steer_text = MAIN_FONT.render(f"Steering angle: {player_car.steering_angle:.2f}", 1, (255, 255, 255))
		win.blit(steer_text, (10, FrameHeight - steer_text.get_height() - 40))
		vel_text = MAIN_FONT.render(f"Vel: {round(player_car.vel, 1)} px/s", 1, (255, 255, 255))
		win.blit(vel_text, (10, FrameHeight - vel_text.get_height() - 10))

	player_car.draw(win)
	pygame.display.update()
	return scroll

def move_player(player_car):
	keys = pygame.key.get_pressed()
	moved = False

	current_CTE = player_car.y - 266
	player_car.steering_angle = controller.process(current_CTE)

	if steer_bias:
		player_car.steering_angle += 0.3

	player_car.rotate()

	# ===== Update metrics once per frame =====
	update_metrics(current_CTE, player_car.steering_angle, clock.get_fps())

	if debug:
		if keys[pygame.K_w]:
			moved = True
			player_car.move_forward()
		if keys[pygame.K_s]:
			moved = True
			player_car.move_backward()
		if not moved:
			player_car.reduce_speed()
	else:
		player_car.move_forward()

class AbstractCar:
	def __init__(self, max_vel, rotation_vel):
		self.img = self.IMG
		self.max_vel = max_vel
		self.vel = 0
		self.rotation_vel = rotation_vel
		self.max_steering_angle = 4.0
		self.steering_angle = 0.0
		self.angle = 220
		self.x, self.y = self.START_POS
		self.prev_x, self.prev_y = self.START_POS
		self.acceleration = 0.1

	def rotate(self):
		if self.steering_angle > self.max_steering_angle:
			self.steering_angle = self.max_steering_angle
		if self.steering_angle < -self.max_steering_angle:
			self.steering_angle = -self.max_steering_angle

		# steering proportional to velocity
		self.angle -= (self.vel / self.max_vel) * self.steering_angle

	def draw(self, win):
		blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

	def move_forward(self):
		self.vel = min(self.vel + self.acceleration, self.max_vel)
		self.move()

	def move_backward(self):
		self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
		self.move()

	def move(self):
		radians = math.radians(self.angle)
		vertical = math.cos(radians) * self.vel
		horizontal = math.sin(radians) * self.vel

		self.prev_x = self.x
		self.prev_y = self.y
		self.y -= vertical
		self.x -= horizontal

		if wind:
			self.y -= 0.2

	def collide(self, mask, x=0, y=0):
		car_mask = pygame.mask.from_surface(self.img)
		offset = (int(self.x - x), int(self.y - y))
		poi = mask.overlap(car_mask, offset)
		return poi

	def reset(self):
		self.x, self.y = self.START_POS
		self.angle = 0
		self.vel = 0

class PlayerCar(AbstractCar):
	IMG = RED_CAR
	START_POS = (45, 200)

	def reduce_speed(self):
		self.vel = max(self.vel - self.acceleration / 2, 0)
		self.move()

	def bounce(self):
		self.vel = -self.vel
		self.move()

# ================== MAIN ==================
player_car = PlayerCar(1, 4)
controller = pid.PIDcontroller()

scroll = 0
tiles = math.ceil(FrameWidth / bg.get_width()) + 1

while True:
	clock.tick(60)  # you can change this during the optimization process

	scroll = draw(screen, player_car, scroll)
	move_player(player_car)

	# Out-of-bounds => report & exit
	if player_car.x > 1200 or player_car.x < 0 or player_car.y < 0 or player_car.y > 400:
		metrics["oob"] += 1
		final_report()
		pygame.quit()
		raise SystemExit

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			final_report()
			pygame.quit()
			raise SystemExit
