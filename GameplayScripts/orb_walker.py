from lview import *
from commons import skills
from commons.targeting import TargetingConfig
from datetime import datetime
import time, json

lview_script_info = {
	"script": "Orbwalker",
	"author": "leryss",
	"description": "Automatically kites enemies. Also has last hit built in"
}

last_attacked = 0
last_moved = 0

key_attack_move = 0
key_orbwalk = 0

key_whitelist = {
	"key_1": 2,
	"key_2": 3,
	"key_3": 4,
	"key_4": 5,
	"key_5": 6,
	"key_6": 7,
	"key_7": 8,
	"key_q": 16,
	"key_w": 17,
	"key_e": 18,
	"key_r": 19,
	"key_d": 32,
	"key_f": 33
}

auto_last_hit = False
target = None
max_atk_speed = 0

toggle_mode = False
toggled = False

targeting = TargetingConfig() 

soldiers = {
	#Name -> (radius, show_radius_circle, show_radius_circle_minimap, icon)                      
	'azirsoldier'          : [325.0, True,  False, "azir_w"]
}


def lview_load_cfg(cfg):
	global key_attack_move, key_orbwalk, max_atk_speed, auto_last_hit, toggle_mode
	global targeting
	
	key_attack_move = cfg.get_int("key_attack_move", 0)	
	key_orbwalk     = cfg.get_int("key_orbwalk", 0)	
	max_atk_speed   = cfg.get_float("max_atk_speed", 2.0)
	auto_last_hit   = cfg.get_bool("auto_last_hit", True)
	toggle_mode     = cfg.get_bool("toggle_mode", False)
	targeting.load_from_cfg(cfg)
	
def lview_save_cfg(cfg):
	global key_attack_move, key_orbwalk, max_atk_speed, auto_last_hit, toggle_mode
	global targeting
		
	cfg.set_int("key_attack_move", key_attack_move)
	cfg.set_int("key_orbwalk", key_orbwalk)
	cfg.set_float("max_atk_speed", max_atk_speed)
	cfg.set_bool("auto_last_hit", auto_last_hit)
	cfg.set_bool("toggle_mode", toggle_mode)
	targeting.save_to_cfg(cfg)
	
def lview_draw_settings(game, ui):
	global key_attack_move, key_orbwalk, max_atk_speed, auto_last_hit, toggle_mode
	global targeting
	
	champ_name = game.player.name
	max_atk_speed   = ui.sliderfloat("Max attack speed", max_atk_speed, 1.5, 3.0)
	key_attack_move = ui.keyselect("Attack move key", key_attack_move)
	key_orbwalk     = ui.keyselect("Orbwalk activate key", key_orbwalk)
	auto_last_hit   = ui.checkbox("Last hit minions when no targets", auto_last_hit)
	toggle_mode     = ui.checkbox("Toggle mode", toggle_mode)
	targeting.draw(ui)

def find_minion_target(game):
	atk_range = game.player.base_atk_range + game.player.gameplay_radius
	min_health = 9999999999
	player_target = None
	for minion in game.minions:
		if minion.is_visible and minion.is_enemy_to(game.player) and minion.is_alive and minion.health < min_health and game.distance(game.player, minion) < atk_range:
			#game.draw_circle_world(minion.pos, 24, 16, 3, Color.BLUE)

			if skills.is_last_hitable(game, game.player, minion):
				player_target = minion
				min_health = minion.health
		
	return player_target
	
def find_soldier_minion_target(game):
	soldier_affect_range = 650.0
	soldier_radius = 325.0
	min_health = 9999999999
	soldier_target = None
	for minion in game.minions:
		soldier = skills.soldier_near_obj(game, minion)
		if minion.is_visible and minion.is_enemy_to(game.player) and minion.is_alive and minion.health < min_health and soldier is not None:
			#game.draw_circle_world(minion.pos, 48.0, 16, 3, Color.BLUE)

			if skills.is_last_hitable(game, game.player, minion):
				soldier_target = minion
				min_health = minion.health
		
	return soldier_target
	
def get_target(game):
	global auto_last_hit
	global target

	atk_range = game.player.base_atk_range + game.player.gameplay_radius

	if target is not None and (not target.is_visible or not target.is_alive or (skills.soldier_near_obj(game, target) is None and game.distance(game.player, target) > atk_range)):
		#game.draw_circle_world(game.player.pos, 24.0, 16, 3, Color.BLACK)
		target = None 
		
	if target is None:
		target = targeting.get_target(game, atk_range)

	if not target and auto_last_hit:
		soldier = skills.is_soldier_alive(game)

		#only need to know if > 0 soldiers are up
		if soldier is not None:
			target = find_soldier_minion_target(game)
	
		if not target:
			target = find_minion_target(game)
	
	return target

def draw_rect(game, start_pos, end_pos, radius, color):
	
	dir = Vec3(end_pos.x - start_pos.x, 0, end_pos.z - start_pos.z).normalize()
				
	left_dir = Vec3(dir.x, dir.y, dir.z).rotate_y(90).scale(radius)
	right_dir = Vec3(dir.x, dir.y, dir.z).rotate_y(-90).scale(radius)
	
	p1 = Vec3(start_pos.x + left_dir.x,  start_pos.y + left_dir.y,  start_pos.z + left_dir.z)
	p2 = Vec3(end_pos.x + left_dir.x,    end_pos.y + left_dir.y,    end_pos.z + left_dir.z)
	p3 = Vec3(end_pos.x + right_dir.x,   end_pos.y + right_dir.y,   end_pos.z + right_dir.z)
	p4 = Vec3(start_pos.x + right_dir.x, start_pos.y + right_dir.y, start_pos.z + right_dir.z)
	
	game.draw_rect_world(p1, p2, p3, p4, 3, color)

def draw(game, obj, radius, show_circle_world, show_circle_map, icon):
			
	sp = game.world_to_screen(obj.pos)
	
	if game.is_point_on_screen(sp):
		duration = obj.duration + obj.last_visible_at - game.time
		if duration > 0:
			game.draw_text(sp.add(Vec2(5, 30)), f'{duration:.0f}', Color.WHITE)	
		game.draw_image(icon, sp, sp.add(Vec2(30, 30)), Color.WHITE, 10)
		
		if show_circle_world:
			game.draw_circle_world(obj.pos, radius, 30, 3, Color.RED)
	
	if show_circle_map:
		p = game.world_to_minimap(obj.pos)
		game.draw_circle(game.world_to_minimap(obj.pos), game.distance_to_minimap(radius), 15, 2, Color.RED)


def lview_update(game, ui):
	global last_attacked, alternate, last_moved
	global key_attack_move, key_orbwalk, max_atk_speed
	global toggle_mode, toggled
	global target
	
	#game.draw_button(game.world_to_screen(game.player.pos), "Buffs: azirwprocbuff" + str(game.player.buffs[0].name) + " - Duration: " + str(game.player.buffs[0].end_time), Color.BLACK, Color.WHITE)

	#if game.player.name == "azir":
		# for obj in game.others:
		# 	if not obj.is_alive or obj.is_enemy_to(game.player):
		# 		continue
			
		# 	if obj.has_tags(UnitTag.Unit_Special_AzirW):
		# 		draw(game, obj, *(soldiers[obj.name]))

	if toggle_mode:
		if game.was_key_pressed(key_orbwalk):
			toggled = not toggled
		if not toggled:
			return
			
	elif not game.is_key_down(key_orbwalk):
		return

	# for key in key_whitelist.items():
	# 	if game.was_key_pressed(key):
	# 		last_attacked = time.time()

	# if game.player.name == "azir":
	# 	if game.was_key_pressed(key_q):
	# 		last_attacked = time.time()
	# 	if game.was_key_pressed(key_w):
	# 		last_attacked = time.time()
	# 	if game.was_key_pressed(key_e):
	# 		last_attacked = time.time()
	# 	if game.was_key_pressed(key_r):
	# 		last_attacked = time.time()

	# game.draw_button(game.world_to_screen(game.player.pos), "OrbWalking", Color.BLACK, Color.WHITE)

	# Handle basic attacks
	self = game.player
	atk_speed = self.base_atk_speed * self.atk_speed_multi
	b_windup_time = ((1.0/self.base_atk_speed)*game.player.basic_atk_windup)
	c_atk_time = (1.0/atk_speed)
	max_atk_time = 1.0/max_atk_speed

	if target is not None:
		game.draw_circle_world(target.pos, 24.0, 16, 3, Color.WHITE)

		# if game.player.name == "azir" and game.player.W.level > 0:
		# 	#Check if azir arise buff is active (it's named azirwprocbuff)
		# 	azir_w_atk_speeds = {
		# 		1:20,
		# 		2:30,
		# 		3:40,
		# 		4:50,
		# 		5:60
		# 	}
		# 	azir_w_atk_speed_multiplier = azir_w_atk_speeds[game.player.W.level]

		# 	w_time = time.time()
		# 	for buff in game.player.buffs:
		# 		if buff.name == "azirwprocbuff":
		# 			if time.time() < buff.end_time:
		# 				#our attack speed buff is active
		# 				#need to check spell level of w and get the attack speed multiplier
		# 				atk_speed = (self.base_atk_speed)


		# soldier = soldier_near_obj(game, target)
		# if soldier is not None:

		# 	num_soldiers = count_soldiers_near_obj(game, target)
		# 	if num_soldiers == 3:


	target = get_target(game)
	t = time.time()
	if t - last_attacked > max(c_atk_time, max_atk_time) and target:
		last_attacked = t
		
		#game.press_key(key_attack_move)
		game.click_at(True, game.world_to_screen(target.pos))
	else:
		dt = t - last_attacked
		if dt > b_windup_time and t - last_moved > 0.15:
			last_moved = t
			game.press_right_click()
			