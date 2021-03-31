#pragma once
#include <string>

class BuffInstance
{
public:
	
	BuffInstance(std::string buffname, float starttime, float endtime) : name(buffname), startTime(starttime), endTime(endtime) {}

	std::string name;
	float startTime;
	float endTime;
};