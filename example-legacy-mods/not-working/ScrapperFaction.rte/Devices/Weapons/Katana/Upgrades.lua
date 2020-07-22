function KATANAFIRE(actor)
	local gun = ToAHuman(actor).EquippedItem;
	if gun ~= nil then
		local Funds = ActivityMan:GetActivity():GetTeamFunds(ToAHuman(actor).Team);
		ActivityMan:GetActivity():SetTeamFunds(Funds - 15, ToAHuman(actor).Team);
		local gun = ToHDFirearm(gun);
		gun:SetNumberValue("Fire Upgrade", 2)		
	end
end

function KATANABLOCK(actor)
	local gun = ToAHuman(actor).EquippedItem;
	if gun ~= nil then
		local Funds = ActivityMan:GetActivity():GetTeamFunds(ToAHuman(actor).Team);
		ActivityMan:GetActivity():SetTeamFunds(Funds - 0, ToAHuman(actor).Team);
		local gun = ToHDFirearm(gun);
		gun:SetNumberValue("Block Mode", 1)	
	end
end
function KATANANORMAL(actor)
	local gun = ToAHuman(actor).EquippedItem;
	if gun ~= nil then
		local gun = ToHDFirearm(gun);
		gun:SetNumberValue("Block Mode", 0)
		gun:SetNumberValue("HaveToResetNum", 1)		
	end
end
