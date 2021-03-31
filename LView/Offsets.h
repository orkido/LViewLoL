#pragma once
#include "ConfigSet.h"

/// Defines offsets for reading structs from league of legends memory
class Offsets {
	
public:
	Offsets();

	static int GameTime;
	static int GameVersion;

	static int ViewProjMatrices;
	static int Renderer;
	static int RendererWidth;
	static int RendererHeight;

	static int ObjectManager;
	static int LocalPlayer;
	static int UnderMouseObject;

	static int Chat;
	static int ChatIsOpen;
	static int FnCharacterDataStackUpdate;

	static int ObjIndex;
	static int ObjTeam;
	static int ObjNetworkID;
	static int ObjPos;
	static int ObjVisibility;
	static int ObjSpawnCount;
	static int ObjHealth;
	static int ObjMaxHealth;
	static int ObjAbilityHaste;
	static int ObjLethality;
	static int ObjMana;
	static int ObjInvulnerable;
	static int ObjTargetable;
	static int ObjRecallState;
	static int ObjArmor;
	static int ObjBonusArmor;
	static int ObjMagicRes;
	static int ObjBonusMagicRes;
	static int ObjBaseAtk;
	static int ObjBonusAtk;
	static int ObjMoveSpeed;
	static int ObjSpellBook;
	static int ObjName;
	static int ObjLvl;
	static int ObjTransformation;
	static int ObjMissileSpellCast;
	static int ObjExpiry;
	static int ObjCrit;
	static int ObjCritMulti;
	static int ObjAbilityPower;
	static int ObjAtkSpeedMulti;
	static int ObjAtkRange;
	static int ObjMagicPen;
	static int ObjMagicPenMulti;
	static int ObjAdditionalApMulti;
	static int ObjItemList;
	static int ObjSrcIndex;
	static int ObjExperience;
	static int ObjDirection;

	static int ItemListItem;
	static int ItemInfo;
	static int ItemInfoId;
	static int ItemActiveName;
	static int ItemCharges;

	static int SpellSlotLevel;
	static int SpellSlotTime;
	static int SpellSlotDamage;
	static int SpellSlotSpellInfo;
	static int SpellInfoSpellData;
	static int SpellDataSpellName;
	static int SpellDataMissileName;
	static int SpellSlotSmiteTimer;
	static int SpellSlotSmiteCharges;
	static int SpellSlotCharges;
	static int SpellSlotTimeCharge;
	static int SpellSlotValue;
	static int SpellDataManaArray;

	static int ObjectMapCount;
	static int ObjectMapRoot;
	static int ObjectMapNodeNetId;
	static int ObjectMapNodeObject;

	static int MissileSpellInfo;
	static int MissileSrcIdx;
	static int MissileDestIdx;
	static int MissileStartPos;
	static int MissileEndPos;

	static int MinimapObject;
	static int MinimapObjectHud;
	static int MinimapHudPos;
	static int MinimapHudSize;

	static int CharacterDataStack;
	static int CharacterDataStackSkinId;

	static int ObjBuffManager;
	static int BuffManagerEntriesArray;
	static int BuffEntryBuff;
	static int BuffEntryBuffStartTime;
	static int BuffEntryBuffEndTime;
	static int BuffName;
	static int BuffEntryBuffCount;
	static int BuffEntryBuffNodeStart;
	static int BuffEntryBuffNodeCurrent;
};