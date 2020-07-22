function Create(self)

	self.grenadeCooldownTimer = Timer();

	self.burstTimer = Timer();
	self.burst = false;
	self.canBurst = true;


	self.parent = nil;
	self.pullTimer = Timer();

	self.newMag = false;
	self.chamber = true;    
	self.num = math.pi;    
	self.sfx = true;    

	
	self.negNum = 0;

end

function Update(self)

	local actor = MovableMan:GetMOFromID(self.RootID);
	if actor and IsAHuman(actor) then
		self.parent = ToAHuman(actor);
	else
		self.parent = nil;
		-- cock and load on pickup
		--self.chamber = true;    --
		--self.pullTimer:Reset();    --
		--self.num = math.pi;    --
		--self.sfx = true;    --
	end
	
	
	if self.parent == nil and self.chamber == true then
    
		self.chamber = false;
		if self.pullTimer:IsPastSimMS(500) then
        
		else
			self.stoppedPremature = true;
		end
		
    end
	
	
	if self:DoneReloading() == true and self.lastMagazineAmmo > 0 then
		self.Magazine.RoundCount = self.Magazine.RoundCount + 1;
		self.newMag = false;
	end
	
	
	if self.parent then

		if self.Magazine then
    
			if self.stoppedPremature == true then
            
				self.chamber = true;
				self.pullTimer:Reset();
				self.num = math.pi;
				self.sfx = true;

				self.stoppedPremature = false;
			end

			self.lastAmmo = self.Magazine.RoundCount;

			if self.newMag == true then

				self.chamber = true;
				self.pullTimer:Reset();
				self.num = math.pi;
				self.sfx = true;

				self.newMag = false;
			end
		else
			self.newMag = true;
			self.lastMagazineAmmo = self.lastAmmo;
		end

		if self.chamber == true then

			self:Deactivate();

			if self.pullTimer:IsPastSimMS(500) then            

				if self.sfx ~= false then
					sfx = CreateAEmitter("Chamber " .. self.PresetName);
					sfx.Pos = self.Pos;
					MovableMan:AddParticle(sfx);
					self.sfx = false
				end
            
				self.RotAngle = self.RotAngle +self.negNum*math.sin(self.num)/6;

				self.num = self.num - math.pi*0.06;
			end

			if self.num <= 0 then
        
				self.num = 0;
				self.chamber = false;
			end
		end
	end
	

	if self.HFlipped == true then
		self.negNum = -1;
	else
		self.negNum = 1;
	end
	
	if self.FiredFrame then
		for i = 1, 2 do
			Effect = CreateMOSParticle("Tiny Smoke Ball 1", "Base.rte")
			if Effect then
				Effect.Pos = self.MuzzlePos;
				Effect.Vel = (self.Vel + Vector(RangeRand(-20,20), RangeRand(-20,20)) + Vector(150*self.negNum,0):RadRotate(self.RotAngle)) / 30
				MovableMan:AddParticle(Effect)
			end
		end
		
		if PosRand() < 0.5 then
			Effect = CreateMOSParticle("Side Thruster Blast Ball 1", "Base.rte")
			if Effect then	
				Effect.Pos = self.MuzzlePos;
				Effect.Vel = (self.Vel + Vector(150*self.negNum,0):RadRotate(self.RotAngle)) / 10
				MovableMan:AddParticle(Effect)
			end
		end
	end
	
	
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