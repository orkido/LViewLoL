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
last_cass_q = 0
last_moved = 0

key_attack_move = 0
key_orbwalk = 0
key_lasthit = 0

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

#Used to branch orbwalking logic if Player is using one of these champs
special_orbwalk_champs = {
	"azir": 0.0,
	"cassiopeia": 0.0
}

def lview_load_cfg(cfg):
	global key_attack_move, key_orbwalk, key_lasthit, max_atk_speed, auto_last_hit, toggle_mode
	global targeting
	
	key_attack_move = cfg.get_int("key_attack_move", 0)	
	key_orbwalk     = cfg.get_int("key_orbwalk", 0)	
	key_lasthit     = cfg.get_int("key_lasthit", 0)
	max_atk_speed   = cfg.get_float("max_atk_speed", 2.0)
	auto_last_hit   = cfg.get_bool("auto_last_hit", True)
	toggle_mode     = cfg.get_bool("toggle_mode", False)
	targeting.load_from_cfg(cfg)
	
def lview_save_cfg(cfg):
	global key_attack_move, key_orbwalk, key_lasthit, max_atk_speed, auto_last_hit, toggle_mode
	global targeting
		
	cfg.set_int("key_attack_move", key_attack_move)
	cfg.set_int("key_orbwalk", key_orbwalk)
	cfg.set_int("key_lasthit", key_lasthit)
	cfg.set_float("max_atk_speed", max_atk_speed)
	cfg.set_bool("auto_last_hit", auto_last_hit)
	cfg.set_bool("toggle_mode", toggle_mode)
	targeting.save_to_cfg(cfg)
	
def lview_draw_settings(game, ui):
	global key_attack_move, key_orbwalk, key_lasthit, max_atk_speed, auto_last_hit, toggle_mode
	global targeting
	
	champ_name = game.player.name
	max_atk_speed   = ui.sliderfloat("Max attack speed", max_atk_speed, 1.5, 3.0)
	key_attack_move = ui.keyselect("Attack move key", key_attack_move)
	key_orbwalk     = ui.keyselect("Orbwalk and focus harass key", key_orbwalk)
	key_lasthit     = ui.keyselect("Orbwalk and focus lasthit key", key_lasthit)
	auto_last_hit   = ui.checkbox("Last hit minions when no targets", auto_last_hit)
	toggle_mode     = ui.checkbox("Toggle mode", toggle_mode)
	targeting.draw(ui)

#Added range parameter so we can specify custom minion targeting range based on champ ability range (like cass E for example)
def find_minion_target(game, range):
	#atk_range = game.player.base_atk_range + game.player.gameplay_radius
	min_health = 9999999999
	player_target = None
	for minion in game.minions:
		if minion.is_visible and minion.is_enemy_to(game.player) and minion.is_alive and minion.health < min_health and game.distance(game.player, minion) < range:
			if skills.is_last_hitable(game, game.player, minion):
				player_target = minion
				min_health = minion.health
		
	return player_target
	
#We rely on skills.soldier_near_obj to calculate the range and retrieve the soldier data for soldier's minion target
def find_soldier_minion_target(game):
	min_health = 9999999999
	soldier_target = None
	for minion in game.minions:
		soldier = skills.soldier_near_obj(game, minion)
		if minion.is_visible and minion.is_enemy_to(game.player) and minion.is_alive and minion.health < min_health and soldier is not None:
			if skills.is_last_hitable(game, game.player, minion):
				soldier_target = minion
				min_health = minion.health
		
	return soldier_target
	
def champ_near_obj(game, champ):
	soldier_target = skills.soldier_near_obj(game, champ)
	atk_range = game.player.base_atk_range + game.player.gameplay_radius
	if soldier_target is not None:
		return True
	else:
		return game.distance(game.player, champ) < atk_range

	return False

def get_target(game, last_hit_prio):
	global auto_last_hit
	global target
	global special_orbwalk_champs

	atk_range = game.player.base_atk_range + game.player.gameplay_radius

	if target is not None and (not target.is_visible or not target.is_alive or (skills.soldier_near_obj(game, target) is None and game.distance(game.player, target) > atk_range)):
		target = None 
		
	if target is not None:
		if not last_hit_prio:
			if not target.has_tags(UnitTag.Unit_Champion):
				#since last target is valid but it isn't a champion and we're focusing on harass then we're allowed to overwrite target only if we can find a champion in range
				for champ in game.champs:
					if champ_near_obj(game, champ):
						target = targeting.get_target(game, atk_range)
		else:
			target = None		
	elif not last_hit_prio:
		target = targeting.get_target(game, atk_range)

	if not target and auto_last_hit:
		if game.player.name in special_orbwalk_champs:
			if game.player.name == "azir":
				soldier = skills.is_soldier_alive(game)

				#only need to know if > 0 soldiers are up
				if soldier is not None:
					target = find_soldier_minion_target(game)
			elif game.player.name == "cassiopeia":
				target = find_minion_target(game, 711.0)

		if not target:
			target = find_minion_target(game, game.player.base_atk_range + game.player.gameplay_radius)

	#Unused for now, only use V for last hitting, don't expect V to harass champs
	# if not target and last_hit_prio:
	# 	target = targeting.get_target(game, atk_range)
	
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

def cassQ(game, target):
	global last_attacked

	skill = getattr(game.player, 'Q')

	cast_point = skills.castpoint_for_collision(game, skill, game.player, target)
	if cast_point and game.distance(game.player, target) < 850.0:
		cast_point = game.world_to_screen(cast_point)
		cursor_pos = game.get_cursor()
		game.move_cursor(cast_point)
		skill.trigger()
		time.sleep(0.01)
		game.move_cursor(cursor_pos)

def cassE(game, target):
	global last_attacked

	skill = getattr(game.player, 'E')

	if game.distance(game.player, target) < 711.0:
		cast_point = game.world_to_screen(target.pos)
		cursor_pos = game.get_cursor()
		game.move_cursor(cast_point)
		skill.trigger()
		time.sleep(0.01)
		game.move_cursor(cursor_pos)


def lview_update(game, ui):
	global last_attacked, last_cass_q, alternate, last_moved
	global key_attack_move, key_orbwalk, key_lasthit, max_atk_speed
	global toggle_mode, toggled
	global target
	global special_orbwalk_champs

	if toggle_mode:
		if game.was_key_pressed(key_orbwalk):
			toggled = not toggled
		if not toggled:
			return
			
	elif not game.is_key_down(key_orbwalk) and not game.is_key_down(key_lasthit):
		return

	last_hit_priority = False
	if game.is_key_down(key_lasthit):
		last_hit_priority = True

	#Show orbwalk target
	if target is not None:
		game.draw_circle_world(target.pos, 24.0, 16, 3, Color.WHITE)

	#Use if you need to prevent orbwalker from interrupting your key presses:
	# for key in key_whitelist.items():
	# 	if game.was_key_pressed(key):
	#		last_attacked = time.time()

	self = game.player
	#Handle basic attacks
	atk_speed = self.base_atk_speed * self.atk_speed_multi
	b_windup_time = ((1.0/self.base_atk_speed)*game.player.basic_atk_windup)
	c_atk_time = (1.0/atk_speed)
	max_atk_time = 1.0/max_atk_speed
	t = time.time()
	soldier_hitting = False

	#NEWWY DEWWY
	target = get_target(game, last_hit_priority)
	
	if game.player.name in special_orbwalk_champs:
		if game.player.name == "azir":
			if target:
				soldier = skills.soldier_near_obj(game, target)
				if soldier is not None:
					soldier_hitting = True
		elif game.player.name == "cassiopeia":
			if target:
				skillQ = getattr(game.player, 'Q')
				skillE = getattr(game.player, 'E')
				abilityHastePercent = (100 - 100/((1/100)*game.player.ability_haste + 1))/100

				if t - last_cass_q >= (3.50 - (3.50 * abilityHastePercent)) and skillQ.get_current_cooldown(game.time) == 0 and game.player.mana > (50.0 + (10 * (skillQ.level-1))) and target and target.has_tags(UnitTag.Unit_Champion) and game.distance(game.player, target) < 850.0:
					last_cass_q = t
					cassQ(game, target) 
				if t - last_attacked >= (0.75 - (0.75 * abilityHastePercent)) and skillE.get_current_cooldown(game.time) == 0 and game.player.mana > 50.0 and target and game.distance(game.player, target) < 711.0:
					last_attacked = t
					cassE(game, target)
		
	if t - last_attacked >= max(c_atk_time, max_atk_time) and target and ((game.distance(game.player, target) < self.base_atk_range + self.gameplay_radius - target.gameplay_radius) or soldier_hitting):
		last_attacked = t
		cast_point = game.world_to_screen(target.pos)
		cursor_pos = game.get_cursor()
		game.move_cursor(cast_point)
		game.press_right_click()
		time.sleep(0.01)
		game.move_cursor(cursor_pos)
	elif t - last_attacked >= b_windup_time and t - last_moved > 0.08:
		last_moved = t
		game.press_right_click()