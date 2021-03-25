#NoEnv
#MaxHotkeysPerInterval 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
#Persistent
#InstallKeybdHook
#InstallMouseHook

#If leagueClientActive()
	$q::
		While(GetKeyState("q","P")) {
			Send, q
			Sleep, 004
		}
		Return
		
	$w::
		While(GetKeyState("w","P")) {
			Send, w
			Sleep, 004
		}
		Return
	
	$e::
		While(GetKeyState("e","P")) {
			Send, e
			Sleep, 004
		}
		Return
		
	$r::
		While(GetKeyState("r","P")) {
			Send, r
			Sleep, 004
		}
		Return
#If

leagueClientActive() {
	return WinActive("ahk_class RiotWindowClass")
}
