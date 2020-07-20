function Create(self)
	self.fireballCountMax = 2;
	self.fireVel = 20;
	
	if self.Magazine and self.Magazine.NextRound then
		self.fireVel = self.Magazine.NextRound.FireVel;
		self.fireballCountMax = self.Magazine.Capacity;
	end
	self.fireballTable = {};
end
function Update(self)
	local fireballCount = 0;
	for i = 1, #self.fireballTable do
		if self.fireballTable[i] and MovableMan:IsParticle(self.fireballTable[i]) then
			fireballCount = fireballCount + 1;
		else
			table.remove(self.fireballTable, i);
		end
	end
	if fireballCount < self.fireballCountMax then
		if self.FiredFrame then
			local negNum = 1;
			if self.HFlipped then
				negNum = -1;
			end
			local fireball = CreateMOSParticle("Mario.rte/Fire Flower Fireball");
			fireball.Pos = self.MuzzlePos;
			fireball.Vel = self.Vel / 2 + (Vector(5 * negNum, 0):RadRotate(self.RotAngle) - SceneMan.GlobalAcc * 0.1):SetMagnitude(self.fireVel);
			fireball.Team = self.Team;
			fireball.IgnoresTeamHits = true;
			MovableMan:AddParticle(fireball);
			table.insert(self.fireballTable, fireball);
		end
	else
		self:Deactivate();
	end
	if self.Magazine then
		self.Magazine.RoundCount = self.fireballCountMax;
		self.Magazine.Frame = self.Frame;
		if self:GetParent() then
			self.Scale = 0;
			self.Magazine.Scale = 1;
		else
			self.Scale = 1;
			self.Magazine.Scale = 0;
		end
	else
		self.Scale = 1;
	end
	self.AngularVel = self.AngularVel / 2;
	self.RotAngle = self.RotAngle / 2;
end
