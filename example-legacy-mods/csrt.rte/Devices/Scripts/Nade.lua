function Create(self)

	self.grenadeCooldownTimer = Timer();

	self.burstTimer = Timer();
	self.burst = false;
	self.canBurst = true;
end

function Update(self)

	-- magic code to make the grenade go the right way
	if self.HFlipped then
		self.negNum = -1;
	else
		self.negNum = 1;
	end

	--magic code to find who is holding us
	local actor = MovableMan:GetMOFromID(self.RootID);
	if actor and IsAHuman(actor) then
		self.parent = ToAHuman(actor);
	else
		self.parent = nil;
	end

	if self.parent then	--if we are being held
		if self.parent:IsPlayerControlled() then -- if player controls the person who is holding us
			if UInputMan:KeyPressed(6) and self.grenadeCooldownTimer:IsPastSimMS(5000) then-- 6 = F key is pressed
			
				-- reset cooldown timer so we have to wait 5 more seconds
				self.grenadeCooldownTimer:Reset();				
				
				--define the grenade as our AEmitter
				self.Grenade = CreateAEmitter("Ronin Thumper Grenade Shot Impact", "M16A4.rte");
				--define its position as our muzzle, but a little lower (where the underbarrel launcher is)
				self.Grenade.Pos = self.MuzzlePos + Vector(0*self.negNum, 3):RadRotate(self.RotAngle);
				--define its velocity as forward where the gun is facing
				self.Grenade.Vel = self.Vel + Vector(60*self.negNum,0):RadRotate(self.RotAngle);
				--set its team as our team so it won't hit us (if friendly fire is off)
				self.Grenade.Team = self.Team;
				--set it to not hit the gun no matter friendly fire options, so it can't blow up in our face
				self.Grenade:SetWhichMOToNotHit(self, -1);
				--spawn it
				MovableMan:AddParticle(self.Grenade);
				
				--do the same process but for an aemitter whose sole purpose is to play a sound then disappear
				self.sfx = CreateAEmitter("M16A4 Underbarrel Grenade Launch");
				self.sfx.Pos = self.Pos;
				MovableMan:AddParticle(self.sfx);				
				
				
			end
		end
	end

	if self.canBurst == true and self:IsActivated() and self.Magazine ~= nil and self.Magazine.RoundCount > 0 then
		self.burstTimer:Reset();
		self.canBurst = false;
		self.burst = true;
	end

	if self.burst == true then
		if self.burstTimer:IsPastSimMS(200) then
			self.burstTimer:Reset();
			self:Deactivate();
			self.burst = false;
		else
			self:Activate();
		end
	else
		if self.canBurst == false then
			self:Deactivate();
			if self.burstTimer:IsPastSimMS(300) then
				self.canBurst = true;
			end
		end
	end

end