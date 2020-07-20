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
			sfx = CreateAEmitter("Scrappers Generic Heavy Casing Hit");
			sfx.Pos = self.Pos;
			MovableMan:AddParticle(sfx);	
		end	
	end
end