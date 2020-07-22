
function Create(self)

	self.flashTimer = Timer();
	self.flashLength = 40;
	
	self.lifeTimer = Timer();
	self.duration = 1000 * 10;

	local actor = MovableMan:GetMOFromID(self.Sharpness);
	if actor and IsActor(actor) then
		self.target = ToActor(actor);
		self.target.GibImpulseLimit = self.target.GibImpulseLimit * 9001;
	else
		self.ToDelete = true;
	end
end

function Update(self)

	if self.target and IsActor(self.target) then

		if self.lifeTimer:IsPastSimMS(self.duration) then
			self.ToDelete = true;
			self.target.GibImpulseLimit = self.target.GibImpulseLimit / 9001;
		else
			self.target.Health = self.target.MaxHealth;
			
			if self.flashTimer:IsPastSimMS(self.flashLength * 2) then
				self.flashTimer:Reset();
				self.target:FlashWhite(self.flashLength);
			end
			
			for i = 1 , MovableMan:GetMOIDCount() - 1 do
				local mo = MovableMan:GetMOFromID(i);
				if mo and mo.RootID == self.target.ID then

					mo = ToMOSRotating(mo);
					mo.MissionCritical = true;
					mo:RemoveWounds(99);
				end
			end
		end
	else
		self.ToDelete = true
	end
end