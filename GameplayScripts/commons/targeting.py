from lview import *
from enum import Enum

class Target(Enum):
	ClosestToPlayer = 0
	LowestHealth    = 1
	MostFed         = 2

class TargetingConfig:
	targets = [ Target.ClosestToPlayer, Target.LowestHealth, Target.MostFed ]
	targeting_lambdas = {
		Target.ClosestToPlayer: (lambda player, enemy: player.pos.distance(enemy.pos)),
		Target.LowestHealth:    (lambda player, enemy: enemy.health),
		Target.MostFed:         (lambda player, enemy: -sum([item.cost for item in enemy.items]))
	}
	selected       = 0
	target_minions = False
	target_jungle  = False
	
	def draw(self, ui):
		ui.separator()
		self.selected       = ui.listbox("Target", [str(target)[7:] for target in self.targets], self.selected)
		self.target_jungle  = ui.checkbox("Allow targeting jungle monsters", self.target_jungle)
		self.target_minions = ui.checkbox("Allow targeting minions", self.target_minions)
	
	def get_target(self, game, range):
		player = game.player
		
		target_info = self.targets[self.selected]
		target = self.find_target(game, game.champs, range, self.targeting_lambdas[target_info])
		if not target:
			others = []
			if self.target_jungle:
				others.extend(game.jungle)
			if self.target_minions:
				others.extend(game.minions)
				
			if len(others) > 0:
				target = self.find_target(game, others, range, self.targeting_lambdas[target_info])

		return target
		
	def find_target(self, game, array, range, value_extractor):
		target = None
		min = 99999999
		for obj in array:
			is_soldier_targeting = False
			range_calc = (game.distance(game.player, obj) - game.player.gameplay_radius - obj.gameplay_radius)
			soldier_radius = 310
			soldier_affect_range = 690
			for soldier_obj in game.others:
				if not soldier_obj.is_alive or soldier_obj.is_enemy_to(game.player):
					continue
				
				if soldier_obj.has_tags(UnitTag.Unit_Special_AzirW):
					if game.distance(game.player, obj) > (range + soldier_radius):
						continue
					
					range_calc = (game.distance(soldier_obj, obj) - soldier_obj.gameplay_radius - obj.gameplay_radius)
					is_soldier_targeting = True
					
			
						
			if not obj.is_alive or not obj.is_visible or obj.is_ally_to(game.player) or range_calc > (range + soldier_radius):
				continue
				
			if is_soldier_targeting == True:
				if not obj.is_alive or not obj.is_visible or obj.is_ally_to(game.player) or range_calc > soldier_radius:
					continue
			
			if is_soldier_targeting == False:
				if not obj.is_alive or not obj.is_visible or obj.is_ally_to(game.player) or range_calc > range:
					continue
				
			val = value_extractor(game.player, obj)
			if val < min:
				min = val
				target = obj
		
		return target		
	
	def load_from_cfg(self, cfg):
		self.selected       = cfg.get_int("targeting_target", 0)
		self.target_jungle  = cfg.get_bool("target_jungle", False)
		self.target_minions = cfg.get_bool("target_minions", False)
		
	def save_to_cfg(self, cfg):
		cfg.set_int("targeting_target", self.selected)
		cfg.set_bool("target_jungle",   self.target_jungle)
		cfg.set_bool("target_minions",  self.target_minions)
	
	