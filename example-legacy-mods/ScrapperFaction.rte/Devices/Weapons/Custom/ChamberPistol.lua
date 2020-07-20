
function Create(self)

	self.parent = nil;
	self.pullTimer = Timer();

	self.newMag = false;
	self.chamber = true;		--
	--self.pullTimer:Reset();	--
	self.num = math.pi;		--
	self.sfx = true;		--
	self.sfxSetShot = true;
	self.sfxSetTail = true;
	self.sfxSetMech = true;
	
	self:SetNumberValue("Recoiling", 0);

	self.negNum = 0;
	self.sLength = self.SharpLength;
	self.ShakeRange = 6
	self.sRange = self.ShakeRange
	self.lifeTimer = Timer();
	self.lifeTimerReset = false
	self.flashCooldown = Timer();
	self.flashedTimer = Timer();
	self.shotTimer = Timer();
	self.recoilTimer = Timer();
	
	self.chargeDelay = 20;      
	self.chargeTimer = Timer();  
	self.charge = false;   

	local actor = MovableMan:GetMOFromID(self.RootID);
	if actor and IsAHuman(actor) then
		self.parent = ToAHuman(actor);
	end
end

function Update(self)

	local actor = MovableMan:GetMOFromID(self.RootID);
	if actor and IsAHuman(actor) then
		self.parent = ToAHuman(actor);
	else
		self.parent = nil;
	-- cock and load on pickup
		--self.chamber = true;	--
		--self.pullTimer:Reset();	--
		--self.num = math.pi;	--
		--self.sfx = true;	--
	end

	if self.justShot == true then
	
		if self.shotTimer:IsPastSimMS(20) then
			
			self.justShot = false;
		end
		
	end
	
	if self.charge == true then           

		if self.chargeTimer:IsPastSimMS(self.chargeDelay) then   
			self:Activate();    
			self.charge = false;
		else            
			self:Deactivate();     
		end
	elseif self.Magazine and self:IsActivated() and self.chamber == false then      
		if self.triggerPulled == false then        
			self:Deactivate();          
			self.charge = true;        
			self.triggerPulled = true;      
			self.chargeTimer:Reset();    
			sfx = CreateAEmitter("Pre Custom Pistol");
			sfx.Pos = self.Pos;
			MovableMan:AddParticle(sfx);		
		end
	else    
		self.triggerPulled = false;
	end
		
	if self:GetNumberValue("Recoiling") == 1 then	
		if self.recoilTimer:IsPastSimMS(45) then
			self:SetNumberValue("Recoiling", 0);
		elseif self.recoilTimer:IsPastSimMS(35) then
			self.SharpStanceOffset = Vector(14, 0);
			self.RotAngle = self.RotAngle + (0.05 * self.negNum);
		elseif self.recoilTimer:IsPastSimMS(25) then
			self.SharpStanceOffset = Vector(12, 0);	
			self.RotAngle = self.RotAngle + (0.10 * self.negNum);
		elseif self.recoilTimer:IsPastSimMS(15) then
			self.SharpStanceOffset = Vector(10, 0);	
			self.RotAngle = self.RotAngle + (0.15 * self.negNum);
		elseif self.recoilTimer:IsPastSimMS(5) then
			self.SharpStanceOffset = Vector(9, 0);
			self.RotAngle = self.RotAngle + (0.2 * self.negNum);
		end
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
	
		self:SetNumberValue("Recoiling", 1);
		self.recoilTimer:Reset();
		self.SharpStanceOffset = Vector(10, 0);
		self.RotAngle = self.RotAngle + (0.17 * self.negNum);
	
		if self.echoMakingSound == true then
			
			if MovableMan:IsParticle(self.echoSound) then	

				self.echoSound.ToDelete = true;
			
				self.echoMakingSound = false;		
	
			end
		
		end

		self.justShot = true;
		self.shotTimer:Reset();

		if self.sfxSetMech ~= false then

			sfxSetShot = CreateAEmitter("HiFi Custom Pistol");
			sfxSetShot.Pos = self.Pos;
			MovableMan:AddParticle(sfxSetShot);

		end
		
		if self.sfxSetMech ~= false then

			sfxSetShot = CreateAEmitter("Shell Custom Pistol");
			sfxSetShot.Pos = self.Pos;
			MovableMan:AddParticle(sfxSetShot);

		end
		
		if self.sfxSetMech ~= false then

			sfxSetShot = CreateAEmitter("CoreBass Custom Pistol");
			sfxSetShot.Pos = self.Pos;
			MovableMan:AddParticle(sfxSetShot);

		end

		local Vector2 = Vector(0,-700);

		local Vector2Left = Vector(0,-700):RadRotate(45);

		local Vector2Right = Vector(0,-700):RadRotate(-45);

		local Vector3 = Vector(0,0);

		local Vector4 = Vector(0,0);

		self.ray = SceneMan:CastObstacleRay(self.Pos, Vector2, Vector3, Vector4, self.RootID, self.Team, 128, 7);

		self.rayRight = SceneMan:CastObstacleRay(self.Pos, Vector2Right, Vector3, Vector4, self.RootID, self.Team, 128, 7);

		self.rayLeft = SceneMan:CastObstacleRay(self.Pos, Vector2Left, Vector3, Vector4, self.RootID, self.Team, 128, 7);

		if self.ray < 0 or self.rayRight < 0 or self.rayLeft < 0 then	
		
			if self.parent then
			
				if self.parent:IsPlayerControlled() then
	
					if self.sfxSetTail ~= false then

						self.sfx = CreateAEmitter("Reflection Custom Pistol");
						self.sfx.Pos = self.Pos;
						self.echoSound = ToAEmitter(self.sfx)
						MovableMan:AddParticle(self.sfx);
						self.echoMakingSound = true;

					end
				else
					if self.sfxSetTail ~= false then

						self.sfx = CreateAEmitter("Reflection Weak Custom Pistol");
						self.sfx.Pos = self.Pos;
						self.echoSound = ToAEmitter(self.sfx)
						MovableMan:AddParticle(self.sfx);
						self.echoMakingSound = true;

					end			
				end
			end
			
			if self.sfxSetMech ~= false then

				sfxSetShot = CreateAEmitter("Add Custom Pistol");
				sfxSetShot.Pos = self.Pos;
				MovableMan:AddParticle(sfxSetShot);

			end
			
			-- if self.sfxSetShot ~= false then

				-- sfxSetShot = CreateAEmitter("Noise Custom Pistol");
				-- sfxSetShot.Pos = self.Pos;
				-- MovableMan:AddParticle(sfxSetShot);

			-- end
				
			
		else
		
			if self.sfxSetMech ~= false then

				sfxSetShot = CreateAEmitter("AddShort Custom Pistol");
				sfxSetShot.Pos = self.Pos;
				MovableMan:AddParticle(sfxSetShot);

			end

	
			if self.parent then
			
				if self.ray > 200 or self.rayRight > 200 or self.rayLeft > 200 then
			
					if self.parent:IsPlayerControlled() then
		
						if self.sfxSetTail ~= false then

							self.sfx = CreateAEmitter("Reflection Big Custom Pistol Indoors");
							self.sfx.Pos = self.Pos;
							self.echoSound = ToAEmitter(self.sfx)
							MovableMan:AddParticle(self.sfx);
							self.echoMakingSound = true;

						end
					else
						if self.sfxSetTail ~= false then

							self.sfx = CreateAEmitter("Reflection Big Weak Custom Pistol Indoors");
							self.sfx.Pos = self.Pos;
							self.echoSound = ToAEmitter(self.sfx)
							MovableMan:AddParticle(self.sfx);
							self.echoMakingSound = true;

						end			
					end
				else
					if self.parent:IsPlayerControlled() then
		
						if self.sfxSetTail ~= false then

							self.sfx = CreateAEmitter("Reflection Custom Pistol Indoors");
							self.sfx.Pos = self.Pos;
							self.echoSound = ToAEmitter(self.sfx)
							MovableMan:AddParticle(self.sfx);
							self.echoMakingSound = true;

						end
					else
						if self.sfxSetTail ~= false then

							self.sfx = CreateAEmitter("Reflection Weak Custom Pistol Indoors");
							self.sfx.Pos = self.Pos;
							self.echoSound = ToAEmitter(self.sfx)
							MovableMan:AddParticle(self.sfx);
							self.echoMakingSound = true;

						end			
					end
				end
			end
			
			-- if self.sfxSetShot ~= false then

				-- sfxSetShot = CreateAEmitter("Noise Custom Pistol");
				-- sfxSetShot.Pos = self.Pos;
				-- MovableMan:AddParticle(sfxSetShot);

			-- end
	
		end

	end

	if self:DoneReloading() == true and self.lastMagazineAmmo > 0 then
		self.Magazine.RoundCount = self.Magazine.RoundCount + 1;
		self.newMag = false;
	end

	if self.HFlipped then
		self.negNum = -1;
	else
		self.negNum = 1;
	end

	if self.parent == nil and self.chamber == true then
		
		self.chamber = false;
		if self.pullTimer:IsPastSimMS(450) then
		
		
		else
			self.stoppedPremature = true;
		end
		self:RemoveNumberValue("ChamberRot")
		self:RemoveNumberValue("Chambering")

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
			self.lastMag = self.Magazine;
			self.velApplied = false;
		else
			
			self.newMag = true;
			self.lastMagazineAmmo = self.lastAmmo;

		end

		if self.chamber == true then
			self:SetNumberValue("ChamberRot", self.RotAngle)
			self:SetNumberValue("Chambering", 1)
			self:Deactivate();
			--self.parent:GetController():SetState(Controller.WEAPON_FIRE,false);

			if self.pullTimer:IsPastSimMS(550) then
				--self.parent:GetController():SetState(Controller.AIM_SHARP,false);
				--self.Frame = 1;

				if self.sfx ~= false then
					sfx = CreateAEmitter("Chamber " .. self.PresetName);
					sfx.Pos = self.Pos;
					MovableMan:AddParticle(sfx);

					self.sfx = false;
				end

				self.RotAngle = self.RotAngle +self.negNum*math.sin(self.num)/8;

				self:SetNumberValue("ChamberRot", self.RotAngle)

				self.num = self.num - math.pi*0.060;
			end

			if self.num <= 0 then

				self.num = 0;
				self.chamber = false;
				self.ShakeRange = self.sRange
				self:RemoveNumberValue("Chambering")
			end
		end
	end
end