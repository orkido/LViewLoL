from lview import *
import math, itertools, time
from . import items
from commons.damage_calculator import DamageSpecification
from commons.damage_calculator import DamageType

Version = "experimental version"
MissileToSpell = {}
Spells         = {}
ChampionSpells = {}

damageCalc = DamageSpecification()
damageType = DamageType.Normal

class SFlag:
	Targeted        = 1
	Line            = 2
	Cone            = 4
	Area            = 8
	
	CollideWindwall = 16
	CollideChampion = 32
	CollideMob      = 64
	
	
	CollideGeneric   = CollideMob      | CollideChampion | CollideWindwall
	SkillshotLine    = CollideGeneric  | Line
	
class Spell:
	def __init__(self, name, missile_names, flags, delay = 0.0):
		global MissileToSpell, Spells
		
		self.flags = flags
		self.name = name
		self.missiles = missile_names
		self.delay = delay
		Spells[name] = self
		for missile in missile_names:
			MissileToSpell[missile] = self
			
	delay    = 0.0
	flags    = 0
	name     = "?"
	missiles = []
	
#Based on level, not sure exact formula so hardcoded it
AzirSoldierDamage = {
	1: 50,
	2: 52,
	3: 54,
	4: 56,
	5: 58,
	6: 60,
	7: 62,
	8: 65,
	9: 70,
	10: 75,
	11: 80,
	12: 90,
	13: 100,
	14: 110,
	15: 120,
	16: 130,
	17: 140,
	18: 150
}

ChampionSpells = {
	"aatrox": [
		Spell("aatroxw",                ["aatroxw"],                               SFlag.CollideGeneric)
	],
	"aurelionsol": [
		Spell("aurelionsolq",           ["aurelionsolqmissile"],                   SFlag.SkillshotLine),
		Spell("aurelionsolr",           ["aurelionsolrbeammissile"],               SFlag.Line | SFlag.CollideWindwall)
	],
	"ahri": [                                                                      
		Spell("ahriorbofdeception",     ["ahriorbmissile"],                        SFlag.Line | SFlag.CollideWindwall),
		Spell("ahriseduce",             ["ahriseducemissile"],                     SFlag.CollideGeneric)
	],
	"ashe": [                           
		Spell("volleyattack",           ["volleyattack", "volleyattackwithsound"], SFlag.SkillshotLine),
		Spell("enchantedcrystalarrow",  ["enchantedcrystalarrow"],                 SFlag.Line | SFlag.CollideWindwall | SFlag.CollideChampion)
	],
	"brand": [
		Spell("brandq",                 ["brandqmissile"],                         SFlag.SkillshotLine),
		Spell("brandw",                 [],                                        SFlag.Area)
	],
	"caitlyn": [
		Spell("caitlynpiltoverpeacemaker", ["caitlynpiltoverpeacemaker", "caitlynpiltoverpeacemaker2"],          SFlag.Line | SFlag.CollideWindwall),
		Spell("caitlynyordletrap",         [],                                                                   SFlag.Area),
		Spell("caitlynentrapment",         ["caitlynentrapmentmissile"],                                         SFlag.SkillshotLine)
	],
	"chogath": [                        
		Spell("rupture",                [],                                        SFlag.Area, delay = 0.627),
		Spell("feralscream",            [],                                        SFlag.Cone | SFlag.CollideWindwall)
	],
	"drmundo": [
		Spell("infectedcleavermissilecast", ["infectedcleavermissile"],            SFlag.SkillshotLine)
	],
	"diana": [
		Spell("dianaq",                 ["dianaqinnermissile", "dianaqoutermissile"], SFlag.Area)
	],
	"ekko": [
		Spell("ekkoq",                  ["ekkoqmis"],                              SFlag.Line | SFlag.CollideChampion),
		Spell("ekkow",                  ["ekkowmis"],                              SFlag.Area, delay=3.0)
	],
	"fizz": [
		Spell("fizzr",                  ["fizzrmissile"],                          SFlag.Line | SFlag.CollideChampion | SFlag.CollideWindwall)
	],
	"irelia": [
		Spell("ireliae",                ["ireliaemissile"],                        SFlag.Area),
		Spell("ireliar",                ["ireliar"],                               SFlag.SkillshotLine)
	],
	"illaoi": [
		Spell("illaoiq",                [],                                        SFlag.Area),
		Spell("illaoie",                ["illaoiemis"],                            SFlag.SkillshotLine)
	],
	"jarvaniv": [
		Spell("jarvanivdemacianstandard", [],                                      SFlag.Area)
	],
	"khazix": [
		Spell("khazixw",                ["khazixwmissile"],                        SFlag.SkillshotLine),
		Spell("khazixwlong",            ["khazixwmissile"],                        SFlag.SkillshotLine)
	],
	"ezreal": [                         
		Spell("ezrealq",                ["ezrealq"],                               SFlag.SkillshotLine),
		Spell("ezrealw",                ["ezrealw"],                               SFlag.SkillshotLine),
		Spell("ezrealr",                ["ezrealr"],                               SFlag.SkillshotLine)
	],
	"evelynn": [
		Spell("evelynnq",               ["evelynnq"],                              SFlag.SkillshotLine)
	],
	"graves": [                         
		Spell("gravesqlinespell",       ["gravesqlinemis", "gravesqreturn"],       SFlag.Line | SFlag.CollideChampion | SFlag.CollideWindwall),
		Spell("gravessmokegrenade",     ["gravessmokegrenadeboom"],                SFlag.Area | SFlag.CollideWindwall),
		Spell("graveschargeshot",       ["graveschargeshotshot"],                  SFlag.Line | SFlag.CollideWindwall)
	],
	"twistedfate": [                    
		Spell("wildcards",              ["sealfatemissile"],                       SFlag.CollideWindwall | SFlag.Line)
	],
	"leesin": [                         
		Spell("blindmonkqone",          ["blindmonkqone"],                         SFlag.SkillshotLine)
	],
	"leona": [
		Spell("leonazenithblade",       ["leonazenithblademissile"],               SFlag.Line | SFlag.CollideChampion | SFlag.CollideWindwall),
		Spell("leonasolarflare",        [],                                        SFlag.Area)
	],
	"leblanc": [
		Spell("leblancw",               [],                                        SFlag.Area),
		Spell("leblancrw",              [],                                        SFlag.Area),
		Spell("leblance",               ["leblancemissile"],                       SFlag.SkillshotLine),
		Spell("leblancre",              ["leblancremissile"],                      SFlag.SkillshotLine)
	],
	"lucian": [
		Spell("lucianw",                ["lucianwmissile"],                          SFlag.SkillshotLine),
		Spell("lucianr",                ["lucianrmissile", "lucianrmissileoffhand"], SFlag.SkillshotLine)
	],
	"rengar": [
		Spell("rengare",                ["rengaremis"],                            SFlag.SkillshotLine),
		Spell("rengareemp",             ["rengareempmis"],                         SFlag.SkillshotLine),
	],
	"ryze": [
		Spell("ryzeqwrapper",           ["ryzeq"],                                 SFlag.SkillshotLine)
	],
	"varus": [
		Spell("varusq",                 ["varusqmissile"],                         SFlag.Line | SFlag.CollideWindwall),
		Spell("varuse",                 ["varusemissile"],                         SFlag.Area),
		Spell("varusr",                 ["varusrmissile"],                         SFlag.Line | SFlag.CollideChampion | SFlag.CollideWindwall)
	],
	"veigar": [                         
		Spell("veigarbalefulstrike",    ["veigarbalefulstrikemis"],                SFlag.SkillshotLine),
		Spell("veigardarkmatter",       [],                                        SFlag.Area, delay=1.0),
		Spell("veigareventhorizon",     [],                                        SFlag.Area, delay=0.5)
	], 
	"lux": [                            
		Spell("luxlightbinding",        ["luxlightbindingmis"],                    SFlag.SkillshotLine),
		Spell("luxlightstrikekugel",    ["luxlightstrikekugel"],                   SFlag.Area | SFlag.CollideWindwall),
		Spell("luxmalicecannon",        ["luxmalicecannon"],                       SFlag.Line)
	],
	"ziggs": [                          
		Spell("ziggsq",                 ["ziggsqspell", "ziggsqspell2", "ziggsqspell3"],                              SFlag.Area | SFlag.CollideWindwall),
		Spell("ziggsw",                 ["ziggsw"],                                                                   SFlag.Area | SFlag.CollideWindwall),
		Spell("ziggse",                 ["ziggse2"],                                                                  SFlag.Area | SFlag.CollideWindwall),
		Spell("ziggsr",                 ["ziggsrboom", "ziggsrboommedium", "ziggsrboomlong", "ziggsrboomextralong"],  SFlag.Area),
	],
	"jhin": [                           
		Spell("jhinw",                  ["jhinw"],                                 SFlag.Line | SFlag.CollideChampion | SFlag.CollideWindwall, delay=0.5),
		Spell("jhine",                  ["jhinetrap"],                             SFlag.Area | SFlag.CollideWindwall),
		Spell("jhinrshot",              ["jhinrshotmis", "jhinrshotmis4"],         SFlag.Line | SFlag.CollideWindwall | SFlag.CollideChampion)
	],
	"nasus": [
		Spell("nasuse",                 [],                                        SFlag.Area)
	],
	"nami": [
		Spell("namiq",                  ["namiqmissile"],                          SFlag.Area),
		Spell("namir",                  ["namirmissile"],                          SFlag.Line | SFlag.CollideWindwall)
	],
	"nidalee": [
		Spell("javelintoss",            ["javelintoss"],                           SFlag.SkillshotLine),
		Spell("bushwhack",              [],                                        SFlag.Area)
	],
	"malphite": [
		Spell("ufslash",                [],                                        SFlag.Area)
	],
	"thresh": [
		Spell("threshq",                ["threshqmissile"],                        SFlag.SkillshotLine),
		Spell("threshw",                ["threshwlanternout"],                     SFlag.Area | SFlag.CollideWindwall)
	],
	"morgana": [                        
		Spell("morganaq",               ["morganaq"],                              SFlag.SkillshotLine),
		Spell("morganaw",               [],                                        SFlag.Area, delay=0.25)
	],
	"missfortune": [
		Spell("missfortunescattershot", [],                                        SFlag.Area, delay=0.25),
		Spell("missfortunebullettime",  ["missfortunebullets"],                    SFlag.Line | SFlag.CollideWindwall)
	],   
	"pantheon": [
		Spell("pantheonq",              ["pantheonqmissile"],                      SFlag.Line | SFlag.CollideWindwall),
		Spell("pantheonr",              ["pantheonrmissile"],                      SFlag.Area)
	],
	"annie": [                                                                     
		Spell("anniew",                 [],                                        SFlag.Cone | SFlag.CollideWindwall),
		Spell("annier",                 [],                                        SFlag.Area)
	],
	"olaf": [
		Spell("olafaxethrowcast",       ["olafaxethrow"],                          SFlag.Line | SFlag.CollideWindwall)
	],
	"anivia": [
		Spell("flashfrost",             ["flashfrostspell"],                       SFlag.Line | SFlag.CollideWindwall),
		Spell("crystallize",            [],                                        SFlag.Area, delay=0.25),
		Spell("glacialstorm",           [],                                        SFlag.Area)
	],
	"urgot": [
		Spell("urgotq",                 ["urgotqmissile"],                         SFlag.Area | SFlag.CollideWindwall, delay = 0.2),
		Spell("urgotr",                 ["urgotr"],                                SFlag.Line | SFlag.CollideWindwall | SFlag.CollideChampion)
	],
	"senna": [
		Spell("sennaw",                 ["sennaw"],                                SFlag.SkillshotLine),
		Spell("sennar",                 ["sennar"],                                SFlag.Line)
	],
	"shyvana": [
		Spell("shyvanafireball",        ["shyvanafireballmissile"],                SFlag.Line | SFlag.CollideChampion | SFlag.CollideWindwall),
		Spell("shyvanafireballdragon2", ["shyvanafireballdragonmissile"],          SFlag.Line | SFlag.Area | SFlag.CollideChampion | SFlag.CollideWindwall)
	],
	"singed": [
		Spell("megaadhesive",           ["singedwparticlemissile"],                SFlag.Area)
	],
	"sivir": [
		Spell("sivirq",                 ["sivirqmissile"],                         SFlag.Line | SFlag.CollideWindwall)
	],
	"soraka": [
		Spell("sorakaq",                ["sorakaqmissile"],                        SFlag.Area),
		Spell("sorakae",                [],                                        SFlag.Area)
	],
	"sona": [
		Spell("sonar",                  ["sonar"],                                 SFlag.Line | SFlag.CollideWindwall)
	],
	"kayle": [
		Spell("kayleq",                 ["kayleqmis"],                             SFlag.SkillshotLine)
	],
	"zac": [
		Spell("zacq",                   ["zacqmissile"],                           SFlag.SkillshotLine),
		Spell("zace",                   [],                                        SFlag.Area)
	],
	"zyra": [
		Spell("zyraq",                  [],                                        SFlag.Area),
		Spell("zyraw",                  [],                                        SFlag.Area),
		Spell("zyrae",                  ["zyrae"],                                 SFlag.Line | SFlag.CollideWindwall),
		Spell("zyrar",                  [],                                        SFlag.Area)
	],
	"zilean": [
		Spell("zileanq",                ["zileanqmissile"],                        SFlag.Area | SFlag.CollideWindwall)
	],
	"orianna": [
		Spell("orianaizunacommand",     ["orianaizuna"],                           SFlag.Line | SFlag.Area | SFlag.CollideWindwall)
	],
	"warwick": [
		Spell("warwickr",               [],                                        SFlag.Area | SFlag.CollideChampion)
	]
}

def draw_prediction_info(game, ui):
	global ChampionSpells, Version
	
	ui.separator()
	ui.text("Using LPrediction " + Version, Color.PURPLE)
	if is_champ_supported(game.player):
		ui.text(game.player.name.upper() + " has skillshot prediction support", Color.GREEN)
	else:
		ui.text(game.player.name.upper() + " doesnt have skillshot prediction support", Color.RED)
	
	if ui.treenode(f'Supported Champions ({len(ChampionSpells)})'):
		for champ, spells in sorted(ChampionSpells.items()):
			ui.text(f"{champ.upper()} {' '*(20 - len(champ))}: {str([spell.name for spell in spells])}")
			
		ui.treepop()

def get_skillshot_range(game, skill_name):
	global Spells
	if skill_name not in Spells:
		raise Exception("Not a skillshot")
	
	# Get the range of the missile if it has a missile
	skillshot = Spells[skill_name]
	if len(skillshot.missiles) > 0:
		return game.get_spell_info(skillshot.missiles[0]).cast_range
		
	# If it doesnt have a missile get simply the cast_range from the skill
	info = game.get_spell_info(skill_name)
	return info.cast_range*2.0 if is_skillshot_cone(skill_name) else info.cast_range

def is_skillshot(skill_name):
	global Spells, MissileToSpell
	return skill_name in Spells or skill_name in MissileToSpell
	
def get_missile_parent_spell(missile_name):
	global MissileToSpell
	return MissileToSpell.get(missile_name, None)
	
def is_champ_supported(champ):
	global ChampionSpells
	return champ.name in ChampionSpells
	
def is_skillshot_cone(skill_name):
	if skill_name not in Spells:
		return False
	return Spells[skill_name].flags & SFlag.Cone

def is_soldier_alive(game):
	if game.player.name == "azir":
		for obj in game.others:
			if not obj.is_alive or obj.is_enemy_to(game.player):
				continue
			
			if obj.has_tags(UnitTag.Unit_Special_AzirW):
				return obj
		
	return None

def soldier_near_obj(game, enemy):
	if game.player.name == "azir":
		soldier_affect_range = 650.0
		soldier_radius = 325.0

		for obj in game.others:
			if not obj.is_alive or obj.is_enemy_to(game.player) or game.distance(game.player, obj) > soldier_affect_range + soldier_radius:
				continue
				
			if obj.has_tags(UnitTag.Unit_Special_AzirW):
				if (game.distance(obj, enemy) < soldier_radius):
					return obj

	return None

def count_soldiers_near_obj(game, enemy):
	num_soldiers = 0
	if game.player.name == "azir":
		soldier_affect_range = 650.0
		soldier_radius = 325.0

		for obj in game.others:
			if not obj.is_alive or obj.is_enemy_to(game.player) or game.distance(game.player, obj) > soldier_affect_range + soldier_radius:
				continue
			
			if obj.has_tags(UnitTag.Unit_Special_AzirW):
				if (game.distance(obj, enemy) < soldier_radius):
					num_soldiers += 1
			
	return num_soldiers

def is_last_hitable(game, player, enemy):
	missile_speed = player.basic_missile_speed + 1
	atk_speed = player.base_atk_speed * player.atk_speed_multi
	
	#percent_ad/ap will be situationally helpful for last hitting
	#damageCalc.percent_ad = 1.0
	#damageCalc.percent_ap = 1.0
	damageCalc.damage_type = damageType
	damageCalc.base_damage = (player.base_atk + player.bonus_atk) - 0.50

	#soldier_near_obj returns None if you're not playing Azir
	#1 soldier = 0% additional onhit soldier dmg, 2 soldiers = 25% addtional onhit soldier dmg, 3 = 50%, etc..
	#one soldier can deal max 150 + 0.60 percent_ap, two soldiers is (150 + 0.60 percent_ap) * 1.25, three is *1.5, etc...
	soldier = soldier_near_obj(game, enemy)

	if soldier is not None:
		num_soldiers = count_soldiers_near_obj(game, enemy)
		#Azir dmg formula
		damageCalc.base_damage = AzirSoldierDamage[player.lvl] + (player.ap * 0.60)
		#Addtional 25% dmg for each additional soldier (num_soldiers-1)
		damageCalc.base_damage = damageCalc.base_damage + (damageCalc.base_damage*((num_soldiers-1) * 0.25)) - 0.50
		damageCalc.damage_type = DamageType.Magic
		#Missile speed for soldier autos is weird- it isnt a missile but the soldier spears do have a travel time before dmg is registered, it can be interrupted by issuing another command much like a traditional auto windup. 
		#Couldn't find a basic_atk_windup for azirsoldier so missile speed is partially based on magic number
		atk_speed = player.base_atk_speed * player.atk_speed_multi
		missile_speed = (3866.0 * atk_speed/player.base_atk_speed)

	#TODO: integrate item onhit calculation based on damagetype
	hit_dmg = (damageCalc.calculate_damage(player, enemy))
	hp = enemy.health
	t_until_basic_hits = game.distance(player, enemy)/missile_speed

	#where should we be applying client-server latency to the formula - in orbwalker or here?
	for missile in game.missiles:
		if missile.dest_id == enemy.id:
			src = game.get_obj_by_id(missile.src_id)
			if src:
				t_until_missile_hits = game.distance(missile, enemy)/(src.basic_missile_speed + 1) #Using src's basic missile speed is most reliable because different minion types have different missile speeds

				if t_until_missile_hits < t_until_basic_hits:
					hp -= src.base_atk

	return hp - hit_dmg <= 0
	
# Returns a point where the mouse should click to cast a spells taking into account the targets movement speed
def castpoint_for_collision(game, spell, caster, target):
	global Spells

	print('predicted')
	if spell.name not in Spells:
		return None
	
	# Get extra data for spell that isnt provided by lview
	spell_extra = Spells[spell.name]
	if len(spell_extra.missiles) > 0:
		missile = game.get_spell_info(spell_extra.missiles[0])
	else:
		missile = spell
		
	t_delay = spell.delay + spell_extra.delay
	if missile.travel_time > 0.0:
		t_missile = missile.travel_time
	else:
		t_missile = (missile.cast_range / missile.speed) if len(spell_extra.missiles) > 0 and missile.speed > 0.0 else 0.0
			
	# Get direction of target
	target_dir = target.pos.sub(target.prev_pos).normalize()
	if math.isnan(target_dir.x):
		target_dir.x = 0.0
	if math.isnan(target_dir.y):
		target_dir.y = 0.0
	if math.isnan(target_dir.z):
		target_dir.z = 0.0

	# If the spell is a line we simulate the main missile to get the collision point
	if spell_extra.flags & SFlag.Line:
		
		iterations = int(missile.cast_range/30.0)
		step = t_missile/iterations
		
		last_dist = 9999999
		last_target_pos = None
		for i in range(iterations):
			t = i*step
			target_future_pos = target.pos.add(target_dir.scale((t_delay + t)*target.movement_speed))
			spell_dir = target_future_pos.sub(caster.pos).normalize().scale(t*missile.speed)
			spell_future_pos = caster.pos.add(spell_dir)
			
			dist = target_future_pos.distance(spell_future_pos)
			#print(dist)
			if dist < missile.width/2.0:
				return target_future_pos
			elif dist > last_dist:
				return last_target_pos
			else:
				last_dist = dist
				last_target_pos = target_future_pos
				
		return None
		
	# If the spell is an area spell we return the position of the player when the spell procs
	elif spell_extra.flags & SFlag.Area:
		return target.pos.add(target_dir.scale((t_delay + t_missile)*target.movement_speed))
	else:
		return target.pos
		