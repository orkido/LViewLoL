import enum
from typing import Optional

class DamageType(enum.Enum):
    True_ = 0
    Normal = 1
    Magic = 2

class DamageSpecification:
    damage_type: Optional[DamageType] = None

    base_damage = 0.0

    percent_ad = 0.0
    percent_ap = 0.0

    # Damage is increased by up to missing_health_multiplier based on missing enemy health. Maximum if enemy health is below missing_health_max_multiplier
    missing_health_scale_multiplier = 0.0
    missing_health_max_scale_multiplier = 1.0

    # Damage increased by missing_health_multiplier * enemy_missing_health
    missing_health_multiplier = 0.0
    # Damage increased by max_health_multiplier * enemy_max_health
    max_health_multiplier = 0.0

    # damage dealt by source to target
    def calculate_damage(self, source, target):
        # Calculate resistance
        resistance_value = 0.0
        penetration_percent = 0.0
        penetration_flat = 0.0
        penetration_lethality = 0.0

        if self.damage_type is None:
            return 0
        elif self.damage_type == DamageType.True_:
            pass
        elif self.damage_type == DamageType.Normal:
            resistance_value = target.armour
            penetration_percent = 0.0    # TODO
            penetration_flat = 0.0       # TODO
            penetration_lethality = 0.0  # TODO
        elif self.damage_type == DamageType.Magic:
            resistance_value = target.magic_resist
            penetration_percent = 0.0    # TODO
            penetration_flat = 0.0       # TODO
            penetration_lethality = 0.0  # TODO

        # Lethality calculation
        penetration_flat += penetration_lethality * (0.6 + 0.4 * source.lvl / 18.0)

        # Negative resistance is not affected by penetration
        if(resistance_value > 0.0):
            resistance_value = resistance_value * penetration_percent - penetration_flat
            # Penetration cannot reduce resistance below 0
            resistance_value = max(0.0, resistance_value)

        # Damage multiplier for armor, magic resistance or true damage (resistance_value is zero for true damage)
        if resistance_value >= 0.0:
            damage_multiplier = 100.0 / (100.0 + resistance_value)
        else:
            damage_multiplier = 2.0 - 100.0 / (100.0 - resistance_value)

        dealt_damage = (
            self.base_damage
            + self.missing_health_multiplier * (target.max_health - target.health)
            + self.max_health_multiplier * target.max_health
            + self.percent_ad * (source.base_atk + source.bonus_atk)
            + self.percent_ap * source.ap
        )

        percent_current_health = target.health / target.max_health
        if percent_current_health <= self.missing_health_max_scale_multiplier:
            dealt_damage = dealt_damage * (1.0 + self.missing_health_scale_multiplier)
        else:
            dealt_damage = (dealt_damage *
                (1.0 + self.missing_health_scale_multiplier - self.missing_health_scale_multiplier
                 * ((percent_current_health - self.missing_health_max_scale_multiplier) / (1.0 - self.missing_health_max_scale_multiplier))))

        # Multiplier for armor, magic resist or true damage
        dealt_damage = damage_multiplier * dealt_damage

        return dealt_damage

def get_damage_specification(champ) -> Optional[DamageSpecification]:
    spec = DamageSpecification()

    if champ.name == "darius":
        # TODO: passive damage multiplier
        spec.damage_type = DamageType.True_

        spec.percent_ad = 0.75
        if champ.R.level == 1:
            spec.base_damage = 100.0
        elif champ.R.level == 2:
            spec.base_damage = 200.0
        elif champ.R.level == 3:
            spec.base_damage = 300.0

    elif champ.name == "garen":
        spec.damage_type = DamageType.True_

        if champ.R.level == 1:
            spec.base_damage = 150.0
            spec.missing_health_multiplier = 0.20
        elif champ.R.level == 2:
            spec.base_damage = 300.0
            spec.missing_health_multiplier = 0.25
        elif champ.R.level == 3:
            spec.base_damage = 450.0
            spec.missing_health_multiplier = 0.30

    elif champ.name == "lux":
        spec.damage_type = DamageType.Magic

        spec.percent_ap = 1.0
        if champ.R.level == 1:
            spec.base_damage = 300.0
        elif champ.R.level == 2:
            spec.base_damage = 400.0
        elif champ.R.level == 3:
            spec.base_damage = 500.0

    elif champ.name == "veigar":
        spec.damage_type = DamageType.Magic

        spec.percent_ap = 0.75
        spec.missing_health_scale_multiplier = 1.0
        spec.missing_health_max_scale_multiplier = 0.33
        if champ.R.level == 1:
            spec.base_damage = 175.0
        elif champ.R.level == 2:
            spec.base_damage = 250.0
        elif champ.R.level == 3:
            spec.base_damage = 325.0

    else:
        return None

    return spec
