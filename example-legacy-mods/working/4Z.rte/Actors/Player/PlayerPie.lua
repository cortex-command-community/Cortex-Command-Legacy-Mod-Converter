function Purchase(actor)

	if actor:GetNumberValue("Purchase") == 0 then
		actor:SetNumberValue("Purchase", 1);
	end
--[[
	if MovableMan:IsActor(actor) and 
	actor ~= nil then

		sfx = CreateAEmitter("Purchase Sound");
		sfx.Pos = actor.Pos;
		MovableMan:AddParticle(sfx);
	end
]]--
end
