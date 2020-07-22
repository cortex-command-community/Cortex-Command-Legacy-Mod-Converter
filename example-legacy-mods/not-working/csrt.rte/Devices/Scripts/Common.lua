function Create(self)

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
end