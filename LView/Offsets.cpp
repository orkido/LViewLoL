#include "Offsets.h"

Offsets::Offsets() {};

int Offsets::GameTime = 0x02F6D134; //			11.6 ==> 11.7
int Offsets::GameVersion = 0x2F872D8; //		11.6 ==> 11.7

int Offsets::ViewProjMatrices = 0x2F97FF0; //	11.6 ==> 11.7
int Offsets::Renderer = 0x2F9ADD0; //			11.6 ==> 11.7
int Offsets::RendererWidth = 0x0C; //			11.6 ==> 11.7
int Offsets::RendererHeight = 0x10; //			11.6 ==> 11.7

int Offsets::ObjectManager = 0x16D85B8; //		11.6 ==> 11.7
int Offsets::LocalPlayer = 0x2F7513C; //		11.6 ==> 11.7
int Offsets::UnderMouseObject = 0x2326780; //	11.6 ==> 11.7

int Offsets::ObjIndex = 0x20;
int Offsets::ObjTeam = 0x4C;
int Offsets::ObjNetworkID = 0xCC;
int Offsets::ObjPos = 0x1d8;
int Offsets::ObjVisibility = 0x270;
int Offsets::ObjSpawnCount = 0x284;
int Offsets::ObjSrcIndex = 0x290;
int Offsets::ObjMana = 0x298;
int Offsets::ObjHealth = 0xD98;
int Offsets::ObjMaxHealth = 0xDA8;
int Offsets::ObjArmor = 0x12C4; //				11.6 ==> 11.7
int Offsets::ObjMagicRes = 0x12CC; //			11.6 ==> 11.7
int Offsets::ObjBaseAtk = 0x129C; //			11.6 ==> 11.7
int Offsets::ObjBonusAtk = 0x1218; //			11.6 ==> 11.7
int Offsets::ObjMoveSpeed = 0x12DC; //			11.6 ==> 11.7
int Offsets::ObjSpellBook = 0x2BA0; //			11.6 ==> 11.7
int Offsets::ObjName = 0x2F8C; //				11.6 ==> 11.7
int Offsets::ObjLvl = 0x36DC; //				11.6 ==> 11.7
int Offsets::ObjExpiry = 0x298;
int Offsets::ObjCrit = 0x12C0; //				11.6 ==> 11.7
int Offsets::ObjCritMulti = 0x12B0; //			11.6 ==> 11.7
int Offsets::ObjAbilityPower = 0x1228; //		11.6 ==> 11.7
int Offsets::ObjAtkSpeedMulti = 0x1270;
int Offsets::ObjItemList = 0x3714; //			11.6 ==> 11.7
int Offsets::ObjExperience = 0x36CC; //			11.6 ==> 11.7

int Offsets::ItemListItem = 0xC;
int Offsets::ItemInfo = 0x20;
int Offsets::ItemInfoId = 0x68;

int Offsets::SpellSlotLevel = 0x20;
int Offsets::SpellSlotTime = 0x28;
int Offsets::SpellSlotDamage = 0x94;
int Offsets::SpellSlotSpellInfo = 0x13C;
int Offsets::SpellInfoSpellData = 0x44;
int Offsets::SpellDataSpellName = 0x64;
int Offsets::SpellDataMissileName = 0x64;
int Offsets::SpellSlotSmiteTimer = 0x64;
int Offsets::SpellSlotSmiteCharges = 0x58;

int Offsets::MissileSpellInfo = 0x258; //		11.6 ==> 11.7
int Offsets::MissileSrcIdx = 0x2B8; //			11.6 ==> 11.7
int Offsets::MissileDestIdx = 0x310; //			11.6 ==> 11.7
int Offsets::MissileStartPos = 0x2D0; //		11.6 ==> 11.7
int Offsets::MissileEndPos = 0x2DC; //			11.6 ==> 11.7

int Offsets::ObjectMapCount = 0x2C;
int Offsets::ObjectMapRoot = 0x28;
int Offsets::ObjectMapNodeNetId = 0x10;
int Offsets::ObjectMapNodeObject = 0x14;

int Offsets::MinimapObject = 0x2F74B38; //		11.6 ==> 11.7
int Offsets::MinimapObjectHud = 0x88;
int Offsets::MinimapHudPos = 0x60;
int Offsets::MinimapHudSize = 0x68;

int Offsets::ObjBuffManager = 0x2178;
int Offsets::BuffManagerEntriesArray = 0x10;
int Offsets::BuffEntryBuff = 0x8;
int Offsets::BuffEntryBuffStartTime = 0xC;
int Offsets::BuffEntryBuffEndTime = 0x10;
int Offsets::BuffName = 0x8;