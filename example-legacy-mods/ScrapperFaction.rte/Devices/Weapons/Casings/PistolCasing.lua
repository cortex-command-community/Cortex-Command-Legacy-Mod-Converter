function Create(self)

	self.soundTimer = Timer();
	self.soundTimerNum = 0;
	
end

function Update(self)
	if self.soundTimer:IsPastSimMS(self.soundTimerNum) then
		if self.TravelImpulse.Magnitude > 0.3 then
			self.soundTimerNum = 350;
			self.rollSound = true;
			local sfx
			sfx = CreateAEmitter("Scrappers Generic Pistol Casing Hit");
			sfx.Pos = self.Pos;
			MovableMan:AddParticle(sfx);	
		elseif self.TravelImpulse.Magnitude > 0.09 and self.TravelImpulse.Magnitude < 0.3 and self.rollSound ~= false then
			self.rollSound = false;
			local sfx
			sfx = CreateAEmitter("Scrappers Generic Pistol Casing Roll");
			sfx.Pos = self.Pos;
			MovableMan:AddParticle(sfx);	
		end	
	end
end