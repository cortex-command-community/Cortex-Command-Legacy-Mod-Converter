function Create(self)
	self.origSharpLength = ToHDFirearm(self).SharpLength;

	self.fireTimer = Timer();
	self.chargeTimer = Timer();
	self.chargeCounter = 1;

	self.maxCharge = 8;
	self.chargesPerSecond = 8;
end

function Update(self)
	local Unit = MovableMan:GetMOFromID(self.RootID);
	if self:IsAttached() and MovableMan:IsActor(Unit) and Unit:IsInGroup("Z Steel Soldiers") and Unit.PresetName == "Laser" then
		self.SharpLength = self.origSharpLength*1.2;
		self.GetsHitByMOs = false;
	else
		self.SharpLength = self.origSharpLength;
		self.GetsHitByMOs = true;
	end
	
	if self:IsAttached() then
		if MovableMan:IsActor(Unit) and ToActor(Unit):IsPlayerControlled() == false then
			ToActor(Unit):GetController():SetState(Controller.BODY_CROUCH,false);
		end
	end

	if self:IsActivated() and self.fireTimer:IsPastSimMS(1500) then
		self.fireTimer:Reset();

		if self.HFlipped == false then
			self.reverseNum = 1;
		else
			self.reverseNum = -1;
		end

		for i = 1, self.chargeCounter do
			local damagePar = CreateMOPixel("LaserGun Laser Particle");
			damagePar.Pos = self.MuzzlePos + Vector(((i-1)*-2)*self.reverseNum,0):RadRotate(self.RotAngle);
			damagePar.Vel = Vector(200*self.reverseNum,0):RadRotate(self.RotAngle);
			damagePar:SetWhichMOToNotHit(MovableMan:GetMOFromID(self.RootID),-1);

			if MovableMan:IsActor(Unit) then
				damagePar.Team = ToActor(Unit).Team;
				damagePar.IgnoresTeamHits = true;
			end

			MovableMan:AddParticle(damagePar);
		end

		local soundfx = CreateAEmitter("LaserGun Sound Fire");
		soundfx.Pos = self.MuzzlePos;
		MovableMan:AddParticle(soundfx);
		
		local effectPar = CreateMOPixel("LaserGun Effect Particle");
		effectPar.Pos = self.MuzzlePos;
		MovableMan:AddParticle(effectPar);

		self.chargeCounter = 1;
		self:Deactivate();

	else
		if self.chargeCounter <= self.maxCharge then
			self.chargeCounter = math.min(self.chargeCounter + ((self.chargeTimer.ElapsedSimTimeMS/1000)*self.chargesPerSecond),self.maxCharge);
			self.chargeTimer:Reset();
		end
	end
end