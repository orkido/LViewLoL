from lview import *
from commons.targeting import TargetingConfig
from time import time
import itertools, math
from commons.skills import *
from copy import copy
from math import *

lview_script_info = {
	"script": "Evader",
	"author": "https://github.com/bckd00r / bckd00r",
	"description": "Evade module with LViewLoL"
}

bound_max = 0

evades = False
evade_min_range  = 0

targeting = TargetingConfig() 

def clamp_norm_2d(v, n_max):	
	vx = v.x
	vy = v.y
	vz = v.z
	n = sqrt(pow(vx, float(2)) + pow(vz, float(2)))
	f = min(n, n_max) / n
	return Vec3(f * vx, vy,f * vz)


def PointOnLineSegment(pt1, pt2, pt, epsilon = 0.001):
        if (pt.x - max(pt1.x, pt2.x) > epsilon or
            min(pt1.x, pt2.x) - pt.x > epsilon or
            pt.y - max(pt1.y, pt2.y) > epsilon or
            min(pt1.y, pt2.y) - pt.y > epsilon):
                return False
        if abs(pt2.x - pt1.x) < epsilon:
            return abs(pt1.x - pt.x) < epsilon or abs(pt2.x - pt.x) < epsilon
        if abs(pt2.y - pt1.y) < epsilon:
            return abs(pt1.y - pt.y) < epsilon or abs(pt2.y - pt.y) < epsilon

        x = pt1.x + (pt.y - pt1.y) * (pt2.x - pt1.x) / (pt2.y - pt1.y)
        y = pt1.y + (pt.x - pt1.x) * (pt2.y - pt1.y) / (pt2.x - pt1.x)

        return abs(pt.x - x) < epsilon or abs(pt.y - y) < epsilon

def isLeft(a, b, c):
    return ((b.x - a.x) * (c.y - a.y) - (b.y - a.y) * (c.x - a.x)) > 0

def lview_load_cfg(cfg):
	global evades, evade_min_range
	evades            = cfg.get_bool("evades", True)
	evade_min_range  = cfg.get_float("evade_min_range", 500)
	
def lview_save_cfg(cfg):
	global evades, evade_min_range
	cfg.set_bool("evades",            evades)
	cfg.set_float("evade_min_range", evade_min_range)
	
def lview_draw_settings(game, ui):
	global evades, evade_min_range
	ui.separator()
	ui.text("Evader (Experimental)")
	evades            = ui.checkbox("Evade skills", evades)
	evade_min_range  = ui.dragfloat("Minimum evade range", evade_min_range, 100, 0, 3000)
	draw_prediction_info(game, ui)


def evade_skills(game, player):
	global targeting, evades, evade_min_range
	color = Color.WHITE
	for missile in game.missiles:
		if missile.is_ally_to(game.player):
			continue
		spell = get_missile_parent_spell(missile.name)
		if not spell:
			continue	
		end_pos = missile.end_pos.clone()
		start_pos = missile.start_pos.clone()
		curr_pos = missile.pos.clone()
		dodge_pos = game.player.pos
		impact_pos = None
		start_pos.y = game.map.height_at(start_pos.x, start_pos.z) + missile.height
		end_pos.y = start_pos.y
		curr_pos.y = start_pos.y
		p = game.world_to_screen(game.player.pos)
		br = game.player.gameplay_radius
		direction = Vec3(end_pos.x - start_pos.x, end_pos.y - start_pos.y, end_pos.z - start_pos.y)
		pos3 = Vec3(end_pos.x + direction.x * float(1.0), end_pos.y + direction.y, end_pos.z + direction.z * -float(1.0))
		pos4 = Vec3(end_pos.x + direction.x * -float(1.0), end_pos.y + direction.y, end_pos.z + direction.z * float(1.0))
		direction2 = Vec3(pos3.x - pos4.x, pos3.y - pos4.y, pos3.z - pos4.z)
		direction2 = clamp_norm_2d(direction2, br)
		direction3 = Vec3(0, 0, 0)
		direction3.x = -direction2.x 
		direction3.y = -direction2.y
		direction3.z = -direction2.z 
		if spell.flags & SFlag.Area:
			end_pos.y = game.map.height_at(end_pos.x, end_pos.z)

		if PointOnLineSegment(game.world_to_screen(start_pos), game.world_to_screen(end_pos), game.world_to_screen(dodge_pos), br):
			r = game.get_spell_info(spell.name).cast_radius
			percent_done = missile.start_pos.distance(curr_pos)/missile.start_pos.distance(end_pos)
			p.y -= 50
			game.draw_button(p, "Evade: ON", Color.GRAY, Color.YELLOW, 100)
			if isLeft(game.world_to_screen(start_pos), game.world_to_screen(end_pos), game.world_to_screen(dodge_pos)):
				direction4 = direction3
			else: 
				direction4 = direction2
			evadePos = Vec3(dodge_pos.x + direction4.x, dodge_pos.y + direction4.y, dodge_pos.z + direction4.z)
			old_cpos = game.get_cursor()
			game.move_cursor(game.world_to_screen(evadePos))
			game.press_right_click()

def lview_update(game, ui):
	global evades
	
	player = game.player

	if evades:
		evade_skills(game, player)
					
				